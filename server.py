from config import config

#########################################################
# flask imports
from flask import Flask, Response, render_template, request, redirect, send_from_directory
#########################################################

#########################################################
# flask socketio imports
from flask_socketio import SocketIO, emit
#########################################################

#########################################################
# local imports
from serverutils.utils import SafeLimitedUniqueQueueList
from serverutils.utils import prettylog
from serverutils.utils import geturl
from serverutils.utils import write_string_to_file
from serverutils.utils import read_string_from_file
from serverutils.utils import dir_listing_as_obj
import chess
from chess.variant import find_variant
#########################################################

#########################################################
# global imports
import time
import os
import sys
import traceback
from urllib.parse import quote
import random
import json
import functools

print("importing pyrebase")
import pyrebase
print("initializing firebase")
try:    
    fbcreds = json.loads(open("firebase/fbcreds.json").read())
    firebase = pyrebase.initialize_app(fbcreds)
    db = firebase.database()
    print("initializing firebase done")
except:
    print("initializing firebase failed")
print("getting stored config")
try:    
    storedconfig = db.child("lgbotconfig").get().val()    
    write_string_to_file("localconfig.json", storedconfig)
    print("getting stored config done, size", len(storedconfig))
except:
    print("getting stored config failed")
    #traceback.print_exc(file=sys.stderr)
print("importing pyrebase done")
#########################################################

#########################################################
# create app
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
#########################################################

#########################################################
# mount socket
socketio = SocketIO(app)
#########################################################

#########################################################
# global context
SIMPLE_SERVER_URL = config.simpleserverurl
MAX_CONNS = 3
CONFIDENTIAL_DIRS = [
    "firebase",
    ".git"
]

def sids_overflow_callback(sid):    
    socketio.emit("siores", {"data": "conn removed"}, room = sid)
    prettylog([
        "removed SID <{}>".format(sid)
    ])

connected_sids = SafeLimitedUniqueQueueList(max = MAX_CONNS, overflow_callback = sids_overflow_callback)

class AppState:
    def __init__(self):
        pass

app_state = AppState()

def my_broadcast(obj):
    with app.app_context():        
        for sid in connected_sids.items:
            try:                
                socketio.emit("siores", obj, room = sid, namespace = "/")
            except:
                print("emit failed for sid {}".format(sid))

def get_variant_board(variantkey):
    if variantkey == "standard":
        return chess.Board()
    elif variantkey == "chess960":
        return chess.Board(chess960=True)
    elif variantkey == "fromPosition":
        return chess.Board()
    else:
        VariantBoard = find_variant(variantkey)
        return VariantBoard()

class socket_handler:
    def __init__(self, ev):
        self.ev = ev
    
    def __call__(self, f):
        def wrapped_f(*args):
            jsonobj = args[0]
            rjsonobj = {}
            connected_sids.enqueue(request.sid)
            prettylog([
                "EV <{}> SID <{}>".format(self.ev,request.sid),
                "ARGS {}".format(args).ljust(160)[:160],
                "CONNS {}".format(connected_sids.items)
            ])  
            if "kind" in jsonobj:                
                try:          
                    kind = jsonobj["kind"]
                    if kind == "cmd":    
                        key = jsonobj["key"]
                        commandjsonstr = json.dumps({"command": jsonobj["data"], "key": key})                        
                        rjsonobj["status"] = geturl(SIMPLE_SERVER_URL + "/" + quote(commandjsonstr))                
                        rjsonobj["key"] = key
                    elif kind == "storebinid":
                        binid = jsonobj["data"]
                        write_string_to_file("binid.txt", binid)
                    elif kind == "storeconfig":
                        write_string_to_file("localconfig.json", jsonobj["data"])
                        rjsonobj["kind"] = "configstored"
                        try:
                            print("setting config on firebase")
                            db.child("lgbotconfig").set(jsonobj["data"])
                            print("setting config on firebase done")            
                            rjsonobj["status"] = "config stored locally and remotely"
                        except:                            
                            print("setting config on firebase failed")
                            rjsonobj["status"] = "config stored only locally"
                    elif kind == "getlocalconfig":
                        rjsonobj["kind"] = "setlocalconfig"
                        try:
                            print("getting config from firebase")
                            rjsonobj["data"] = db.child("lgbotconfig").get().val()
                            write_string_to_file("localconfig.json", rjsonobj["data"])
                            print("getting config from firebase done, size", len(rjsonobj["data"]))
                        except:
                            print("getting config from firebase failed, falling back to local config")
                            rjsonobj["data"] = read_string_from_file("localconfig.json", "{}")
                    elif kind == "mainboardmove":                        
                        try:                          
                            variantkey = jsonobj["variantkey"]
                            fen = jsonobj["fen"]
                            moveuci = jsonobj["moveuci"]
                            move = chess.Move.from_uci(moveuci)
                            board = get_variant_board(variantkey)
                            board.set_fen(fen)
                            if board.is_legal(move):
                                board.push(move)
                                rjsonobj["kind"] = "setmainboardfen"
                                rjsonobj["fen"] = board.fen()
                                rjsonobj["status"] = "making main board move ok"
                            else:
                                rjsonobj["kind"] = "setmainboardfen"
                                rjsonobj["fen"] = fen
                                rjsonobj["status"] = "! making main board move failed, illegal move"                                
                        except:
                            rjsonobj["status"] = "! making main board move failed, fatal"
                            traceback.print_exc(file=sys.stderr)
                    elif kind == "mainboardsetvariant":   
                        try:    
                            variantkey = jsonobj["variantkey"]   
                            board = get_variant_board(variantkey)              
                            if variantkey == "chess960":
                                board.set_chess960_pos(random.randint(0, 959))
                            rjsonobj["kind"] = "setmainboardfen"
                            rjsonobj["fen"] = board.fen()
                            rjsonobj["status"] = "main board variant selected ok"
                        except:
                            rjsonobj["status"] = "! main board variant selection failed"
                            traceback.print_exc(file=sys.stderr)
                except:
                    rjsonobj["status"] = "! command error"

            emit('siores', {"request": jsonobj, "response": rjsonobj})
            f(*args)
        return wrapped_f
#########################################################

def randurl():
    return random.randint(1e9,1e10)

#########################################################
# app routes
@app.route("/")
def index():
    print("request root", request.full_path)
    return render_template("index.html", randurl = randurl)

@app.route("/read", methods = ["POST"])
def read():
    obj = request.get_json()
    my_broadcast(obj)
    return ""

@app.route("/file/<path:path>")
def serve_static_envs(path):
    parts = path.split("/")
    basedir = parts[0]
    if basedir in CONFIDENTIAL_DIRS:
        return "sorry, {} directory content is confidential".format(basedir)
    return send_from_directory('.', path)

@app.route("/dirlist/<path:path>")
def dirlist_of_path(path):
    path = functools.reduce(os.path.join, path.split("/")[1:], ".")
    return Response(json.dumps(dir_listing_as_obj(path)), content_type = "application/json")
#########################################################

#########################################################
# socketio event handlers
@socketio.on('sioreq')
@socket_handler('sioreq')
def handle_sioreq(json):
    pass
#########################################################

#########################################################
# startup
def startup(port = 5000):
    socketio.run(app, port = port)
#########################################################
    
#########################################################
# main
if __name__ == '__main__':    
    #startup()
    pass
#########################################################
