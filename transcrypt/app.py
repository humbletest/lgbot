######################################################
# dom
def ce(tag):
    return document.createElement(tag)

def ge(id):
    return document.getElementById(id)

class e:
    def __init__(self, tag):
        self.e = ce(tag)

    # append element
    def a(self, e):
        self.e.appendChild(e.e)
        return self

    # append list of elements
    def aa(self, es):
        for e in es:
            self.a(e)
        return self

    # shorthand for setAttribute
    def sa(self, key, value):
        self.e.setAttribute(key,value)
        return self

    # shorthand for setting value
    def sv(self, value):
        self.e.value = value
        return self

    # set inner html
    def h(self, value):
        self.e.innerHTML = value
        return self

    def x(self):
        self.h("")
        return self

    # add class
    def ac(self, klass):
        self.sa("class",klass)
        return self

    # return value
    def v(self):
        return self.e.value

    def focusme(self):                
        self.e.focus()
        return self

    # focus later
    def fl(self):                
        setTimeout(self.focusme, 50)
        return self

    # add event listener
    def ae(self, kind, callback):
        self.e.addEventListener(kind, callback)
        return self

class Div(e):
    def __init__(self):
        super().__init__("div")

class Span(e):
    def __init__(self):
        super().__init__("span")

class Input(e):
    def __init__(self, kind):
        super().__init__("input")
        self.sa("type",kind)
######################################################

######################################################
# widgets
class Button(Input):
    def __init__(self, caption, callback = None):
        super().__init__("button")        
        self.sv(caption)
        if not ( callback is None):
            self.ae("mousedown",callback)

class Text(Input):
    def keyup(self, ev):
        if not ( self.callback is None):
            if ev.keyCode == 13:
                self.callback(self.v())

    def __init__(self, callback = None):
        super().__init__("text")
        self.callback = callback
        if not ( callback is None ):
            self.ae("keyup",self.keyup)

class TextInput(e):
    def submit_callback(self):
        if not ( self.callback is None ):
            v = self.tinp.v()
            self.tinp.sv("")
            self.callback(v)

    def __init__(self, callback):
        super().__init__("div")
        self.callback = callback
        self.tinp = Text(self.submit_callback).ac("textinputtext")
        sbtn = Button("Submit",self.submit_callback).ac("textinputbutton")
        self.aa([self.tinp,sbtn])

    def focus(self):
        self.tinp.fl()
        return self

class LogItem(e):
    def __init__(self, content, kind = "normal"):
        super().__init__("div")
        tdiv = Div().ac("logtimediv").h("{}".format(__new__ (Date()).toLocaleString()))
        cdiv = Div().ac("logcontentdiv").h(content)
        idiv = Div().ac("logitemdiv").aa([tdiv,cdiv])
        idiv.aa([tdiv,cdiv])
        self.a(idiv)

class Log(e):
    def __init__(self, maxitems = 25):        
        super().__init__("div")
        self.ldiv = Div().ac("logdiv")
        self.maxitems = maxitems
        self.items = []
        self.a(self.ldiv)

    def build(self):
        self.ldiv.x()
        for item in reversed(self.items):
            self.ldiv.a(item)

    def add(self, item):
        self.items.append(item)        
        if len(self.items) > self.maxitems:
            self.items = self.items[1:]

    def log(self, item):
        self.add(item)
        self.build()
######################################################

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

