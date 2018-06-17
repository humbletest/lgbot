#########################################################
# flask imports
from flask import Flask, render_template, request, redirect
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
#########################################################

#########################################################
# global imports
import time
import os
import traceback
from urllib.parse import quote
import random
import json
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
    traceback.print_exc(file=sys.stderr)
print("importing pyrebase done")
#########################################################

#########################################################
# create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#########################################################

#########################################################
# mount socket
socketio = SocketIO(app)
#########################################################

#########################################################
# global context
SIMPLE_SERVER_URL = os.environ["SIMPLE_SERVER_URL"]
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
                "ARGS {}".format(args),
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
                        try:
                            print("setting config on firebase")
                            db.child("lgbotconfig").set(jsonobj["data"])
                            print("setting config on firebase done")
                        except:
                            print("setting config on firebase failed")
                    elif kind == "getlocalconfig":
                        rjsonobj["kind"] = "setlocalconfig"
                        try:
                            print("getting config from firebase")
                            rjsonobj["data"] = db.child("lgbotconfig").get().val()
                            print("getting config from firebase done")
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
