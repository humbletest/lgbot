from config import config

import backoff

import json

import sys, traceback

from serverutils.utils import read_string_from_file
from serverutils.utils import getjsonbin, getjsonbinobj

from lbot.lichess import Lichess
from lbot.model import Challenge, Game

import threading

import chess
from chess.variant import find_variant
from chess.uci import InfoHandler, Engine

import random

from requests.exceptions import ChunkedEncodingError, ConnectionError, HTTPError
from urllib3.exceptions import ProtocolError

try:
    from http.client import RemoteDisconnected
    # New in version 3.5: Previously, BadStatusLine('') was raised.
except ImportError:
    from http.client import BadStatusLine as RemoteDisconnected

import queue

#########################################################

VERSION = "1.0.0"
LICHESS_API_BASE_URL = "https://lichess.org/"

#########################################################

def empty_queue(q):
    while not q.empty():
        q.get()

def senducis(ucis):
    print(json.dumps({
        "enginecmd": "ucis",
        "ucis": ucis
    }))    

def sendoption(name, value):
    senducis([
        "setoption name {} value {}".format(name, value)
    ])

def sendenginelog(value):
    print(json.dumps({
        "enginecmd": "enginelog",
        "value": value
    }))    

def setup_board(game):
    if game.variant_name.lower() == "chess960":
        board = chess.Board(game.initial_fen, chess960=True)
    elif game.variant_name == "From Position":
        board = chess.Board(game.initial_fen)
    else:
        VariantBoard = find_variant(game.variant_name)
        board = VariantBoard()
    moves = game.state["moves"].split()
    for move in moves:
        board = update_board(board, move)

    return board

def is_white_to_move(game, moves):
    return len(moves) % 2 == (0 if game.white_starts else 1)

def is_engine_move(game, moves):
    return game.is_white == is_white_to_move(game, moves)

def update_board(board, move):
    uci_move = chess.Move.from_uci(move)
    board.push(uci_move)
    return board

def get_most_drawish_move(info):
    print("getting most drawish move")
    try:
        mindelta = 10000 * 10000
        move = None
        for i in range(1, len(info["score"])+1):
            score = info["score"][i][0]
            if score == None:
                mate = info["score"][i][1]
                if mate < 0:
                    score = -10000 - mate
                else:
                    score = 10000 - mate
            scdelta = score * score
            if scdelta < mindelta:
                mindelta = scdelta
                pv = info["pv"][i]
                move = pv[0]
                print("found more drawish move", move, score)
        print("most drawish {} delta {}".format(move, mindelta))
        return move
    except:
        traceback.print_exc(file = sys.stderr)
        return None

#########################################################

