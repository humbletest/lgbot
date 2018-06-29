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
    #db.child("lgbotconfig").set(read_string_from_file("configbackup.json","{}"))
    storedconfig = db.child("lgbotconfig").get().val()    
    write_string_to_file("localconfig.json", storedconfig)
    print("getting stored config done, size", len(storedconfig))
except:
    print("getting stored config failed")
    traceback.print_exc(file=sys.stderr)
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
def hello():
    print("request root", request.full_path)
    if request.full_path == "/?":
        binid = read_string_from_file("binid.txt", "local")
        # use local anyway ( comment this out to get stored binid )
        binid = "local"
        rurl = "/?id=" + binid
        print("redirecting root to", rurl)
        return redirect(rurl)
    return render_template("index.html", randurl = randurl)

@app.route("/read", methods = ["POST"])
def read():
    obj = request.get_json()
    my_broadcast(obj)
    return ""

@app.route("/file/<path:path>")
def serve_static_envs(path):
    parts = path.split("/")
    if parts[0] == "firebase":
        return "sorry, firebase directory content is confidential"
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
