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
    "start": {"display":"Start", "cmds":["r"]},
    "stop": {"display":"Stop", "cmds":["s"]},
    "restart": {"display":"Restart", "cmds":["s","r"]}
}

BOT_CMD_ALIASES = ENGINE_CMD_ALIASES
######################################################

######################################################
# app globals
socket = None
processconsoles = {
    "engine": None,
    "bot": None
}
maintabpane = None
engineconsole = None
configschema = SchemaDict({})
id = None
srcdiv = Div().ms().fs(20)
schemajson = None
######################################################

######################################################
# client functions
def showsrc():
    srcjsoncontent = JSON.stringify(serializeconfig(), None, 2)
    srcdiv.html("<pre>" + srcjsoncontent + "</pre>")
    maintabpane.selectByKey("src")

def serializeconfig():
    obj = {
        "config": configschema.topureobj(),
        "configschema": configschema.toobj()
    }
    return obj

def deserializeconfig(obj):
    global configschema
    schemaobj = {}
    if "configschema" in obj:
        schemaobj = obj["configschema"]    
    configschema = schemafromobj(schemaobj)

def buildconfigdiv():    
    global configschema
    configsplitpane = SplitPane({
        "controlheight": 50
    })
    configsplitpane.controldiv.aa([
        Button("Serialize", serializecallback).fs(24),
        Button("Show source", showsrc).fs(16)
    ]).bc("#ddd")
    configsplitpane.setcontent(configschema)
    return configsplitpane

def getbincallback(content):    
    obj = JSON.parse(content)    
    deserializeconfig(obj)
    maintabpane.setTabElementByKey("config", buildconfigdiv())

def getbinerrcallback(err):
    print("get bin failed with",err)
    loadlocal()

def loadlocal():
    document.location.href="/?id=local"

def log(content, dest = "engine"):    
    li = LogItem("<pre>" + content + "</pre>")
    processconsoles[dest].log.log(li)

def cmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"cmd", "data": cmd})

def botcmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"botcmd", "data": cmd})

def serializeputjsonbincallback(json, content):
    #print(json);return;
    try:
        obj = JSON.parse(content)        
        binid = None
        if "id" in obj:
            binid = obj["id"]                
        if "parentId" in obj:
            binid = obj["parentId"]                
        if binid is None:
            binid = "local"
        else:
            #store binid in binid.txt
            socket.emit('sioreq', {"kind":"storebinid", "data": binid})
        href = window.location.protocol + "//" + window.location.host + "/?id=" + binid        
        document.location.href = href
    except:
        print("there was an error parsing json", content)
        return

def serializecallback():
    global id, maintabpane, configschema, schemajson        
    json = JSON.stringify(serializeconfig(), None, 2)        
    putjsonbin(json, serializeputjsonbincallback, id)
######################################################

######################################################
# app
def build():
    global processconsoles, maintabpane, engineconsole

    processconsoles["engine"] = ProcessConsole({
        "cmdinpcallback": cmdinpcallback,
        "cmdaliases": ENGINE_CMD_ALIASES
    })

    processconsoles["bot"] = ProcessConsole({
        "cmdinpcallback": botcmdinpcallback,
        "cmdaliases": BOT_CMD_ALIASES
    })

    maintabpane = TabPane({"kind":"main"})
    maintabpane.setTabs(
        [
            Tab("engineconsole", "Engine console", processconsoles["engine"]),
            Tab("botconsole", "Bot console", processconsoles["bot"]),
            Tab("config", "Config", buildconfigdiv()),
            Tab("src", "Src", srcdiv),
            Tab("about", "About", Div().ac("appabout").html("Flask hello world app."))
        ], "config"
    )    
    
    ge("maintabdiv").innerHTML = ""
    ge("maintabdiv").appendChild(maintabpane.e)
######################################################

######################################################
# socket handler
def onconnect():    
    log("socket connected ok")    
    socket.emit('sioreq', {"data": "socket connected"})

def onevent(json):
    dest = "engine"
    if "botline" in json:
        dest = "bot"
    if "response" in json:
        response = json["response"]
        if "kind" in response:
            kind = response["kind"]
            if kind == "ackbotcmd":
                dest = "bot"
    log("socket received event " + JSON.stringify(json, null, 2), dest)    

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
    getjsonbin(id, getbincallback, getbinerrcallback)
else:
    loadlocal()

startup()
