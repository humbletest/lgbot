######################################################
# client

######################################################
# establish submit url
if window.location.protocol == "https:":
    ws_scheme = "wss://"
else:
    ws_scheme = "ws://"

SUBMIT_URL = ws_scheme + location.host

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
    "uci": {"display":"uci", "cmds":["uci"]},
    "d15": {"display":"d15", "cmds":["go depth 15"]}
}

BOT_CMD_ALIASES = {
    "start": {"display":"R", "cmds":["r"]},
    "stop": {"display":"S", "cmds":["s"]},    
    "loadconfig": {"display":"LC", "cmds":["s", "r", "lc", "sc"]}
}
######################################################

######################################################
# app globals
socket = None
processconsoles = {
    "engine": None,
    "bot": None
}
maintabpane = None
configschema = SchemaDict({})
id = None
srcdiv = Div().ms().fs(20)
schemajson = None
######################################################

######################################################
# client functions
def getlocalconfig():
    global socket
    socket.emit('sioreq', {"kind":"getlocalconfig"})

def loadlocal():
    document.location.href="/?id=local"

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
    loadlocal()

def log(content, dest = "engine"):    
    li = LogItem("<pre>" + content + "</pre>")
    processconsoles[dest].log.log(li)

def cmdinpcallback(cmd, key):    
    global socket
    socket.emit('sioreq', {"kind":"cmd", "key": key, "data": cmd})

def serializeputjsonbincallback(content):
    global socket
    #print(json);return;
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
        loadlocal()
        return

def serializeputjsonbinerrcallback(err):
    print("there was an error putting to json bin", err)
    loadlocal()

def serializecallback():
    global id, socket
    json = JSON.stringify(serializeconfig(), None, 2)        
    socket.emit('sioreq', {"kind":"storeconfig", "data": json})
    #putjsonbin(json, id, serializeputjsonbincallback, serializeputjsonbinerrcallback)

def reloadcallback():
    document.location.href = "/"
######################################################

######################################################
# app
def build():
    global processconsoles, maintabpane

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

    maintabpane = TabPane({"kind":"main", "id":"main"})
    maintabpane.setTabs(
        [
            Tab("engineconsole", "Engine console", processconsoles["engine"]),
            Tab("botconsole", "Bot console", processconsoles["bot"]),
            Tab("config", "Config", buildconfigdiv()),
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
    log("socket connected ok")    
    socket.emit('sioreq', {"data": "socket connected"})
    if id == "local":
        getlocalconfig()

def onevent(json):    
    global configschema
    dest = "engine"
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
            if not ( selfprofile is None ):
                selfprofile.setchildatkey("ucioptions", ucischema)
                maintabpane.setTabElementByKey("config", buildconfigdiv())
                maintabpane.selectByKey("config")
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
            elif kind == "configstored":
                window.alert("Config storing status: " + status + ".")
    if logitem is None:
        log("socket received event " + JSON.stringify(json, null, 2), dest)    
    else:
        processconsoles[dest].log.log(logitem)

def windowresizehandler():
    maintabpane.resize()

def startup():
    global socket

    log("creating socket for submit url [ " + SUBMIT_URL + " ]")

    socket = io.connect(SUBMIT_URL)

    log("socket created ok")

    socket.on('connect', onconnect)
    socket.on('siores', lambda json: onevent(json))

    addEventListener(window, "resize", windowresizehandler)
######################################################

build()

if "id" in queryparams:    
    id = queryparams["id"]
    if not ( id == "local" ):
        #getjsonbin(id, getbincallback, getbinerrcallback)
        loadlocal()
else:
    loadlocal()

startup()
