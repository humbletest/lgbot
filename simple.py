#############################################
# global imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import sys
import os
import json
#############################################

#############################################
# local imports
from serverutils import process
from serverutils.utils import postjson, ProcessManager
#############################################

FLASK_SERVER_URL = os.environ["FLASK_SERVER_URL"]
SIMPLE_ENGINE_PATH = os.path.join("engines", os.environ["SIMPLE_ENGINE_NAME"])
PROCESS_READ_CALLBACK_URL = FLASK_SERVER_URL + "/read"

#############################################

class SimpleProcessManager(ProcessManager):
    def __init__(self, key):
        super().__init__(key)

    def read_line_callback(self, sline):
        pass

    def base_read_line_callback(self, sline):
        postjson(PROCESS_READ_CALLBACK_URL, {
            "kind": "procreadline",
            "prockey": self.key,
            "sline": sline
        })
        self.read_line_callback(sline)

class EngineProcessManager(SimpleProcessManager):
    def __init__(self, key):
        super().__init__(key)

    def popen(self):
        return process.PopenProcess(
            SIMPLE_ENGINE_PATH,
            self.base_read_line_callback
        )

class BotProcessManager(SimpleProcessManager):
    global processmanagers

    def __init__(self, key):
        super().__init__(key)

    def read_line_callback(self, sline):
        try:
            obj = json.loads(sline)
            print("bot json command")
            if "enginecmd" in obj:                
                epm = processmanagers["engine"]
                enginecmd = obj["enginecmd"]
                print("bot engine command", enginecmd)
                if enginecmd == "restart":
                    epm.stop()
                    epm.start()
        except:
            pass

    def popen(self):
        return process.PopenProcess(
            "python",
            self.base_read_line_callback,
            proc_args = ["-u", "bot.py"],
            ignore_cwd = True
        )

processmanagers = {
    "engine": EngineProcessManager("engine"),
    "bot": BotProcessManager("bot")
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

def start_server():
  print('starting server...')
 
  server_address = (sys.argv[1], int(sys.argv[2]))
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)

  print('running server on address', server_address)

  httpd.serve_forever()

#############################################

start_server()

print("server started")