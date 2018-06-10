#############################################
# global imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import sys
import os
#############################################

#############################################
# local imports
from serverutils import process
from serverutils.utils import postjson
#############################################

FLASK_SERVER_URL = os.environ["FLASK_SERVER_URL"]
SIMPLE_ENGINE_PATH = os.path.join("engines", os.environ["SIMPLE_ENGINE_NAME"])
PROCESS_READ_CALLBACK_URL = FLASK_SERVER_URL + "/read"

engineprocess = None
botprocess = None

def read_line_callback(sline):
    print("engine:",sline)
    postjson(PROCESS_READ_CALLBACK_URL, {"line": sline})

def bot_read_line_callback(sline):
    print("bot:",sline)
    postjson(PROCESS_READ_CALLBACK_URL, {"botline": sline})

def startengine():
    global engineprocess    
    if engineprocess is None:
        engineprocess = process.PopenProcess(SIMPLE_ENGINE_PATH, read_line_callback)
        print("engine started")
        return("starting engine")        
    else:        
        return("engine already running")

def startbot():
    global botprocess    
    if botprocess is None:
        botprocess = process.PopenProcess(
            "python",
            bot_read_line_callback,
            proc_args = ["-u", "bot.py"],
            ignore_cwd = True
        )
        print("bot started")
        return("starting bot")        
    else:        
        return("bot already running")

def stopengine():
    global engineprocess
    if engineprocess is None:        
        return("engine already stopped")        
    else:
        #engineprocess.send_line("quit")
        engineprocess.kill()
        engineprocess = None    
        print("engine stopped")
        return("stopping engine")

def stopbot():
    global botprocess
    if botprocess is None:        
        return("bot already stopped")        
    else:        
        botprocess.kill()
        botprocess = None    
        print("bot stopped")
        return("stopping bot")

#############################################
 
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "nop"

        if self.path == "/startengine":
            message = startengine()            

        elif self.path == "/startbot":
            message = startbot()

        elif self.path == "/stopengine":
            message = stopengine()

        elif self.path == "/stopbot":
            message = stopbot()

        else:            
            if len(self.path) > 2:
                dest = self.path[1]
                line = unquote( self.path[2:] )
                if dest == "e":
                    if not ( engineprocess is None ):
                        engineprocess.send_line(line)
                        message = "sent engine: " + line
                    else:
                        message = "engine missing"
                elif dest == "b":
                    if not ( botprocess is None ):
                        botprocess.send_line(line)
                        message = "sent bot: " + line
                    else:
                        message = "bot missing"
            else:
                message = "empty command"

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
