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
from serverutils.utils import get_variant_board
import chess
from chess.pgn import read_game
from cbuild.book import get_zobrist_key_hex
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
import io
import uuid

print("importing pyrebase")
import pyrebase
print("initializing firebase")
try:    
    fbcreds = json.loads(open("firebase/fbcreds.json").read())
    firebase = pyrebase.initialize_app(fbcreds)
    db = firebase.database()
    dbstorage = firebase.storage()
    print("initializing firebase done")
except:
    print("initializing firebase failed")
print("getting stored config")
try:    
    storedconfig = db.child("lichguibotconfig").get().val()    
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
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['DOWNLOAD_FOLDER'] = 'download'
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

def getchildatpath(path):
    try:
        parts = path.split("/")
        child = db.child(parts[0])
        if len(parts) > 1:
            for part in parts:
                child  = child.child(part)
        return child
    except:
        #traceback.print_exc(file=sys.stderr)
        return None

def storedb(path, dataobj):
    try:
        child = getchildatpath(path)
        if not ( child is None ):
            child.set(json.dumps(dataobj))
            return "store db ok at {}".format(path)
    except:
        #traceback.print_exc(file=sys.stderr)
        pass
    return "store db failed at {}".format(path)

def retrievedb(path):
    try:
        child = getchildatpath(path)
        if not ( child is None ):
            val = child.get().val()
            obj = json.loads(val)
            return ( obj , "retrieve db ok at {} size {}".format(path, len(json.dumps(obj))) )
    except:
        #traceback.print_exc(file=sys.stderr)
        pass
    return ( None , "retrieve db failed at {}".format(path) )

def addpositioninfo(board, obj, genmove = None, genboard = None):
    moves = board.generate_legal_moves()
    movelist = []
    for move in moves:
        movelist.append({
            "uci": move.uci(),
            "san": board.san(move)
        })
    obj["positioninfo"] = {
        "movelist": movelist,
        "zobristkeyhex": get_zobrist_key_hex(board)
    }
    if genmove == "reset":
        obj["positioninfo"]["genmove"] = "reset"
    elif not ( genmove is None ):        
        obj["positioninfo"]["genmove"] = {
            "uci": genmove.uci(),
            "san": genboard.san(genmove)
        }

def createhistory(pgn):
    historyobj = None
    try:    
        pgnio = io.StringIO(pgn)
        game = read_game(pgnio)
        board = game.board()
        positioninfos = []
        pinfo = {
            "fen": board.fen()
        }
        addpositioninfo(board, pinfo)
        positioninfos.append(pinfo)
        for move in game.main_line():
            genboard = board.copy()
            board.push(move)
            pinfo = {
                "fen": board.fen()
            }
            addpositioninfo(board, pinfo, move, genboard)
            positioninfos.append(pinfo)
        historyobj = {            
            "positioninfos": positioninfos,
            "pgn": pgn,
            "uci_variant": board.uci_variant,
            "chess960": board.chess960
        }
        return ( historyobj , "game history created ok" )
    except:
        traceback.print_exc(file=sys.stderr)
        return ( None , "! create game history failed" )

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
                    if "owner" in jsonobj:
                        rjsonobj["owner"] = jsonobj["owner"]
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
                            db.child("lichguibotconfig").set(jsonobj["data"])
                            print("setting config on firebase done")            
                            rjsonobj["status"] = "config stored locally and remotely"
                        except:                            
                            print("setting config on firebase failed")
                            rjsonobj["status"] = "config stored only locally"
                    elif kind == "storedb":
                        try:
                            path = jsonobj["path"]
                            dataobj = jsonobj["dataobj"]                                                                                    
                            rjsonobj["status"] = storedb(path, dataobj)
                            rjsonobj["path"] = path                            
                        except:                            
                            traceback.print_exc(file=sys.stderr)
                            rjsonobj["status"] = "! store db failed at {}".format(path)
                    elif kind == "retrievedb":
                        try:
                            path = jsonobj["path"]
                            rjsonobj["dataobj"] , rjsonobj["status"] = retrievedb(path)
                            rjsonobj["path"] = path                            
                        except:                            
                            traceback.print_exc(file=sys.stderr)
                            rjsonobj["dataobj"] = None
                            rjsonobj["status"] = "! retrieve db failed at {}".format(path)
                    elif kind == "parsepgn":
                        rjsonobj["historyobj"] = None
                        try:
                            data = jsonobj["data"]
                            rjsonobj["historyobj"] , rjsonobj["status"] = createhistory(data)
                        except:                            
                            traceback.print_exc(file=sys.stderr)                            
                            rjsonobj["status"] = "! parse pgn failed"
                    elif kind == "getlocalconfig":
                        rjsonobj["kind"] = "setlocalconfig"
                        try:
                            print("getting config from firebase")
                            rjsonobj["data"] = db.child("lichguibotconfig").get().val()
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
                                genboard = board.copy()
                                board.push(move)
                                rjsonobj["kind"] = "setmainboardfen"
                                rjsonobj["fen"] = board.fen()
                                rjsonobj["status"] = "making main board move ok"
                                addpositioninfo(board, rjsonobj, move, genboard)
                            else:
                                rjsonobj["kind"] = "setmainboardfen"
                                rjsonobj["fen"] = fen
                                rjsonobj["status"] = "! making main board move failed, illegal move"                                
                                addpositioninfo(board, rjsonobj)
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
                            addpositioninfo(board, rjsonobj, "reset")
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

@app.route("/upload", methods = ["POST"])
def upload():
    if 'files' not in request.files:            
        return Response(json.dumps({
            "success": False,
            "status": "no file input"
        }), content_type = "application/json")
    file = request.files['files']
    if file:            
        filename = file.filename
        parts = filename.split(".")            
        savefilename = uuid.uuid1().hex + "." + parts[-1]            
        savepath = os.path.join(app.config['UPLOAD_FOLDER'], savefilename)
        file.save(savepath)            
        dbstorage.child("upload").child(savefilename).put(savepath)
        return Response(json.dumps({
            "success": True,
            "filename": filename,
            "savefilename": savefilename
        }), content_type = "application/json")

@app.route("/file/<path:path>")
def serve_static_file(path):
    parts = path.split("/")
    basedir = parts[0]
    if basedir in CONFIDENTIAL_DIRS:
        return "sorry, {} directory content is confidential".format(basedir)
    return send_from_directory('.', path)

@app.route("/uploads/<path:path>")
def serve_uploaded_file(path):        
    filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], path)    
    dbstorage.child("upload").child(path).download(filepath)
    return send_from_directory('.', "download/{}".format(path))

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