class Bot:
    def __init__(self, cfg):
        self.cfg = cfg
        self.li = None
        self.lock = threading.Lock()
        self.num_playing = 0
        self.engine_queue = queue.Queue()
        self.username = "!nouser"
        self.controlstarted = False

    def modify_num_playing_atomic(self, delta):    
        self.lock.acquire()
        self.num_playing += delta
        self.lock.release()

    def sendmultipv(self):        
        if "multipv" in self.cfg.profileobj:
            sendoption("MultiPV", self.cfg.multipv)

    def senducioptions(self):
        for ucioption in self.cfg.ucioptions:        
            sendoption(ucioption.name, ucioption.value)  

    def max_games_reached(self):        
        return self.num_playing >= self.cfg.concurrency  

    def loadprofile(self):            
        try:
            print("loading profile")
            profile = self.li.get_profile()
            self.username = profile["username"]
            print("profile loaded for {}".format(self.username))
        except:
            print("! loading profile failed")
            traceback.print_exc(file=sys.stderr)    

    def get_engine_best_move(self, board, wtime, btime, winc, binc):
        first = ( board.fullmove_number == 1 )
        print("getting engine best move", first, wtime, btime, winc, binc)        
        gocommand = "go wtime {} btime {} winc {} binc {}".format(wtime, btime, winc, binc)
        if first:
            gocommand = "go movetime {}".format(2000)
        senducis([
            "position fen {}".format(board.fen()),
            gocommand
        ])
        eng = Engine()
        eng.board = board
        infh = InfoHandler()    
        eng.info_handlers.append(infh)
        while True:
            sline = self.engine_queue.get()        
            parts = sline.split(" ")
            kind = parts[0]        
            if kind == "bestmove":
                try:
                    move = chess.Move.from_uci(parts[1])
                    print("best move received", move)                
                    if self.cfg.selectmove == "mostdrawish":
                        move = get_most_drawish_move(infh.info)
                    return move
                except:
                    return None
            elif kind == "info":
                try:
                    eng._info(sline)
                    #print("engine thinking")
                except:
                    print("info handler error")
                    traceback.print_exc(file = sys.stderr)
        return None

    def play_move(self, game, board, wtime, btime, winc, binc):
        print("playing move", wtime, btime, winc, binc)
        moves = list(board.generate_legal_moves())
        if len(moves)>0:
            best_move = random.choice(moves)
            print("random best move", best_move)
            engine_best_move = self.get_engine_best_move(board, wtime, btime, winc, binc)
            if not ( engine_best_move is None ):
                print("using engine best move", engine_best_move)
                best_move = engine_best_move
            print("making move {} in game {}".format(best_move.uci(), game.id))
            self.li.make_move(game.id, best_move)
            game.abort_in(20)
        else:
            print("! no legal move in game {}".format(game.id))

    def play_game(self, game_id):        
        self.modify_num_playing_atomic(1)
        print("playing game {}".format(game_id))
        updates = self.li.get_game_stream(game_id).iter_lines()
        game = Game(json.loads(next(updates).decode('utf-8')), self.username, self.li.baseUrl, 20)
        board = setup_board(game)    
        print(board)    
        # spawn fresh engine
        print(json.dumps({
            "enginecmd": "restart"
        }))
        self.sendmultipv()
        self.senducioptions()
        sendenginelog(False)
        empty_queue(self.engine_queue)
        moves = game.state["moves"].split()
        if is_engine_move(game, moves):                                        
            self.play_move(game, board, 2000, 2000, 0, 0)
        try:
            for binary_chunk in updates:
                upd = json.loads(binary_chunk.decode('utf-8')) if binary_chunk else None
                u_type = upd["type"] if upd else "ping"
                if u_type == "chatLine":
                    pass
                elif u_type == "gameState":
                    game.state = upd
                    moves = upd["moves"].split()
                    board = update_board(board, moves[-1])
                    if is_engine_move(game, moves):                                        
                        self.play_move(game, board, upd["wtime"], upd["btime"], upd["winc"], upd["binc"])
                elif u_type == "ping":
                    if game.should_abort_now():
                        print("aborting {} by lack of activity".format(game.url()))
                        self.li.abort(game.id)
        except (RemoteDisconnected, ChunkedEncodingError, ConnectionError, ProtocolError, HTTPError) as exception:
            print("! abandoning game due to connection error")
            traceback.print_exception(type(exception), exception, exception.__traceback__)        
        finally:
            print("game over {}".format(game.url()))
            self.modify_num_playing_atomic(-1)
            sendenginelog(True)

    def log_control_event(self, event):    
        print(event)
        try:        
            kind = event["type"]
            if kind == "challenge":
                chlng = Challenge(event["challenge"])
                if self.max_games_reached():
                    print("! max games reached, decline new {}".format(chlng))
                else:
                    try:
                        response = self.li.accept_challenge(chlng.id)
                        print("accept {}".format(chlng))                
                    except HTTPError as exception:
                        if exception.response.status_code == 404: # ignore missing challenge
                            print("skip missing {}".format(chlng))
                        else:
                            raise exception
            elif kind == "gameStart":            
                game_id = event["game"]["id"]            
                if self.max_games_reached():
                    print("! max games reached, decline new game {}".format(game_id))
                else:
                    threading.Thread(target = self.play_game, args = (game_id,)).start()
        except:
            print("! error handling event")
            traceback.print_exc(file = sys.stderr)

    @backoff.on_exception(backoff.expo, BaseException, max_time=600)
    def control_thread_func(self):
        print("starting control stream")    
        try:
            es = self.li.get_event_stream()
            print("event stream created")
            for evnt in es.iter_lines():
                if evnt:
                    event = json.loads(evnt.decode('utf-8'))
                    self.log_control_event(event)
                else:
                    self.log_control_event({"type": "ping", "num_playing": self.num_playing})
        except:
            print("! failed to get event stream") 
            traceback.print_exc(file = sys.stderr)       

    def startcontrol(self):        
        if self.controlstarted:
            print("! control stream already started")
        else:        
            threading.Thread(target = self.control_thread_func, args = ()).start()
            self.controlstarted = True

    def createli(self):        
        token = self.cfg.token
        print("creating lichess api agent", token, LICHESS_API_BASE_URL, VERSION)
        self.li = Lichess(token, LICHESS_API_BASE_URL, VERSION)
        print("lichess api agent created")
        print("testing lichess api agent")
        self.loadprofile()

#########################################################

bot = Bot(config)

while True:
    cmd = input("").rstrip()
    if cmd == "pc":
        print(bot.cfg)
    elif cmd == "lc":
        bot.cfg.fromfile()        
        print(bot.cfg)
        bot.createli()
    elif cmd == "lp":
        bot.loadprofile()
    elif cmd == "sc":
        bot.startcontrol()
    elif cmd == "x":
        break
    else:
        try:
            obj = json.loads(cmd)            
            if "engineline" in obj:                
                engineline = obj["engineline"]                
                bot.engine_queue.put(engineline)
        except:
            print("echo", cmd)
