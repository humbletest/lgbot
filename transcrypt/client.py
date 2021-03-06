######################################################
# client

######################################################
# establish submit url
if window.location.protocol == "https:":
    ws_scheme = "wss://"
else:
    ws_scheme = "ws://"

SUBMIT_URL = ws_scheme + window.location.host

queryparamsstring = window.location.search

queryparams = {}

if len(queryparamsstring) > 1:
    queryparamsstring = queryparamsstring[1:]
    mainparts = queryparamsstring.split('&')
    for mainpart in mainparts:
        parts = mainpart.split("=")
        queryparams[parts[0]] = parts[1]
######################################################

######################################################
# app consts

ENGINE_CMD_ALIASES = {
    "start": {"display":"R", "cmds":["r"]},
    "stop": {"display":"S", "cmds":["s"]},
    "parseuci": {"display":"Parse UCI options", "cmds":["r", "parseuci"]},
    "d15": {"display":"d15", "cmds":["go depth 15"]}
}

BOT_CMD_ALIASES = {
    "start": {"display":"R", "cmds":["r"]},
    "stop": {"display":"S", "cmds":["s"]},    
    "loadconfig": {"display":"LC", "cmds":["s", "r"]}
}

CBUILD_CMD_ALIASES = {    
    "stop": {"display":"S", "cmds":["s"]},    
    "example": {"display":"example build", "cmds":["-e antichess --variant antichess --nextlichessdb -a"]},
    "help": {"display":"help", "cmds":["-h"]}    
}
######################################################

######################################################
# app globals
socket = None
processconsoles = {
    "engine": None,
    "bot": None,
    "cbuild": None
}
mainlogpane = None
maintabpane = None
mainboard = None
configschema = SchemaDict({})
srcdiv = Div().ms().fs(20)
schemajson = None
######################################################

######################################################
# client functions
def getlocalconfig():
    global socket
    socket.emit('sioreq', {"kind":"getlocalconfig"})

def showsrc():
    srcjsoncontent = JSON.stringify(serializeconfig(), None, 2)
    srcdiv.html("<pre>" + srcjsoncontent + "</pre>")
    maintabpane.selectByKey("src")

def serializeconfig():
    global configschema
    obj = {
        "config": configschema.topureobj(),
        "configschema": configschema.toobj()
    }    
    return obj

def deserializeconfig(obj):
    global configschema
    schemaobj = {}
    try:        
        if "configschema" in obj:
            schemaobj = obj["configschema"]
        configschema = schemafromobj(schemaobj)
    except:
        print("deserialize config obj failed for", obj)

def deserializeconfigcontent(content):
    global maintabpane
    try:
        obj = JSON.parse(content)    
        deserializeconfig(obj)        
    except:
        print("deserializing config content failed for", content)
    maintabpane.setTabElementByKey("config", buildconfigdiv())

def buildconfigdiv():    
    global configschema
    configsplitpane = SplitPane({
        "controlheight": 50
    })
    configsplitpane.controldiv.aa([
        Button("Serialize", serializecallback).fs(24),
        Button("Reload", reloadcallback).fs(16),
        Button("Show source", showsrc).fs(16)
    ]).bc("#ddd")
    configschemacontainerdiv = Div().ac("configschemacontainerdiv").a(configschema)
    configsplitpane.setcontent(configschemacontainerdiv)
    return configsplitpane

def getbincallback(content):    
    deserializeconfigcontent(content)    

def getbinerrcallback(err):
    print("get bin failed with", err)    

def mainlog(logitem):
    global mainlogpane
    mainlogpane.log.log(logitem)

def log(content, dest = "engine"):    
    li = LogItem("<pre>" + content + "</pre>")
    processconsoles[dest].log.log(li)

def cmdinpcallback(cmd, key):    
    global socket
    socket.emit('sioreq', {"kind":"cmd", "key": key, "data": cmd})

def serializeputjsonbincallback(content):
    global socket
    try:
        obj = JSON.parse(content)        
        binid = "local"
        if "id" in obj:
            binid = obj["id"]                
        elif "parentId" in obj:
            binid = obj["parentId"]
        if not ( binid == "local" ):
            socket.emit('sioreq', {"kind":"storebinid", "data": binid})
        href = window.location.protocol + "//" + window.location.host + "/?id=" + binid        
        document.location.href = href
    except:
        print("there was an error parsing json", content)        
        return

def serializeputjsonbinerrcallback(err):
    print("there was an error putting to json bin", err)    

def serializecallback():
    global socket
    json = JSON.stringify(serializeconfig(), None, 2)        
    socket.emit('sioreq', {"kind":"storeconfig", "data": json})    

def reloadcallback():
    document.location.href = "/"

def mainboardmovecallback(variantkey, fen, moveuci):
    global socket
    setTimeout(lambda ev: socket.emit('sioreq', {"kind":"mainboardmove", "variantkey":variantkey, "fen":fen, "moveuci":moveuci}), simulateserverlag())

def mainboardvariantchangedcallback(variantkey):
    global socket
    setTimeout(lambda ev: socket.emit('sioreq', {"kind":"mainboardsetvariant", "variantkey":variantkey}), simulateserverlag())

