import threading
import inspect
import certifi
import urllib3
import json
import os, stat

#############################################

import chess
from chess.variant import find_variant

#############################################

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

JSONBIN_APIBASEURL = "https://api.jsonbin.io"

def geturl(url):
    print("get url", url)
    r = http.request("GET", url)
    content = r.data.decode("utf-8")
    return content

def postjson(url, obj):
    #print("post json", url, obj)
    try:
        r = http.request('POST', url, headers={'Content-Type': 'application/json'}, body=json.dumps(obj))
        content = r.data.decode("utf-8")
        return content
    except:
        return None

def getjsonbin(id, version = "latest"):
    url = JSONBIN_APIBASEURL + "/b/" + id + "/" + version
    print("get jsonbin", url)
    r = http.request("GET", url, headers = {
        "Content-Type": "application/json",
        "private": False
    })
    content = r.data.decode("utf-8")
    return content

def getjsonbinobj(id, version = "latest"):
    content = getjsonbin(id, version)
    obj = json.loads(content)
    return obj

#############################################

lock = threading.Lock()

SEP = "-" * 60

class SafeLimitedUniqueQueueList:
    def __init__(self, max = 10, overflow_callback = None):
        self.items = []
        self.max = max
        self.overflow_callback = overflow_callback
    def enqueue(self, item):
        if item in self.items:
            return
        lock.acquire()        
        self.items = [ item ] + self.items
        if len(self.items) > self.max:
            removed_item = self.items.pop()
            if not ( self.overflow_callback is None ):
                self.overflow_callback(removed_item)
        lock.release()
    def dequeue(self):
        if len(self.items) == 0:
            return None
        lock.acquire() 
        item = self.items.pop()
        lock.release()
        return item

def prettylog(lines):
    print(SEP)
    for line in lines:
        print("- " + line)
    print(SEP)

#############################################
# file utils

def write_string_to_file(path, str, force = True):
	if os.path.isfile(path) and not force:
		return
	with open(path,"w") as outfile:
		outfile.write(str)
	print("written file {} ( {} characters )".format(path,len(str)))

def read_string_from_file(path, default):
	try:
		content = open(path).read()
		return content
	except:
		return default

def os_stats_as_dict(stats, name, isdir):
    return {
        "name": name,
        "isdir": isdir,
        "st_mode": stats.st_mode,
        "st_mode_unix_rwx": stat.filemode(stats.st_mode),
        "st_ino": stats.st_ino,
        "st_dev": stats.st_dev,
        "st_nlink": stats.st_nlink,
        "st_uid": stats.st_uid,
        "st_gid": stats.st_gid,
        "st_size": stats.st_size,
        "st_atime": stats.st_atime,
        "st_mtime": stats.st_mtime,
        "st_ctime": stats.st_ctime
    }

def dir_listing_as_obj(path):
    return [os_stats_as_dict(os.stat(os.path.join(path, name)), name, os.path.isdir(os.path.join(path, name))) for name in os.listdir(path)]

#############################################

MATE_SCORE = 10000
MATE_LIMIT = MATE_SCORE * 0.9

def get_score_numerical(score):
    cp = score[0]
    mate = score[1]
    if cp == None:
        if mate > 0:
            return MATE_SCORE - mate
        else:
            return -MATE_SCORE - mate
    if cp > MATE_LIMIT:
        cp = MATE_LIMIT
    elif cp < (-MATE_LIMIT):
        cp = (-MATE_LIMIT)
    return cp

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

#############################################

class ProcessManager:
    def __init__(self, key):
        self.key = key
        self.process = None
        self.sendlog = True

    def send_line_task(self, sline):
        self.process.send_line(sline)

    def send_line(self, sline):
        if self.process is None:
            msg = "! no {} process to send line".format(self.key)
            #print(msg)
            return msg
        else:
            self.send_line_task(sline)
            msg = "line sent to {} process : {}".format(self.key, sline)
            #print(msg)
            return msg

    def popen(self):
        return None

    def start(self):
        if self.process is None:
            self.process = self.popen()
            msg = "{} - started".format(self.key)
            print(msg)
            return msg
        else:
            msg = "! {} - already running".format(self.key)
            print(msg)
            return msg

    def stop(self):
        if self.process is None:            
            msg = "! {} - already stopped".format(self.key)
            print(msg)
            return msg
        else:
            self.process.kill()
            self.process = None
            msg = "{} - stopped".format(self.key)
            print(msg)
            return msg

#############################################
