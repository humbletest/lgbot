from config import config

import backoff

import json

import os, sys, traceback, time

from serverutils.utils import read_string_from_file
from serverutils.utils import getjsonbin, getjsonbinobj

from lbot.lichess import Lichess
from lbot.model import Challenge, Game

import threading

import chess
from chess.variant import find_variant
from chess.uci import InfoHandler, Engine
from chess.polyglot import open_reader

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

FIRST_MOVE_TIME = 2000

#########################################################

class TimeControl:
    def __init__(self, wtime, btime, winc, binc, board):
        self.wtime = int(wtime)
        self.btime = int(btime)
        self.winc = int(winc)
        self.binc = int(binc)       
        self.board = board 
        self.startedat = time.time()
        testboard = self.board.copy()
        while len(testboard.move_stack) > 0:
            testboard.pop()
        self.initial_fen = testboard.fen()

    def elapsed(self):
        return int( time.time() - self.startedat )

    def corrtime(self, t, color):
        if self.board.turn == color:
            return max(t - self.elapsed(), 0)
        return t

    def getwtime(self):
        return self.corrtime(self.wtime, chess.WHITE)        

    def getbtime(self):
        return self.corrtime(self.btime, chess.BLACK)        

    def getmoves(self):
        if len(self.board.move_stack) <= 0:
            return ""
        return " moves " + " ".join([move.uci() for move in self.board.move_stack])

    def gocommand(self, ponder = False):
        gc = "go wtime {} btime {} winc {} binc {}".format(self.getwtime(), self.getbtime(), self.winc, self.binc)
        if ponder:
            gc += " ponder"
        return gc        

    def positioncommand(self):
        return "position fen {}{}".format(self.initial_fen, self.getmoves())

    def __repr__(self):
        return "timecontrol wtime {} mwtime {} btime {} mbtime {} winc {} binc {} white's turn {} initial fen {}{}".format(self.wtime, self.getwtime(), self.btime, self.getbtime(), self.winc, self.binc, self.board.turn, self.initial_fen, self.getmoves())

class PvInfo:
    def __init__(self, bestmove = None, scorecp = None, scoremate = None, INFINITE_SCORE = 10000):
        self.bestmove = bestmove
        self.scorecp = scorecp
        self.scoremate = scoremate
        self.INFINITE_SCORE = INFINITE_SCORE

    def score(self, default = 0):
        if not ( self.scorecp is None ):
            return self.scorecp
        if not ( self.scoremate is None ):
            if self.scoremate > 0:
                return ( self.INFINITE_SCORE - self.scoremate )
            else:
                return ( - self.INFINITE_SCORE - self.scoremate )
                
        return default

    def __repr__(self):
        return "{} {}".format(self.bestmove, self.score())

class PvInfos:
    def __init__(self, infh):
        self.infh = infh
        self.pvis = {}

    def process(self):
        self.pvis = {}
        info = self.infh.info        
        pvobj = info["pv"]
        scoreobj = info["score"]
        for pvi in pvobj:
            try:
                pv = pvobj[pvi]
                bestmove = pv[0]
                score = scoreobj[pvi]
                scorecp = score[0]
                scoremate = score[1]
                self.pvis[pvi] = PvInfo(bestmove = bestmove, scorecp = scorecp, scoremate = scoremate)
            except:
                print("there was an error parsing pv")
                traceback.print_exc(file = sys.stderr)

    def getbest(self, sortfunc = None, verbose = False):
        self.process()
        items = self.pvis.items()
        if len(items) == 0:
            return None
        items = sorted(items, key = lambda item: item[0])
        if not ( sortfunc is None ):
            items = sorted(items, key = lambda item: sortfunc( item[1] ), reverse = True)
        if verbose:
            for item in items:
                print(item[0], item[1])
        return items[0][1]

#########################################################

def empty_queue(q):
    while not q.empty():
        q.get()

def get_book_dir_path(uci_variant):
    return os.path.join("book", uci_variant)

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

#########################################################

