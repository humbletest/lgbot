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
import traceback
#############################################

#############################################
# local imports
from serverutils import process
process.VERBOSE = False
from serverutils.utils import postjson, ProcessManager
from serverutils.utils import get_variant_board
from serverutils.utils import get_score_numerical
import chess
from chess.uci import InfoHandler, Engine
from cbuild.book import get_zobrist_key_hex
#############################################

def SIMPLE_ENGINE_PATH():
    config.fromfile()
    return os.path.join("engines", config.enginename)

FLASK_SERVER_URL = config.flaskserverurl
PROCESS_READ_CALLBACK_URL = FLASK_SERVER_URL + "/read"

MAX_PV_LENGTH = 6

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
        self.analyze = False

    def send_line_task(self, sline):     
        if sline == "parseuci":
            sline = "uci"
            self.sendparseuci = True
        elif sline == "uci":
            print("parsing uci command output")
            self.eng = Engine()
            self.parseuci = True   
        elif sline == "stopanalyze":
            self.process.send_line("stop")            
            self.analyze = False
            self.sendlog = True
            return
        else:
            parts = sline.split(" ")
            if parts[0] == "analyze":
                try:
                    config.fromfile()
                    variantkey = parts[1]
                    multipv = parts[2]
                    fen = " ".join(parts[3:])
                    print("analyzing", variantkey, fen)
                    self.board = get_variant_board(variantkey)
                    self.board.set_fen(fen)
                    self.eng = Engine()
                    self.eng.board = self.board
                    self.infh = InfoHandler()    
                    self.eng.info_handlers.append(self.infh)
                    self.process.send_line("stop")            
                    for ucioption in config.ucioptions:
                        self.process.send_line("setoption name {} value {}".format(ucioption.name, ucioption.value))    
                    self.process.send_line("setoption name MultiPV value {}".format(multipv))
                    self.process.send_line("setoption name UCI_Variant value {}".format(type(self.board).uci_variant))
                    self.process.send_line("position fen {}".format(fen))
                    self.process.send_line("go infinite")            
                    self.analyze = True
                    self.sendlog = False
                    self.analyzestarted = time.time()
                    return
                except:
                    print("there was a problem with analyze command", sline)
                    traceback.print_exc(file=sys.stderr)                        
        self.process.send_line(sline)            

    def read_line_callback(self, sline):
        if self.analyze:
            parts = sline.split(" ")
            kind = parts[0]               
            if kind == "info":
                try:                    
                    self.eng._info(sline)                    
                except:
                    print("info handler error", sline)
                    traceback.print_exc(file = sys.stderr)                    
                    return                        
            now = time.time()
            if ( now - self.analyzestarted ) > 0.5:
                analysisinfo = {
                    "zobristkeyhex": get_zobrist_key_hex(self.board),
                    "pvitems": []
                }
                info = self.infh.info
                firstdepth = None
                depthsequal = True
                for i , score in info["score"].items():                    
                    pvsan = None
                    bestmovesan = None                    
                    pvuci = None                    
                    bestmoveuci = None                    
                    pvpgn = None
                    try:
                        pvi = info["pv"][i]
                        sans = []
                        pgnsans = []
                        ucis = []
                        sanboard = self.board.copy()
                        mcnt = 0
                        for move in pvi:
                            san = sanboard.san(move)
                            sans.append(san)
                            ucis.append(move.uci())
                            if mcnt < MAX_PV_LENGTH:
                                pref = ""                                
                                if mcnt == 0:
                                    dot = ""                                    
                                    if sanboard.turn == chess.BLACK:
                                        dot = "."
                                    pref = "{}.{}".format(sanboard.fullmove_number, dot)
                                elif sanboard.turn == chess.WHITE:
                                    pref = "{}.".format(sanboard.fullmove_number)
                                if not ( pref == "" ):
                                    pgnsans.append(pref)
                                pgnsans.append(san)
                            sanboard.push(move)                            
                            mcnt += 1                            
                        if len(sans) > MAX_PV_LENGTH:
                            sans = sans[:MAX_PV_LENGTH]
                            ucis = ucis[:MAX_PV_LENGTH]
                        pvsan = " ".join(sans)
                        bestmovesan = sans[0]
                        pvuci = " ".join(ucis)                        
                        bestmoveuci = ucis[0]
                        pvpgn = " ".join(pgnsans)
                    except:
                        traceback.print_exc(file=sys.stderr)                        
                        pass
                    depthi = info["depths"][i]
                    if firstdepth is None:
                        firstdepth = depthi
                    else:
                        if not ( depthi == firstdepth ):
                            depthsequal = False
                    npsi = info["npss"][i]
                    analysisinfo["pvitems"].append({
                        "i": i,
                        "score": score,
                        "pvsan": pvsan,
                        "pvpgn": pvpgn,
                        "bestmovesan": bestmovesan,
                        "pvuci": pvuci,
                        "bestmoveuci": bestmoveuci,
                        "scorenumerical": get_score_numerical(score),
                        "depth": depthi,
                        "nodes": info["nodes"],
                        "nps": npsi
                    })
                if depthsequal or config.analysisdepth == "partial":
                    postjson(PROCESS_READ_CALLBACK_URL, {
                        "kind": "analysisinfo",
                        "prockey": self.key,
                        "analysisinfo": analysisinfo
                    })
                    self.analyzestarted = now                
            return
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
        return self.send_line("-h")

    def terminated_callback(self):
        print("cbuild terminated")
        self.process = None

    def send_line(self, sline):
        if self.process is None:
            args = sline.split(" ")
            self.process = process.PopenProcess(
                "python",
                self.base_read_line_callback,
                proc_args = ["-u", "cbuild.py"] +  args,
                ignore_cwd = True,
                terminated_callback = self.terminated_callback
            )
            msg = "cbuild started"
            print(msg)
            return msg
        else:
            msg = "cbuild already running"
            print(msg)
            return msg

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

def bot_scheduler_thread_func(processmanagers):
    delay = config.autostartbot
    if delay > 0:
        print("waiting {} seconds to start bot".format(delay))
        time.sleep(delay)
        print("auto starting bot")
        processmanagers["bot"].start()
    else:
        print("auto start bot disabled")

def engine_scheduler_thread_func(processmanagers):
    delay = config.autostartengine
    if delay > 0:
        print("waiting {} seconds to start engine".format(delay))
        time.sleep(delay)
        print("auto starting engine")
        processmanagers["engine"].start()
    else:
        print("auto start engine disabled")

print("starting scheduler...")
threading.Thread(target = bot_scheduler_thread_func, args = (processmanagers,)).start()
threading.Thread(target = engine_scheduler_thread_func, args = (processmanagers,)).start()

def start_server():
  print('starting server...')
 
  server_address = (sys.argv[1], int(sys.argv[2]))
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)

  print('running server on address', server_address)

  httpd.serve_forever()

#############################################

start_server()

print("server started")
