import json

from serverutils.utils import read_string_from_file
from serverutils.utils import getjsonbin, getjsonbinobj

from lbot.lichess import Lichess

#########################################################

VERSION = "1.0.0"
LICHESS_API_BASE_URL = "https://lichess.org/"

#########################################################

def getbinid():
    binid = read_string_from_file("binid.txt", "")
    if binid == "":
        return None
    return binid

configobj = {}

configname = None

config = {}

li = None

def gettoken():
    return config.get("token","xxxxxxxxxxxxxxxx")

#########################################################

def loadconfig():
    global configobj, configname, config
    binid = getbinid()
    if not ( binid is None ):            
        try:
            obj = getjsonbinobj(binid)
            configobj = obj["config"]
            configname = configobj[0]
            config = configobj[1]
            print("config {} loaded ok".format(configname))            
        except:
            print("! loading config failed")
    else:
        print("! missing binid")

def printconfig():
    print("printing config")
    formatted = json.dumps(configobj)
    print(formatted)
    print("config printed")

def loadprofile():    
    try:
        print("loading profile")
        profile = li.get_profile()
        print("profile loaded")
        print(profile)
    except:
        print("! loading profile failed")

def createli():
    global li
    token = gettoken()
    print("creating lichess api agent", token, LICHESS_API_BASE_URL, VERSION)
    li = Lichess(token, LICHESS_API_BASE_URL, VERSION)
    print("lichess api agent created")
    print("testing lichess api agent")
    loadprofile()

#########################################################

while True:
    cmd = input("").rstrip()
    if cmd == "lc":
        loadconfig()
        printconfig()
        createli()
    elif cmd == "lp":
        loadprofile()
    else:
        print("echo", cmd)