def mainboardmoveclickedcallback(variantkey, fen, moveuci):
    global socket
    setTimeout(lambda ev: socket.emit('sioreq', {"kind":"mainboardmove", "variantkey":variantkey, "fen":fen, "moveuci":moveuci}), simulateserverlag())

def mainboardenginecommandcallback(sline):
    global socket
    socket.emit('sioreq', {"kind":"cmd", "key": "engine", "data": sline})
######################################################

######################################################
# app
def build():
    global processconsoles, maintabpane, mainlogpane, mainboard, socket

    processconsoles["engine"] = ProcessConsole({
        "key": "engine",
        "cmdinpcallback": cmdinpcallback,
        "cmdaliases": ENGINE_CMD_ALIASES
    })

    processconsoles["bot"] = ProcessConsole({
        "key": "bot",
        "cmdinpcallback": cmdinpcallback,
        "cmdaliases": BOT_CMD_ALIASES
    })

    processconsoles["cbuild"] = ProcessConsole({
        "key": "cbuild",
        "cmdinpcallback": cmdinpcallback,
        "cmdaliases": CBUILD_CMD_ALIASES
    })

    mainlogpane = LogPane()

    mainboard = Board({
        "movecallback": mainboardmovecallback,
        "variantchangedcallback": mainboardvariantchangedcallback,
        "moveclickedcallback": mainboardmoveclickedcallback,
        "enginecommandcallback": mainboardenginecommandcallback,
        "socket": socket
    })

    maintabpane = TabPane({"kind":"main", "id":"main"}).setTabs(
        [
            Tab("engineconsole", "Engine console", processconsoles["engine"]),
            Tab("botconsole", "Bot console", processconsoles["bot"]),
            Tab("cbuildconsole", "Cbuild console", processconsoles["cbuild"]),
            Tab("upload", "Upload", FileUploader({
                "url": "/upload"
            })),
            Tab("dirbrowser", "Dirbrowser", DirBrowser()),
            Tab("board", "Board", mainboard),
            Tab("config", "Config", buildconfigdiv()),
            Tab("log", "Log", mainlogpane),
            Tab("src", "Src", srcdiv),
            Tab("about", "About", Div().ac("appabout").html("Lichess GUI bot."))
        ], "botconsole"
    )    
    
    ge("maintabdiv").innerHTML = ""
    ge("maintabdiv").appendChild(maintabpane.e)
######################################################

######################################################
# socket handler
def onconnect():    
    global socket
    mainlog(LogItem("socket connected ok", "cmdstatusok"))
    socket.emit('sioreq', {"data": "socket connected"})    
    getlocalconfig()
    socket.emit('sioreq', {"kind":"mainboardsetvariant", "variantkey":"standard"})

def onevent(json):    
    global configschema, mainboard
    dest = None
    logitem = None    
    if "kind" in json:
        kind = json["kind"]
        if kind == "procreadline":
            dest = json["prockey"]
            sline = json["sline"]
            logitem = LogItem(sline, "cmdreadline")
            if dest == "bot":
                if len(sline)>0:
                    if sline[0] == "!":
                        logitem = LogItem("bot error:" + sline[1:], "cmdstatuserr")        
        elif kind == "ucioptionsparsed":
            ucioptionsobj = json["ucioptions"]
            ucischema = schemafromucioptionsobj(ucioptionsobj)
            selfprofile = getpathfromschema(configschema, "profile/#")
            if selfprofile is None:
                window.alert("Warning: no profile selected to store UCI options.")                
            else:
                selfprofile.setchildatkey("ucioptions", ucischema)
                maintabpane.setTabElementByKey("config", buildconfigdiv())
                maintabpane.selectByKey("config")
                window.alert("UCI options stored in current profile.")
        elif kind == "analysisinfo":
            mainboard.processanalysisinfo(json["analysisinfo"])
    if "response" in json:        
        status = "?"
        response = json["response"]        
        if "key" in response:
            dest = response["key"]
        if "status" in response:
            status = response["status"]
            logitem = LogItem(status, "cmdstatusok")
            if len(status)>0:
                if status[0] == "!":
                    logitem = LogItem(status, "cmdstatuserr")
        if "kind" in response:            
            kind = response["kind"]
            if kind == "setlocalconfig":                
                data = response["data"]                
                deserializeconfigcontent(data)
                mainboard.setconfigschema(configschema)
            elif kind == "configstored":                
                window.alert("Config storing status: " + status + ".")            
                mainboard.setconfigschema(configschema)
            elif kind == "setmainboardfen":                
                fen = response["fen"]
                positioninfo = response["positioninfo"]                
                mainboard.setfromfen(fen, positioninfo)
        if "owner" in response:
            owner = response["owner"]
            if owner == "board":
                mainboard.siores(response)
    if ( logitem is None ) or ( dest is None ):
        jsonstr = JSON.stringify(json, null, 2)
        mainlog(LogItem(jsonstr))
    else:
        processconsoles[dest].log.log(logitem)

def windowresizehandler():
    maintabpane.resize()
######################################################

######################################################
# startup

console.log("creating socket for submit url [ {} ]".format(SUBMIT_URL))

socket = io.connect(SUBMIT_URL)

console.log("socket created ok")

build()

socket.on('connect', onconnect)
socket.on('siores', lambda json: onevent(json))

addEventListener(window, "resize", windowresizehandler)

######################################################