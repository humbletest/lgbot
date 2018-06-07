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
# app globals
socket = None
cmdinp = None
mainlog = None
maintabpane = None
engineconsole = None
configschema = SchemaDict({})
id = None

def buildconfigdiv():    
    global configschema
    configdiv = Div().aa([
        Button("Serialize", serializecallback).fs(24),
        configschema
    ])
    return configdiv

def getbincallback(content):
    global configschema    
    obj = JSON.parse(content)    
    configschema = schemafromobj(obj)        
    configschema.openchilds()
    maintabpane.setTabElementByKey("config", buildconfigdiv())

def getbinerrcallback(err):
    print("get bin failed with",err)
    loadlocal()

srcdiv = Div()
schemajson = None
######################################################

######################################################
# client functions
def loadlocal():
    document.location.href="/?id=local"

def docwln(content):    
    li = LogItem("<pre>" + content + "</pre>")
    mainlog.log(li)    

def cmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"cmd", "data": cmd})

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
        print("href", href)
        document.location.href = href
    except:
        print("there was an error parsing json", content)
        return

def serializecallback():
    global id, maintabpane, configschema, schemajson        
    schemajson = JSON.stringify(configschema.toobj(), None, 2)        
    putjsonbin(schemajson, serializeputjsonbincallback, id)
######################################################

######################################################
# app
def build():
    global cmdinp, mainlog, maintabpane, engineconsole

    cmdinp = TextInputWithButton({"submitcallback": cmdinpcallback})
    mainlog = Log()

    engineconsole = Div().aa([cmdinp, mainlog])    

    maintabpane = TabPane({"kind":"main"})
    maintabpane.setTabs(
        [
            Tab("engineconsole", "Engine console", engineconsole),
            Tab("config", "Config", buildconfigdiv()),            
            Tab("about", "About", Div().ac("appabout").html("Flask hello world app."))
        ], "config"
    )    
    
    ge("maintabdiv").innerHTML = ""
    ge("maintabdiv").appendChild(maintabpane.e)
######################################################

######################################################
# socket handler
def onconnect():    
    docwln("socket connected ok")    
    socket.emit('sioreq', {"data": "socket connected"})

def onevent(json):
    docwln("socket received event " + JSON.stringify(json, null, 2))    

def windowresizehandler():
    build()

def startup():
    global socket

    docwln("creating socket for submit url [ " + SUBMIT_URL + " ]")

    socket = io.connect(SUBMIT_URL)

    docwln("socket created ok")

    cmdinp.focus()

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