class Bot:
    def bot_startup_thread_func(self):
        delay = config.autostartbot
        if delay > 0:
            print("waiting {} seconds to start bot".format(delay))
            time.sleep(delay)
            print("auto starting bot")
            self.createli()            
            self.startcontrol()
        else:
            print("auto start bot disabled")

    def __init__(self, cfg):
        self.cfg = cfg
        self.li = None
        self.lock = threading.Lock()
        self.num_playing = 0
        self.engine_queue = queue.Queue()
        self.username = "!nouser"
        self.controlstarted = False
        self.ponder = None
        print("scheduling bot startup...")
        threading.Thread(target = self.bot_startup_thread_func, args = ()).start()

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

    def sendcorrecteducioptions(self, board = chess.Board()):
        self.senducioptions()
        self.sendmultipv()
        sendoption("UCI_Variant", type(board).uci_variant)

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

    def get_book_best_move(self, game, board):
        strategy = self.cfg.strategy
        if strategy == "none":
            return None
        uci_variant = game.variant_key
        book_dir_path = get_book_dir_path(uci_variant)
        if not ( os.path.exists(book_dir_path) ):
            print("book dir path {} does not exist".format(book_dir_path))
            return None
        for name in os.listdir(book_dir_path):
            book_path = os.path.join(book_dir_path, name)
            print("looking up move in {}".format(book_path))
            with chess.polyglot.open_reader(book_path) as reader:
                entries = reader.find_all(board, minimum_weight = self.cfg.minweight)                                
                entries = sorted(entries, key = lambda entry: entry.weight, reverse = True)
                if len(entries) > 0:
                    print("entries in {} : {}".format(book_path, [(entry.move().uci(), entry.weight) for entry in entries]))
                    if strategy == "best":
                        entry = entries[0]
                        move = entry.move()
                        print("best book move found in {} : {} , weight {}".format(book_path, move, entry.weight))
                        return move
                    if strategy == "random":
                        entry = random.choice(entries)
                        move = entry.move()
                        print("random book move found in {} : {} , weight {}".format(book_path, move, entry.weight))
                        return move                        
                    # weighted                    
                    total_weights = sum(entry.weight for entry in entries)
                    choice = random.randint(0, total_weights - 1)
                    current_sum = 0
                    for entry in entries:
                        current_sum += entry.weight
                        if current_sum > choice:
                            move = entry.move()
                            print("weighted book move found in {} : {} , total weights {} , choice {} , weight {}".format(book_path, move, total_weights, choice, entry.weight))
                            return move                        

    def get_engine_best_move(self, game, board, tc, ponderhit):
        book_best_move = self.get_book_best_move(game, board)
        if not ( book_best_move is None ):
            return book_best_move
        first = ( board.fullmove_number == 1 ) or ( len(board.move_stack) == 0 )
        print("getting engine best move, first: {}, ponderhit: {}, tc: {}".format(first, ponderhit, tc))
        gocommand = tc.gocommand()     
        positioncommand = tc.positioncommand()   
        if first:
            gocommand = "go movetime {}".format(FIRST_MOVE_TIME)
            positioncommand = "position fen {}".format(board.fen())
        if ponderhit:
            if self.cfg.ponder == "uci":
                print("uci ponderhit")
                senducis([
                    "ponderhit"
                ])
            else:
                print("naive ponderhit")
        else:
            if not ( self.ponder is None ):
                print("pondermiss on", self.ponder)
                senducis(["stop"])
                print("awaiting best move")
                bmr = False
                while not bmr:
                    sline = self.engine_queue.get()                            
                    parts = sline.split(" ")
                    kind = parts[0]        
                    if kind == "bestmove":
                        bmr = True
                print("pondermiss best move received")
            senducis([
                positioncommand,            
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
                print("best move received", parts)                
                try:
                    try:
                        move = chess.Move.from_uci(parts[1])
                        testboard = board.copy()
                        testboard.push(move)
                    except:
                        print("error parsing bestmove", parts)
                        traceback.print_exc(file = sys.stderr)
                        return None
                    try:
                        ponder = chess.Move.from_uci(parts[3])                        
                        testboard.push(move)
                    except:
                        print("error parsing ponder", parts)
                        traceback.print_exc(file = sys.stderr)
                        ponder = None                        
                    print("best move", move, "ponder", ponder)
                    pvinfos = PvInfos(infh)                   
                    if self.cfg.selectmove == "mostdrawish":
                        bestpvinfo = pvinfos.getbest(lambda pvinfo: -abs(pvinfo.score()))
                        move = bestpvinfo.bestmove                        
                        print("most drawish move", move, bestpvinfo.score())
                    elif self.cfg.selectmove == "worst":
                        bestpvinfo = pvinfos.getbest(lambda pvinfo: -pvinfo.score())
                        move = bestpvinfo.bestmove                        
                        print("worst move", move, bestpvinfo.score())
                    return (move, ponder)
                except:
                    traceback.print_exc(file = sys.stderr)
                    return None
            elif kind == "info":
                try:                    
                    eng._info(sline)
                    #print("engine thinking")
                except:
                    print("info handler error")
                    traceback.print_exc(file = sys.stderr)
        return None

    def get_capture_random_move(self, board, moves):        
        moves = sorted(moves, key = lambda move: -int(board.is_capture(move)))
        return moves[0]

    def play_move(self, game, board, tc, ponderhit):
        print("playing move", tc)
        moves = list(board.generate_legal_moves())
        if len(moves)>0:
            ponder = None
            best_move = random.choice(moves)
            if self.cfg.selectmove == "random":
                print("random best move", best_move)
            elif self.cfg.selectmove == "capturerandom":
                best_move = self.get_capture_random_move(board, moves)
                print("capture random best move", best_move)
            else:
                engine_best_move = self.get_engine_best_move(game, board, tc, ponderhit)
                if not ( engine_best_move is None ):
                    print("using engine best move", engine_best_move)
                    best_move = engine_best_move[0]
                    ponder = engine_best_move[1]
            print("making move {} in game {}".format(best_move.uci(), game.id))
            self.li.make_move(game.id, best_move)
            game.abort_in(20)
            return (best_move, ponder)
        else:
            print("! no legal move in game {}".format(game.id))
            return None

    def play_game(self, game_id):        
        self.modify_num_playing_atomic(1)
        print("playing game {}".format(game_id))
        updates = self.li.get_game_stream(game_id).iter_lines()
        game = Game(json.loads(next(updates).decode('utf-8')), self.username, self.li.baseUrl, 20)
        board = setup_board(game)    
        print(board)    
        # spawn fresh engine
        if self.cfg.needsengine():
            print(json.dumps({
                "enginecmd": "restart"
            }))        
        self.sendcorrecteducioptions(board)
        sendenginelog(False)
        empty_queue(self.engine_queue)
        moves = game.state["moves"].split()
        if is_engine_move(game, moves):                                        
            self.play_move(game, board, TimeControl(FIRST_MOVE_TIME, FIRST_MOVE_TIME, 0, 0, board), False)
        self.ponder = None
        try:
            for binary_chunk in updates:
                upd = json.loads(binary_chunk.decode('utf-8')) if binary_chunk else None
                u_type = upd["type"] if upd else "ping"
                if u_type == "chatLine":
                    pass
                elif u_type == "gameState":
                    game.state = upd
                    moves = upd["moves"].split()
                    lastmove = moves[-1]
                    board = update_board(board, lastmove)
                    if is_engine_move(game, moves):                                        
                        tc = TimeControl(upd["wtime"], upd["btime"], upd["winc"], upd["binc"], board)
                        playmove = self.play_move(game, board, tc, lastmove == self.ponder)
                        self.ponder = None
                        if not ( playmove is None ):
                            if ( not ( self.cfg.ponder == "none" ) ) and ( not ( playmove[1] is None ) ):                                
                                ponderboard = board.copy()
                                ponderboard.push(playmove[0])
                                ponderboard.push(playmove[1])
                                ponderbook = self.get_book_best_move(game, ponderboard)
                                if ponderbook is None:                                    
                                    tc.board = ponderboard
                                    self.ponder = playmove[1].uci()   
                                    print("start pondering on", self.ponder)                                    
                                    senducis([                                        
                                        tc.positioncommand(),
                                        tc.gocommand(ponder = ( self.cfg.ponder == "uci" ) )
                                    ])
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

    def challenge_supported(self, chlng):
        if ( chlng.challenger_is_bot ) and ( not ( "bot" in self.cfg.opponent ) ):
            return False
        if ( not ( chlng.challenger_is_bot ) ) and ( not ( "human" in self.cfg.opponent ) ):
            return False
        if not chlng.is_supported_speed(self.cfg.timecontrol):
            return False
        if not chlng.is_supported_variant(self.cfg.variant):
            return False
        if not chlng.is_supported_mode(self.cfg.mode):
            return False
        return True

    def log_control_event(self, event):    
        print(event)
        try:        
            kind = event["type"]
            if kind == "challenge":
                chlng = Challenge(event["challenge"])                
                if self.max_games_reached():
                    print("! max games reached, decline new {}".format(chlng))
                    self.li.decline_challenge(chlng.id)
                elif not self.challenge_supported(chlng):
                    print("! challenge not supported {}".format(chlng))
                    self.li.decline_challenge(chlng.id)
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

print(config)

bot = Bot(config)

while True:
    cmd = input("").rstrip()
    if cmd == "pc":
        print(bot.cfg)
    elif cmd == "lc":
        bot.cfg.fromfile()
        bot.createli()
    elif cmd == "lp":
        bot.loadprofile()
    elif cmd == "sc":
        bot.startcontrol()
    elif cmd == "scu":        
        bot.sendcorrecteducioptions()
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
