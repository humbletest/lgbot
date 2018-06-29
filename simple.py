from config import config

#############################################
# global imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import sys
import os
import json
import threading
import time
#############################################

#############################################
# local imports
from serverutils import process
process.VERBOSE = False
from serverutils.utils import postjson, ProcessManager
from chess.uci import Engine
#############################################

def SIMPLE_ENGINE_PATH():
    config.fromfile()
    return os.path.join("engines", config.enginename)

FLASK_SERVER_URL = config.flaskserverurl
PROCESS_READ_CALLBACK_URL = FLASK_SERVER_URL + "/read"

#############################################

class SimpleProcessManager(ProcessManager):
    def __init__(self, key):
        super().__init__(key)

    def read_line_callback(self, sline):
        pass

    def base_read_line_callback(self, sline):
        if self.sendlog:
            postjson(PROCESS_READ_CALLBACK_URL, {
                "kind": "procreadline",
                "prockey": self.key,
                "sline": sline
            })
        self.read_line_callback(sline)

class EngineProcessManager(SimpleProcessManager):
    global processmanagers

    def __init__(self, key):
        super().__init__(key)    
        self.parseuci = False        
        self.sendparseuci = False

    def send_line_task(self, sline):     
        if sline == "parseuci":
            sline = "uci"
            self.sendparseuci = True
        if sline == "uci":
            print("parsing uci command output")
            self.eng = Engine()
            self.parseuci = True   
        self.process.send_line(sline)            

    def read_line_callback(self, sline):
        if self.parseuci:
            command_and_args = sline.split(None, 1)
            if len(command_and_args)>=1:
                if command_and_args[0] == "uciok":
                    self.parseuci = False
                    print("uci command output parsed")
                    optsobj = []
                    for key in self.eng.options:
                        opt = self.eng.options[key]
                        optsobj.append({
                            "key": opt[0],
                            "kind": opt[1],
                            "default": opt[2],
                            "min": opt[3],
                            "max": opt[4],
                            "options": opt[5]
                        })
                    print("opts", optsobj)
                    if self.sendparseuci:
                        self.sendparseuci = False
                        postjson(PROCESS_READ_CALLBACK_URL, {
                            "kind": "ucioptionsparsed",
                            "ucioptions": optsobj
                        })                    
                else:
                    if len(command_and_args)>=2:
                        if command_and_args[0] == "option":
                            self.eng._option(command_and_args[1])
        bpm = processmanagers["bot"]
        obj = {
            "engineline": sline
        }
        bpm.send_line(json.dumps(obj))

    def popen(self):
        return process.PopenProcess(
            SIMPLE_ENGINE_PATH(),
            self.base_read_line_callback
        )

class BotProcessManager(SimpleProcessManager):
    global processmanagers

    def __init__(self, key):
        super().__init__(key)

    def read_line_callback(self, sline):
        try:
            obj = json.loads(sline)
            #print("bot json command")
            if "enginecmd" in obj:                
                epm = processmanagers["engine"]
                enginecmd = obj["enginecmd"]
                #print("bot engine command", enginecmd)                
                if enginecmd == "restart":
                    epm.stop()
                    epm.start()
                elif enginecmd == "ucis":                    
                    ucis = obj["ucis"]
                    #print("sending engine", ucis)
                    for uci in ucis:
                        epm.send_line(uci)
                elif enginecmd == "enginelog":
                    value = obj["value"]
                    epm.sendlog = value
                    
        except:
            pass

    def popen(self):
        return process.PopenProcess(
            "python",
            self.base_read_line_callback,
            proc_args = ["-u", "bot.py"],
            ignore_cwd = True
        )

class CbuildProcessManager(SimpleProcessManager):
    global processmanagers

    def __init__(self, key):
        super().__init__(key)

    def read_line_callback(self, sline):
        pass

    def start(self):
        msg = "start not supported on one off process"
        print(msg)
        return msg

    def stop(self):
        msg = "stop not supported on one off process"
        print(msg)
        return msg

    def popen(self):
        return process.PopenProcess(
            "python",
            self.base_read_line_callback,
            proc_args = ["cbuild.py"],
            ignore_cwd = True
        )

    def send_line(self, sline):
        args = sline.split(" ")
        process.PopenProcess(
            "python",
            self.base_read_line_callback,
            proc_args = ["cbuild.py"] +  args,
            ignore_cwd = True
        )
        return ""

processmanagers = {
    "engine": EngineProcessManager("engine"),
    "bot": BotProcessManager("bot"),
    "cbuild": CbuildProcessManager("cbuild")
}

#############################################
 
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        global processmanagers

        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "! no command"        

        if len(self.path) > 1:
            commandstr = unquote(self.path[1:])
            print("commandstr", commandstr)
            try:
                commandobj = None            
                commandobj = json.loads(commandstr)                
                try:
                    command = commandobj.get("command", None)
                    key = commandobj.get("key", None)
                    if command == "r":
                        message = processmanagers[key].start()
                    elif command == "s":
                        message = processmanagers[key].stop()
                    else:                        
                        message = processmanagers[key].send_line(command)                
                except:
                    message = "! command error"                
            except:
                message = "! command parse error"

        print("status", message)

        self.wfile.write(bytes(message, "utf8"))

#############################################

def scheduler_thread_func(processmanagers):
    delay = config.autostartbot * 2
    if delay > 0:
        print("waiting {} seconds to start bot".format(delay))
        time.sleep(delay)
        print("auto starting bot")
        processmanagers["bot"].start()
    else:
        print("auto start bot disabled")

print("starting scheduler...")
threading.Thread(target = scheduler_thread_func, args = (processmanagers,)).start()

def start_server():
  print('starting server...')
 
  server_address = (sys.argv[1], int(sys.argv[2]))
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)

  print('running server on address', server_address)

  httpd.serve_forever()

#############################################

start_server()

print("server started")