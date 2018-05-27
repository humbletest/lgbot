######################################################
# client

######################################################
# establish submit url
if window.location.protocol == "https:":
    ws_scheme = "wss://"
else:
    ws_scheme = "ws://"

SUBMIT_URL = ws_scheme + location.host
######################################################

######################################################
# app globals
socket = None
cmdinp = None
mainlog = None
maintab = None
engineconsole = None
configschema = None
######################################################

######################################################
# client functions
def docwln(content):    
    li = LogItem("<pre>" + content + "</pre>")
    mainlog.log(li)    

def cmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"cmd", "data": cmd})
######################################################

######################################################
# app
def build():
    global cmdinp, mainlog, maintab, engineconsole

    cmdinp = TextInputWithButton({"submitcallback": cmdinpcallback})
    mainlog = Log()

    engineconsole = Div().aa([cmdinp, mainlog])    

    configschema = SchemaCollection({})

    maintabpane = TabPane({"kind":"main"})
    maintabpane.setTabs(
        [
            Tab("engineconsole", "Engine console", engineconsole),
            Tab("config", "Config", configschema),
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

