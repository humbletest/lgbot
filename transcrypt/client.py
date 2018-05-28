######################################################
# client

######################################################
# establish submit url
if window.location.protocol == "https:":
    ws_scheme = "wss://"
else:
    ws_scheme = "ws://"

SUBMIT_URL = ws_scheme + location.host

queryParamsString = window.location.search

queryParams = {}

if len(queryParamsString) > 1:
    queryParamsString = queryParamsString[1:]
    mainparts = queryParamsString.split('&')
    for mainpart in mainparts:
        parts = mainpart.split("=")
        queryParams[parts[0]] = parts[1]
######################################################

######################################################
# app globals
socket = None
cmdinp = None
mainlog = None
maintab = None
engineconsole = None
configschema = SchemaDict({})
srcdiv = Div()
######################################################

######################################################
# client functions
def docwln(content):    
    li = LogItem("<pre>" + content + "</pre>")
    mainlog.log(li)    

def cmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"cmd", "data": cmd})

__pragma__("jsiter")

def putjsonbin(json, callback):
    args = {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "private": False
        },
        "body": json
    }
    fetch("https://api.jsonbin.io/b", args).then(
        lambda response: response.text().then(
            lambda content: callback(json, content),
            lambda err: print(err)
        ),
        lambda err: print(err)
        )

__pragma__("nojsiter")

def serializeputjsonbincallback(json, content):    
    try:
        obj = JSON.parse(content)
        id = obj["id"]        
        srcdiv.html("<pre>" + json + "</pre><hr><a href='https://api.jsonbin.io/b/"+id+"'>"+id+"</a>")
    except:
        print("there was an error parsing json", content)
        return

def serializecallback():
    json = JSON.stringify(configschema.toobj(), None, 2)    
    putjsonbin(json, serializeputjsonbincallback)
######################################################

######################################################
# app
def build():
    global cmdinp, mainlog, maintab, engineconsole

    cmdinp = TextInputWithButton({"submitcallback": cmdinpcallback})
    mainlog = Log()

    engineconsole = Div().aa([cmdinp, mainlog])    

    configdiv = Div().aa([
        Button("Serialize", serializecallback).fs(24),
        configschema
    ])

    maintabpane = TabPane({"kind":"main"})
    maintabpane.setTabs(
        [
            Tab("engineconsole", "Engine console", engineconsole),
            Tab("config", "Config", configdiv),
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

startup()

