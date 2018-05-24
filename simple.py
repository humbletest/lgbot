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

bp = None

def read_line_callback(sline):
    print(sline)
    postjson(PROCESS_READ_CALLBACK_URL, {"line": sline})

def startengine():
    global bp    
    if bp is None:
        bp = process.PopenProcess(SIMPLE_ENGINE_PATH, read_line_callback)
        print("engine started")
        return("starting engine")        
    else:        
        return("engine already running")

def stopengine():
    global bp
    if bp is None:        
        return("engine already stopped")        
    else:
        #bp.send_line("quit")
        bp.kill()
        bp = None    
        print("engine stopped")
        return("stopping engine")

#############################################
 
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "nop"

        if self.path == "/r":
            message = startengine()            

        elif self.path == "/s":
            message = stopengine()

        else:
            if not ( bp is None ):
                if len(self.path) > 1:
                    line = unquote( self.path[1:] )
                    bp.send_line(line)
                    message = "sent: " + line
                else:
                    message = "empty command"
            else:
                message = "engine missing"

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
