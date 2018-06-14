import json

import sys, traceback

from serverutils.utils import read_string_from_file
from serverutils.utils import getjsonbin, getjsonbinobj

from lbot.lichess import Lichess
from lbot.model import Challenge, Game

import threading

import chess
from chess.variant import find_variant

import random

#########################################################

VERSION = "1.0.0"
LICHESS_API_BASE_URL = "https://lichess.org/"

#########################################################

def getbinid():
    binid = read_string_from_file("binid.txt", "")
    if binid == "":
        return None
    return binid

configobj = {}

configname = None

config = {}

li = None

MAX_NUM_PLAYING = 1

lock = threading.Lock()

num_playing = 0

username = "!nouser"

controlstarted = False

def gettoken():
    return config.get("token", "xxxxxxxxxxxxxxxx")

#########################################################

def modify_num_playing_atomic(delta):
    global num_playing, lock
    lock.acquire()
    num_playing += delta
    lock.release()

def max_games_reached():
    global num_playing, MAX_NUM_PLAYING
    return num_playing >= MAX_NUM_PLAYING

def loadconfig():
    global configobj, configname, config
    binid = getbinid()
    if not ( binid is None ):            
        try:
            obj = getjsonbinobj(binid)
            configobj = obj["config"]
            configname = configobj[0]
            config = configobj[1]
            print("config {} loaded ok".format(configname))            
        except:
            print("! loading config failed")
    else:
        print("! missing binid")

def printconfig():
    print("printing config")
    formatted = json.dumps(configobj)
    print(formatted)
    print("config printed")

def loadprofile():    
    global username
    try:
        print("loading profile")
        profile = li.get_profile()
        username = profile["username"]
        print("profile loaded for {}".format(username))
        #print(profile)
    except:
        print("! loading profile failed")
        traceback.print_exc(file=sys.stderr)

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

def play_move(game, board):
    moves = list(board.generate_legal_moves())
    if len(moves)>0:
        best_move = random.choice(moves)
        print("making move {} in game {}".format(best_move.uci(), game.id))
        li.make_move(game.id, best_move)
        game.abort_in(20)
    else:
        print("! no legal move in game {}".format(game.id))

def play_game(game_id):    
    modify_num_playing_atomic(1)
    print("playing game {}".format(game_id))
    updates = li.get_game_stream(game_id).iter_lines()
    game = Game(json.loads(next(updates).decode('utf-8')), username, li.baseUrl, 20)
    board = setup_board(game)    
    print(board)
    moves = game.state["moves"].split()
    if is_engine_move(game, moves):                                        
        play_move(game, board)    
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
                    play_move(game, board)
            elif u_type == "ping":
                if game.should_abort_now():
                    print("aborting {} by lack of activity".format(game.url()))
                    li.abort(game.id)
    except (RemoteDisconnected, ChunkedEncodingError, ConnectionError, ProtocolError, HTTPError) as exception:
        print("! abandoning game due to connection error")
        traceback.print_exception(type(exception), exception, exception.__traceback__)
    finally:
        print("game over {}".format(game.url()))
        modify_num_playing_atomic(-1)

def log_control_event(event):    
    print(event)
    try:        
        kind = event["type"]
        if kind == "challenge":
            chlng = Challenge(event["challenge"])
            if max_games_reached():
                print("! max games reached, decline new {}".format(chlng))
            else:
                try:
                    response = li.accept_challenge(chlng.id)
                    print("accept {}".format(chlng))                
                except HTTPError as exception:
                    if exception.response.status_code == 404: # ignore missing challenge
                        print("skip missing {}".format(chlng))
                    else:
                        raise exception
        elif kind == "gameStart":            
            game_id = event["game"]["id"]            
            if max_games_reached():
                print("! max games reached, decline new game {}".format(game_id))
            else:
                threading.Thread(target = play_game, args = (game_id,)).start()
    except:
        print("! error handling event")
        traceback.print_exc(file = sys.stderr)

"""
@backoff.on_exception(backoff.expo, BaseException, max_time=600)
"""
def control_thread_func():
    global num_playing
    print("starting control stream")    
    try:
        es = li.get_event_stream()
        print("event stream created")
        for evnt in es.iter_lines():
            if evnt:
                event = json.loads(evnt.decode('utf-8'))
                log_control_event(event)
            else:
                log_control_event({"type": "ping", "num_playing": num_playing})
    except:
        print("! failed to get event stream")        

def startcontrol():
    global controlstarted
    if controlstarted:
        print("! control stream already started")
    else:        
        threading.Thread(target = control_thread_func).start()
        controlstarted = True

def createli():
    global li
    token = gettoken()
    print("creating lichess api agent", token, LICHESS_API_BASE_URL, VERSION)
    li = Lichess(token, LICHESS_API_BASE_URL, VERSION)
    print("lichess api agent created")
    print("testing lichess api agent")
    loadprofile()

#########################################################

while True:
    cmd = input("").rstrip()
    if cmd == "lc":
        loadconfig()
        printconfig()
        createli()
    elif cmd == "lp":
        loadprofile()
    elif cmd == "sc":
        startcontrol()
    else:
        print("echo", cmd)
