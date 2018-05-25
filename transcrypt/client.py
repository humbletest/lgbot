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

def docwln(content):    
    li = LogItem("<pre>" + content + "</pre>")
    mainlog.log(li)    

__pragma__("jsiter")

document.querySelector("#content").innerHTML = "Flask hello world"

def cmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"cmd", "data": cmd})

cmdinp = TextInput(cmdinpcallback)
mainlog = Log()

ge("cmddiv").appendChild(cmdinp.e)
ge("logdiv").appendChild(mainlog.e)

maintab = TabPane()
#ge("tabdiv").appendChild(maintab.e)

docwln("creating socket for submit url [ " + SUBMIT_URL + " ]")

socket = io.connect(SUBMIT_URL)

docwln("socket created ok")

cmdinp.focus()

def onconnect():    
    docwln("socket connected ok")    
    socket.emit('sioreq', {"data": "socket connected"})

def onevent(json):
    docwln("socket received event " + JSON.stringify(json, null, 2))    

socket.on('connect', onconnect)
socket.on('siores', lambda json: onevent(json))

######################################################

