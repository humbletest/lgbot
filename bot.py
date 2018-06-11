import json

from serverutils.utils import read_string_from_file
from serverutils.utils import getjsonbin, getjsonbinobj

def getbinid():
    binid = read_string_from_file("binid.txt", "")
    if binid == "":
        return None
    return binid

config = {}

def loadconfig():
    global config
    binid = getbinid()
    if not ( binid is None ):            
        try:
            obj = getjsonbinobj(binid)
            config = obj["config"]
            print("config loaded ok")
        except:
            print("loading config failed")
    else:
        print("missing binid")

def printconfig():
    print("printing config")
    formatted = json.dumps(config, indent = 2)
    print(formatted)
    print("config printed")

print("bot started")
while True:
    cmd = input("").rstrip()
    if cmd == "lc":
        loadconfig()
        printconfig()
    else:
        print("echo", cmd)
