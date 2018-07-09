MAX_CONTENT_LENGTH = 1000
MAX_LINE_LENGTH = 500

MATE_SCORE = 10000
MATE_LIMIT = MATE_SCORE * 0.9
WINNING_MOVE_LIMIT = 1000
DOUBLE_EXCLAM_LIMIT = 500
EXCLAM_LIMIT = 350
PROMISING_LIMIT = 250
INTERESTING_LIMIT = 150
DRAWISH_LIMIT = 80

def scorecolor(score):
    if score > MATE_LIMIT:
        return "#0f0"
    if score > WINNING_MOVE_LIMIT:
        return "#0e0"
    if score > DOUBLE_EXCLAM_LIMIT:
        return "#0c0"
    if score > EXCLAM_LIMIT:
        return "#0a0"
    if score > PROMISING_LIMIT:
        return "#090"
    if score > INTERESTING_LIMIT:
        return "#070"
    if score > DRAWISH_LIMIT:
        return "#050"
    if score > 0:
        return "#033"
    if score > (-DRAWISH_LIMIT):
        return "#330"
    if score > (-INTERESTING_LIMIT):
        return "#500"
    if score > (-PROMISING_LIMIT):
        return "#900"
    if score > (-EXCLAM_LIMIT):
        return "#a00"
    if score > (-DOUBLE_EXCLAM_LIMIT):
        return "#c00"
    if score > WINNING_MOVE_LIMIT:
        return "#e00"
    return "#f00"

class View:
    def __init__(self, callback, value = None):
        self.callback = callback
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.callback()

def xor(b1, b2):
    if b1 and b2:
        return False
    if b1 or b2:
        return True
    return False

def cpick(cond, vtrue, vfalse):
    if cond:
        return vtrue
    return vfalse

def simulateserverlag(range = 1000, min_lag = 10):    
    if "localhost" in window.location.host:
        return int(min_lag + Math.random() * range)
    return min_lag

def choose(cond, choicetrue, choicefalse):
    if cond:
        return choicetrue
    return choicefalse

class Vect:
    def __init__(self, x, y):
        try:
            self.x = float(x)
            self.y = float(y)
        except:
            self.x = 0.0
            self.y = 0.0
            print("vect init failed on", x, y)

    def p(self, v):
        return Vect(self.x + v.x, self.y + v.y)

    def s(self, s):
        return Vect(self.x * s, self.y * s)

    def m(self, v):
        return self.p(v.s(-1))
    
    def copy(self):
        return Vect(self.x, self.y)

    def __repr__(self):
        return "Vect[x: {}, y: {}]".format(self.x, self.y)

def getClientVect(ev):
    return Vect(ev.clientX, ev.clientY)

def getglobalcssvar(key):
    return getComputedStyle(window.document.documentElement).getPropertyValue(key)

def getglobalcssvarpxint(key, default):
    try:
        px = getglobalcssvar(key)
        pxint = int(px.replace("px",""))
        return pxint
    except:
        return default

def striplonglines(content, maxlen = MAX_LINE_LENGTH):
    lines = content.split("\n")    
    strippedlines = []
    for line in lines:        
        if len(line) > maxlen:   
            sline = "{} ... [ truncated {} characters ]".format(line.substring(0,maxlen), len(line) - maxlen)
            strippedlines.append(sline)
        else:
            strippedlines.append(line)
    content = "\n".join(strippedlines)    
    return content

# https://stackoverflow.com/questions/13382516/getting-scroll-bar-width-using-javascript
def getScrollBarWidth():
    outer = document.createElement("div")
    outer.style.visibility = "hidden"
    outer.style.width = "100px"
    outer.style.msOverflowStyle = "scrollbar" # needed for WinJS apps

    document.body.appendChild(outer)

    widthNoScroll = outer.offsetWidth
    # force scrollbars
    outer.style.overflow = "scroll"

    # add innerdiv
    inner = document.createElement("div")
    inner.style.width = "100%"
    outer.appendChild(inner)       

    widthWithScroll = inner.offsetWidth

    # remove divs
    outer.parentNode.removeChild(outer)

    return widthNoScroll - widthWithScroll

def randint(range):
    return int(Math.random()*range)

def randscalarvalue(baselen, pluslen):
    len = baselen + randint(pluslen)
    buff = ""
    for i in range(len):
        if (i % 2) == 1:        
            buff += ["a", "e", "i", "o", "u"][randint(5)]
        else:
            buff += ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"][randint(21)]
    return buff

def uid():
    uid = randscalarvalue(8, 0)
    return uid

def getfromobj(obj, key, default):
    if key in obj:
        return obj[key]    
    return default    

def patchclasses(selfref, args):
    items = args.get("patchclasses", [])
    for item in items:
        parts = item.split("/")
        membername = parts[0]
        action = parts[1]
        classname = parts[2]
        if action == "a":
            selfref[membername].ac(classname)
        elif action == "r":
            selfref[membername].rc(classname)

def parsejson(jsonstr, callback, errcallback):
    try:
        obj = JSON.parse(jsonstr)
        callback(obj)
    except:
        errcallback("error parsing json")

__pragma__("jsiter")

def putjsonbin(json, id, callback, errcallback):

    method = "POST"
    url = "https://api.jsonbin.io/b"        

    if id == "local":
        pass
    elif not ( id is None ):
        url = url + "/" + id        
        method = "PUT"    
    
    args = {
        "method": method,
        "headers": {
            "Content-Type": "application/json",
            "private": False
        },
        "body": json
    }        
    
    fetch(url, args).then(
        lambda response: response.text().then(
            lambda content: callback(content),
            lambda err: errcallback(err)
        ),
        lambda err: errcallback(err)
    )

def getjsonbin(id, callback, errcallback, version = "latest"):

    args = {
        "method": "GET",
        "headers": {
            "Content-Type": "application/json",
            "private": False
        }
    }

    fetch("https://api.jsonbin.io/b/" + id + "/" + version, args).then(
        lambda response: response.text().then(
            lambda content: callback(content),
            lambda err: errcalback(err)
        ),
        lambda err: errcallback(err)
    )

def getjson(path, callback, errcallback):

    args = {
        "method": "GET",
        "headers": {
            "Content-Type": "application/json"
        }
    }

    fetch(path, args).then(
        lambda response: response.text().then(
            lambda content: parsejson(content, callback, errcallback),
            lambda err: errcalback(err)
        ),
        lambda err: errcallback(err)
    )

__pragma__("nojsiter")
######################################################
# dom
SCROLL_BAR_WIDTH = getScrollBarWidth()

def ce(tag):
    return document.createElement(tag)

def ge(id):
    return document.getElementById(id)

def addEventListener(object, kind, callback):
    object.addEventListener(kind, callback, False)

class e:
    def __init__(self, tag):
        self.e = ce(tag)

    # background color
    def bc(self, color):
        self.e.style.backgroundColor = color
        return self

    # cursor pointer
    def cp(self):
        self.e.style.cursor = "pointer"
        return self

    # conditional background color
    def cbc(self, cond, colortrue, colorfalse):
        self.e.style.backgroundColor = cpick(cond, colortrue, colorfalse)
        return self

    # color
    def c(self, color):
        self.e.style.color = color
        return self
    
    # conditional color
    def cc(self, cond, colortrue, colorfalse):
        self.e.style.color = cpick(cond, colortrue, colorfalse)
        return self

    # z-index
    def zi(self, zindex):
        self.e.style.zIndex = zindex
        return self

    # opacity
    def op(self, opacity):
        self.e.style.opacity = opacity
        return self

    # monospace
    def ms(self):
        self.e.style.fontFamily = "monospace"
        return self

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

    # shorthand for removeAttribute
    def ra(self, key):
        self.e.removeAttribute(key)
        return self

    # shorthand for getAttribute
    def ga(self, key):
        return self.e.getAttribute(key)

    # shorthand for setting value
    def sv(self, value):
        self.e.value = value
        return self

    # set inner html
    def html(self, value):
        self.e.innerHTML = value
        return self

    # clear
    def x(self):
        #self.html("")
        while self.e.firstChild:
            self.e.removeChild(self.e.firstChild)
        return self

    # width
    def w(self, w):
        self.e.style.width = w + "px"
        return self

    def mw(self, w):
        self.e.style.minWidth = w + "px"
        return self

    # height
    def h(self, h):
        self.e.style.height = h + "px"
        return self

    def mh(self, h):
        self.e.style.minHeight = h + "px"
        return self

    # top
    def t(self, t):
        self.e.style.top = t + "px"
        return self

    # left
    def l(self, l):
        self.e.style.left = l + "px"
        return self

    # conditional left
    def cl(self, cond, ltrue, lfalse):
        self.e.style.left = cpick(cond, ltrue, lfalse) + "px"
        return self

    # conditional top
    def ct(self, cond, ttrue, tfalse):
        self.e.style.top = cpick(cond, ttrue, tfalse) + "px"
        return self

    # position vector
    def pv(self, v):
        return self.l(v.x).t(v.y)

    # position absolute
    def pa(self):
        self.e.style.position = "absolute"
        return self

    # position relative
    def pr(self):
        self.e.style.position = "relative"
        return self

    # margin left
    def ml(self, ml):
        self.e.style.marginLeft = ml + "px"
        return self

    # margin right
    def mr(self, mr):
        self.e.style.marginRight = mr + "px"
        return self

    # margin top
    def mt(self, mt):
        self.e.style.marginTop = mt + "px"
        return self

    # margin bottom
    def mb(self, mb):
        self.e.style.marginBottom = mb + "px"
        return self

    # add class
    def ac(self, klass):
        self.e.classList.add(klass)
        return self

    # add classes
    def aac(self, klasses):
        for klass in klasses:
            self.e.classList.add(klass)
        return self

    # remove class
    def rc(self, klass):
        self.e.classList.remove(klass)
        return self

    # add or remove class based on condition
    def arc(self, cond, klass):
        if cond:
            self.e.classList.add(klass)
        else:
            self.e.classList.remove(klass)
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

    # disable
    def disable(self):
        return self.sa("disabled", True)

    # enable
    def enable(self):
        return self.ra("disabled")

    # able
    def able(self, able):
        if able:
            return self.enable()
        return self.disable()

    # font size
    def fs(self, size):
        self.e.style.fontSize = size + "px"
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
        self.sa("type", kind)

class Select(e):
    def __init__(self):
        super().__init__("select")

class Option(e):
    def __init__(self, key, displayname, selected = False):
        super().__init__("option")
        self.sa("name", key)
        self.sa("id", key)
        self.sv(key)
        self.html(displayname)
        if selected:
            self.sa("selected", True)

class Slider(Input):
    def setmin(self, min):
        self.sa("min", min)
        return self

    def setmax(self, max):
        self.sa("max", max)
        return self

    def __init__(self):
        super().__init__("range")

class CheckBox(Input):
    def setchecked(self, checked):
        self.e.checked = checked
        return self

    def getchecked(self):
        return self.e.checked

    def __init__(self, checked = False):
        super().__init__("checkbox")
        self.setchecked(checked)

class TextArea(e):
    def __init__(self):
        super().__init__("textarea")

    def setText(self, content):
        self.sv(content)
        return self

    def getText(self):
        return self.v()

class Canvas(e):
    def __init__(self, width, height):
        super().__init__("canvas")
        self.width = width
        self.height = height
        self.sa("width", self.width)
        self.sa("height", self.height)        
        self.ctx = self.e.getContext("2d")

    def lineWidth(self, linewidth):        
        self.ctx.lineWidth = linewidth

    def strokeStyle(self, strokestyle):        
        self.ctx.strokeStyle = strokestyle

    def fillStyle(self, fillstyle):        
        self.ctx.fillStyle = fillstyle

    def fillRect(self, tlv, brv):          
        self.ctx.fillRect(tlv.x, tlv.y, brv.m(tlv).x, brv.m(tlv).y)

    def clear(self):        
        self.ctx.clearRect(0, 0, self.width, self.height)

    def drawline(self, fromv, tov):        
        self.ctx.beginPath()
        self.ctx.moveTo(fromv.x, fromv.y)
        self.ctx.lineTo(tov.x, tov.y)
        self.ctx.stroke()
######################################################

######################################################
# constants
WINDOW_SAFETY_MARGIN = 10
######################################################

######################################################
# widgets
class Button(Input):
    def clicked(self):
        self.callback(self.key)

    def __init__(self, caption, callback = None, key = None):
        super().__init__("button")                
        self.sv(caption)
        if not ( callback is None ):
            self.callback = callback
            self.key = key
            self.ae("mousedown", self.clicked)

class RawTextInput(Input):
    def keyup(self, ev):
        if not ( self.callback is None ):
            if ev.keyCode == 13:
                if not ( self.entercallback is None ):
                    self.entercallback(self.v())
            else:
                if not ( self.keycallback is None ):
                    self.keycallback(ev.keyCode, self.v())

    def setText(self, content):
        self.sv(content)
        return self

    def getText(self):
        return self.v()

    def __init__(self, args):
        super().__init__("text")                
        self.entercallback = args.get("entercallback", None)
        self.keycallback = args.get("keycallback", None)
        self.cssclass = args.get("tinpclass", "defaultrawtextinput")
        self.ac(self.cssclass)
        self.ae("keyup", self.keyup)

class TextInputWithButton(e):
    def submitcallback(self):
        if not ( self.onsubmitcallback is None ):
            v = self.tinp.v()
            self.tinp.sv("")
            self.onsubmitcallback(v)

    def __init__(self, args = {}):
        super().__init__("div")
        contclass = args.get("contclass", "textinputcontainer")
        args["tinpclass"] = args.get("tinpclass", "textinputtext")
        sbtnclass = args.get("sbtnclass", "textinputbutton")
        self.container = Div().ac(contclass)
        self.onsubmitcallback = args.get("submitcallback", None)
        args["entercallback"] = self.submitcallback
        self.tinp = RawTextInput(args)
        self.sbtn = Button("Submit", self.submitcallback).ac(sbtnclass)        
        self.container.aa([self.tinp, self.sbtn])
        self.a(self.container)

    def focus(self):
        self.tinp.fl()
        return self

class LogItem(e):
    def equalto(self, logitem):
        return ( self.content == logitem.content ) and ( self.kind == logitem.kind )

    def getcontent(self):
        if self.mul == 0:
            return self.content
        else:
            return "<span class='logitemcontentmul'>+{}</span> {}".format(self.mul, self.content)

    def updatecontent(self):
        self.cdiv.html(self.getcontent())
        return self

    def __init__(self, content, kind = "normal"):
        super().__init__("div")
        self.kind = kind
        self.mul = 0
        self.tdiv = Div().ac("logtimediv").html("{}".format(__new__ (Date()).toLocaleTimeString()))
        self.content = content
        self.cdiv = Div().ac("logcontentdiv")
        if len(self.content)>0:
            if self.content[0] == "[" or self.content[0] == "{":
                try:
                    json = JSON.parse(self.content)
                    jsonstr = JSON.stringify(json, None, 2)
                    self.content = "<pre>" + jsonstr + "</pre>"
                    self.cdiv.ac("logcontentjson")
                except:
                    pass
        self.content = striplonglines(self.content)
        if len(self.content) > MAX_CONTENT_LENGTH:
            self.content = self.content[:MAX_CONTENT_LENGTH]
        self.cdiv.html(self.content)
        if self.kind == "cmd":
            self.cdiv.ac("logcontentcmd")
        elif self.kind == "cmdinfo":
            self.cdiv.ac("logcontentcmdinfo")
        elif self.kind == "cmdreadline":
            self.cdiv.ac("logcontentcmdreadline")
        elif self.kind == "cmdstatusok":
            self.cdiv.ac("logcontentcmdstatusok")
        elif self.kind == "cmdstatuserr":
            self.cdiv.ac("logcontentcmdstatuserr")
        self.idiv = Div().ac("logitemdiv").aa([self.tdiv, self.cdiv])
        self.idiv.aa([self.tdiv, self.cdiv])
        self.a(self.idiv)

class Log(e):
    def __init__(self, args):
        super().__init__("div")
        self.width = args.get("width", 600)
        self.height = args.get("height", 400)
        self.maxitems = args.get("maxitems", 100)
        self.ac("logdiv")
        self.items = []        
        self.resize(self.width, self.height)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.w(self.width).mh(self.height)
        return self

    def build(self):
        self.x()
        for item in reversed(self.items):
            item.updatecontent()
            self.a(item)

    def add(self, item):        
        if len(self.items)>0:
            last = self.items[len(self.items)-1]            
            if last.equalto(item):
                last.mul+=1                
            else:
                self.items.append(item)        
        else:
            self.items.append(item)        
        if len(self.items) > self.maxitems:
            self.items = self.items[1:]

    def log(self, item):
        self.add(item)
        self.build()

class Tab(e):
    def __init__(self, key, displayname, element):
        self.key = key
        self.displayname = displayname
        self.element = element
        self.tabelement = None

class TabPane(e):
    def __init__(self, args):        
        super().__init__("div")
        self.id = args.get("id", None)
        self.kind = args.get("kind", "child")
        self.width = args.get("width", 600)
        self.height = args.get("height", 400)
        self.marginleft = args.get("marginleft", 0)
        self.margintop = args.get("margintop", 0)
        self.tabsheight = args.get("tabsheight", 40)                
        self.tabsdiv = Div().ac("tabpanetabsdiv")
        self.contentdiv = Div().ac("tabpanecontentdiv")
        self.container = Div().ac("tabpanecontainer")
        self.container.aa([self.tabsdiv, self.contentdiv])        
        self.a(self.container)        
        self.tabs = []
        self.seltab = None
        self.resize()

    def resize(self, width = None, height = None):
        if self.kind == "main":
            self.width = window.innerWidth - 2 * WINDOW_SAFETY_MARGIN
            self.height = window.innerHeight - 2 * WINDOW_SAFETY_MARGIN
            self.marginleft = WINDOW_SAFETY_MARGIN
            self.margintop = WINDOW_SAFETY_MARGIN
        if not ( width is None ):
            self.width = width
        if not ( height is None ):
            self.height = height
        self.contentheight = self.height - self.tabsheight
        self.tabsdiv.w(self.width).h(self.tabsheight)
        self.contentdiv.w(self.width).h(self.contentheight)
        self.container.w(self.width).h(self.height).ml(self.marginleft).mt(self.margintop)
        try:
            self.resizecontent(self.seltab.element)
        except:
            pass

    def tabSelectedCallback(self, tab):
        self.selectByKey(tab.key)

    def setTabs(self, tabs, key):
        self.tabs = tabs
        self.tabsdiv.x()
        for tab in self.tabs:
            tabelement = Div().aac(["tabpanetab","noselect"]).html(tab.displayname)
            self.tabsdiv.a(tabelement)
            tab.tabelement = tabelement
            tab.tabelement.ae("mousedown", self.tabSelectedCallback.bind(self, tab))
        if not ( self.key is None ):
            storedkey = localStorage.getItem(self.id)
            if not ( storedkey is None ):
                key = storedkey
        return self.selectByKey(key)

    def getTabByKey(self, key, updateclass = False):
        if len(self.tabs) == 0:
            return None
        seltab = self.tabs[0]
        for tab in self.tabs:
            if updateclass:
                tab.tabelement.rc("tabpaneseltab")
                if tab.key == key:
                    tab.tabelement.ac("tabpaneseltab")
            if tab.key == key:
                seltab = tab        
        return seltab

    def innercontentheight(self):
        return self.contentheight - SCROLL_BAR_WIDTH

    def innercontentwidth(self):
        return self.width - SCROLL_BAR_WIDTH

    def resizecontent(self, element):
        try:
            element.resize(self.innercontentwidth(), self.innercontentheight())
        except:
            pass

    def setTabElementByKey(self, key, tabelement = None):
        tab = self.getTabByKey(key, tabelement is None)
        if tab == None:
            return self
        if not ( tabelement is None ):
            tab.element = tabelement
            if tab == self.seltab:
                self.contentdiv.x().a(tab.element)
        else:
            self.seltab = tab
            self.contentdiv.x().a(tab.element)
        self.resizecontent(tab.element)
        return self

    def selectByKey(self, key):
        if not ( self.id is None ):
            localStorage.setItem(self.id, key)
        return self.setTabElementByKey(key)

class ComboOption:
    def __init__(self, key, displayname):
        self.key = key
        self.displayname = displayname

class ComboBox(e):
    def selectchangecallback(self):
        key = self.select.v()
        if not ( self.changecallback is None ):
            self.changecallback(key)

    def __init__(self, args):
        super().__init__("div")
        self.selectclass = args.get("selectclass", "comboboxselect")
        self.optionfirstclass = args.get("optionfirstclass", "comboboxoptionfirst")
        self.optionclass = args.get("optionclass", "comboboxoption")
        self.changecallback = args.get("changecallback", None)
        self.options = []
        self.container = Div()
        self.select = Select().aac(["comboboxselect", self.selectclass])
        self.select.ae("change", self.selectchangecallback)
        self.container.a(self.select)
        self.a(self.container)

    def setoptions(self, options, selectedkey = None):
        self.options = options
        self.select.x()
        first = True
        for key , displayname in self.options.items():            
            opte = Option(key, displayname, key == selectedkey)            
            if first:
                opte.ac(self.optionfirstclass)
                first = False
            else:                
                opte.ac(self.optionclass)
            self.select.a(opte)
        return self

class LinkedCheckBox(Input):
    def setchecked(self, checked):        
        self.e.checked = checked
        return self

    def getchecked(self):
        return self.e.checked

    def updatevar(self):        
        self.parent[self.varname] = self.getchecked()

    def changed(self):        
        self.updatevar()
        if not ( self.changecallback is None ):
            self.changecallback()

    def __init__(self, parent, varname, args = {}):
        super().__init__("checkbox")                                        
        self.parent = parent
        self.varname = varname
        self.setchecked(self.parent[self.varname])
        self.changecallback = args.get("changecallback", None)
        self.ae("change", self.changed)

class LinkedTextInput(e):
    def updatevar(self):        
        self.parent[self.varname] = self.getText()

    def keyup(self):
        self.updatevar()
        if not ( self.keyupcallback is None ):
            self.keyupcallback()

    def setText(self, content):
        self.rawtextinput.setText(content)
        return self

    def getText(self):
        return self.rawtextinput.getText()

    def able(self, enabled):
        self.rawtextinput.able(enabled)
        return self

    def __init__(self, parent, varname, args = {}):
        super().__init__("div")
        self.parent = parent
        self.varname = varname        
        self.value = self.parent[self.varname]
        self.rawtextinputclass = args.get("textclass", "defaultlinkedtextinputtext")
        self.rawtextinput = RawTextInput({
            "keycallback": self.keyup,
            "entercallback": self.keyup,
            "tinpclass": self.rawtextinputclass
        })                
        self.setText(self.value)
        patchclasses(self, args)
        self.keyupcallback = args.get("keyupcallback", None)
        self.a(self.rawtextinput)

class LinkedSlider(e):
    def changed(self):                        
        self.verify()
        if not ( self.changecallback is None ):
            self.changecallback()

    def sliderchanged(self):
        if self.sliderenabled:
            self.value = self.slider.v()        
            self.valuetextinput.setText(self.value)
            self.verify()
            if not ( self.changecallback is None ):
                self.changecallback()

    def setslider(self):
        self.sliderenabled = False        
        self.slider.setmin(self.minvalue)
        self.slider.setmax(self.maxvalue)
        self.slider.sv(self.value)
        self.sliderenabled = True

    def build(self):
        self.container = Div().aac(["linkedslidercontainerclass", self.containerclass])
        self.valuetextinput = LinkedTextInput(self, "value", {
            "keyupcallback": self.changed,
            "textclass": self.valuetextclass
        })
        self.mintextinput = LinkedTextInput(self, "minvalue", {
            "keyupcallback": self.changed,
            "textclass": self.mintextclass
        })        
        self.maxtextinput = LinkedTextInput(self, "maxvalue", {
            "keyupcallback": self.changed,
            "textclass": self.maxtextclass
        })
        self.slider = Slider().aac(["linkedslidersliderclass", self.sliderclass])                
        self.slider.ae("change", self.sliderchanged)                
        self.container.aa([self.valuetextinput, self.mintextinput, self.slider, self.maxtextinput])
        self.x().a(self.container)
        self.verify()
        return self

    def verify(self):
        try:
            self.value = int(self.value)
        except:
            self.value = 1        
        try:
            self.minvalue = int(self.minvalue)
        except:
            self.minvalue = 1        
        try:
            self.maxvalue = int(self.maxvalue)
        except:
            self.maxvalue = 100        
        self.parent[self.varname] = self.value        
        self.parent[self.minvarname] = self.minvalue        
        self.parent[self.maxvarname] = self.maxvalue        
        self.setslider()

    def __init__(self, parent, varname, args = {}):
        super().__init__("div")                                        
        self.parent = parent
        self.varname = varname                                
        self.minvarname = "min" + self.varname
        self.maxvarname = "max" + self.varname        
        self.value = self.parent[self.varname]   
        self.minvalue = self.parent[self.minvarname]   
        self.maxvalue = self.parent[self.maxvarname]   
        self.changecallback = args.get("changecallback", None)
        self.containerclass = args.get("containerclass", "linkedslidercontainerclass")
        self.valuetextclass = args.get("valuetextclass", "linkedslidervaluetextclass")
        self.mintextclass = args.get("mintextclass", "linkedslidermintextclass")        
        self.sliderclass = args.get("sliderclass", "linkedslidersliderclass")
        self.maxtextclass = args.get("maxtextclass", "linkedslidermaxtextclass")                
        self.build()

class LinkedTextarea(e):
    def updatevar(self):        
        self.parent[self.varname] = self.getText()

    def keyup(self):
        self.updatevar()

    def setText(self, content):
        self.textarea.setText(content)

    def getText(self):
        return self.textarea.getText()

    def __init__(self, parent, varname, args = {}):
        super().__init__("div")
        self.parent = parent
        self.varname = varname        
        self.textarea = TextArea()        
        self.textarea.ae("keyup", self.keyup)
        self.text = args.get("text", "")
        self.setText(self.text)
        patchclasses(self, args)
        self.a(self.textarea)

class LabeledLinkedCheckBox(e):
    def __init__(self, label, parent, varname, args = {}):
        super().__init__("div")
        self.lcb = LinkedCheckBox(parent, varname, args)
        self.container = Div().ac("labeledlinkedcheckboxcontainer")
        self.ldiv = Div().html(label)
        self.container.aa([self.ldiv, self.lcb])                
        patchclasses(self, args)
        self.a(self.container).ac("labeledlinkedcheckbox")

class LogPane(e):
    def resize(self, width, height):
        self.width = width
        self.height = height        
        self.contentheight = self.height
        if self.contentheight < self.mincontentheight:
            self.contentheight = self.mincontentheight
        self.contentdiv.w(self.width).h(self.contentheight)
        self.w(self.width).h(self.height)        
        try:
            self.content.resize(self.innercontentwidth(), self.innercontentheight())
        except:
            pass

    def innercontentheight(self):
        return self.contentheight - SCROLL_BAR_WIDTH

    def innercontentwidth(self):
        return self.width - SCROLL_BAR_WIDTH

    def setcontent(self, element):
        self.content = element
        self.contentdiv.x().a(self.content)

    def __init__(self, args = {}):
        super().__init__("div")
        self.width = args.get("width", 600)
        self.height = args.get("height", 400)        
        self.mincontentheight = args.get("mincontentheight", 100)        
        self.contentdiv = Div().ac("logpanecontentdiv")
        self.resize(self.width, self.height)        
        self.aa([self.contentdiv])
        self.log = Log({})
        self.setcontent(self.log)

class SplitPane(e):
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.controldiv.w(self.width).h(self.controlheight)
        self.contentheight = self.height - self.controlheight
        if self.contentheight < self.mincontentheight:
            self.contentheight = self.mincontentheight
        self.contentdiv.w(self.width).h(self.contentheight)
        self.w(self.width).h(self.height)        
        try:
            self.content.resize(self.innercontentwidth(), self.innercontentheight())
        except:
            pass

    def innercontentheight(self):
        return self.contentheight - SCROLL_BAR_WIDTH

    def innercontentwidth(self):
        return self.width - SCROLL_BAR_WIDTH

    def setcontent(self, element):
        self.content = element
        self.contentdiv.x().a(self.content)

    def __init__(self, args = {}):
        super().__init__("div")
        self.width = args.get("width", 600)
        self.height = args.get("height", 400)
        self.controlheight = args.get("controlheight", 100)
        self.mincontentheight = args.get("mincontentheight", 100)
        self.controldiv = Div().ac("splitpanecontrolpanel")
        self.contentdiv = Div().ac("splitpanecontentdiv")
        self.resize(self.width, self.height)        
        self.aa([self.controldiv, self.contentdiv])

class ProcessConsole(SplitPane):
    def aliascallback(self, key):                
        cmds = self.cmdaliases[key]["cmds"]
        for cmd in cmds:
            self.submitcallback(cmd)

    def submitcallback(self, content):
        self.log.log(LogItem(content, "cmd"))
        if self.cmdinpcallback is None:
            return
        self.cmdinpcallback(content, self.key)

    def __init__(self, args = {}):
        args["controlheight"] = 80
        super().__init__(args)
        self.key = args.get("key", None)
        self.cmdinpcallback = args.get("cmdinpcallback", None)        
        self.cmdinp = TextInputWithButton({"submitcallback": self.submitcallback})
        self.cmdaliases = args.get("cmdaliases", {})
        self.controldiv.a(self.cmdinp)        
        for cmdaliaskey in self.cmdaliases.keys():
            cmdalias = self.cmdaliases[cmdaliaskey]
            btn = Button(cmdalias["display"], self.aliascallback, cmdaliaskey)
            self.controldiv.a(btn)
        self.log = Log({})
        self.setcontent(self.log)

######################################################

######################################################
# schema

schemaclipboard = None

SCHEMA_WRITE_PREFERENCE_DEFAULTS = [
    {"key":"addchild","display":"Add child","default":True},
    {"key":"remove","display":"Remove","default":True},
    {"key":"childsopened","display":"Childs opened","default":False},
    {"key":"editenabled","display":"Edit enabled","default":True},
    {"key":"editkey","display":"Edit key","default":True},
    {"key":"editvalue","display":"Edit value","default":True},        
    {"key":"radio","display":"Radio","default":False},        
    {"key":"slider","display":"Slider","default":False},        
    {"key":"check","display":"Check","default":False},        
    {"key":"showhelpashtml","display":"Show help as HTML","default":True}
]

class SchemaWritePreference:    
    def __init__(self):
        for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
            self[item["key"]] = item["default"]
        self.parent = None
        self.changecallback = None
        self.disabledlist = []

    def setparent(self, parent):
        self.parent = parent
        return self

    def setchangecallback(self, changecallback):
        self.changecallback = changecallback
        return self

    def changed(self):        
        if not ( self.changecallback is None ):
            self.changecallback()

    def setdisabledlist(self, disabledlist):
        self.disabledlist = disabledlist
        return self

    def form(self):
        formdiv = Div().ac("noselect")

        mdl = self.disabledlist
        if not ( self.parent is None ):
            if self.parent.parent is None:
                mdl = mdl + ["editkey"]

        for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
            if not ( item["key"] in mdl ):
                formdiv.a(LabeledLinkedCheckBox(item["display"], self, item["key"], {
                    "patchclasses":["container/a/schemawritepreferenceformsubdiv"],
                    "changecallback": self.changed
                }))

        return formdiv

    def toobj(self):        
        obj = {}
        for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
            obj[item["key"]] = self[item["key"]]
        return obj

DEFAULT_HELP = "No help available for this item."
DEFAULT_ENABLED = True

class SchemaItem(e):
    def parentsettask(self):
        pass

    def setparent(self, parent):
        self.parent = parent
        self.parentsettask()

    def getitem(self):
        return self

    def label(self):
        return ""

    def baseobj(self):        
        obj = {
            "kind": self.kind,
            "enabled": self.enabled,
            "help": self.help,
            "writepreference": self.writepreference.toobj()
        }
        return obj

    def toobj(self):
        return self.baseobj()

    def topureobj(self):
        pureobj = {}
        return pureobj

    def enablechangedtask():
        pass

    def enablecallback(self):                
        self.enabled = self.enablecheckbox.getchecked()
        if not ( self.childparent is None ):
            if self.childparent.writepreference.radio:
                self.childparent.setradio(self)            
            self.childparent.enablechangedtask()
        self.enablechangedtask()

    def setenabled(self, enabled):
        self.enabled = enabled
        self.enablecheckbox.setchecked(self.enabled)

    def helpboxclicked(self):        
        if self.helpopen:
            self.helphook.x()
            self.helpopen = False
        else:
            self.helpdiv = Div().ac("schemahelpdiv")
            self.helpcontentdiv = Div().aac(["schemahelpcontentdiv","noselect"]).html(self.help)
            self.helpeditdiv = Div().ac("schemahelpeditdiv")
            self.helpedittextarea = LinkedTextarea(self, "help", {"patchclasses":["textarea/a/schemahelpedittextarea"],"text":self.help})
            self.helpeditdiv.a(self.helpedittextarea)
            if self.writepreference.showhelpashtml:                
                self.helpdiv.a(self.helpcontentdiv)
            else:
                self.helpdiv.a(self.helpeditdiv)
            self.helphook.a(self.helpdiv)
            self.helpopen = True

    def copyboxclicked(self):
        schemaclipboard.copy(self)        
    
    def settingsboxclicked(self):
        if self.settingsopen:
            self.settingshook.x()
            self.settingsopen = False
        else:
            self.settingsdiv = Div().ac("schemasettingsdiv").a(self.writepreference.form())
            self.settingshook.a(self.settingsdiv)
            self.settingsopen = True            

    def removeboxclicked(self):
        self.childparent.remove(self)
        pass

    def writepreferencechangedtask(self):
        pass

    def writepreferencechanged(self):
        self.helpboxclicked()
        self.helpboxclicked()
        self.enablecheckbox.able(self.writepreference.editenabled)
        self.setchildparent(self.childparent)
        self.writepreferencechangedtask()
        if not ( self.parent is None ):
            self.parent.writepreferencechangedtask()

    def setchildparent(self, childparent):
        self.childparent = childparent
        if ( not ( self.childparent is None ) ) and self.writepreference.remove:
            self.schemacontainer.x().aa([self.enablebox, self.element, self.helpbox, self.copybox, self.settingsbox, self.removebox])
        else:
            self.schemacontainer.x().aa([self.enablebox, self.element, self.helpbox, self.copybox, self.settingsbox])

    def elementdragstart(self, ev):
        self.dragstartvect = getClientVect(ev)        

    def elementdrag(self, ev):
        pass

    def move(self, dir):
        if self.childparent is None:
            return
        i = self.childparent.getitemindex(self)
        newi = i + dir
        self.childparent.movechildi(i, newi)

    def elementdragend(self, ev):
        self.dragendvect = getClientVect(ev)        
        diff = self.dragendvect.m(self.dragstartvect)
        dir = int(diff.y / getglobalcssvarpxint("--schemabase"))
        self.move(dir)

    def __init__(self, args):
        super().__init__("div")
        self.parent = None
        self.childparent = None
        self.args = args
        self.kind = "item"
        self.enabled = args.get("enabled", DEFAULT_ENABLED)
        self.help = args.get("help", DEFAULT_HELP)
        self.writepreference = args.get("writepreference", SchemaWritePreference())
        self.writepreference.setparent(self)
        self.writepreference.setchangecallback(self.writepreferencechanged)        
        self.element = Div().ac("schemaitem")        
        self.schemacontainer = Div().ac("schemacontainer")
        self.enablebox = Div().ac("schemaenablebox")
        self.enablecheckbox = CheckBox(self.enabled).ac("schemaenablecheckbox").ae("change", self.enablecallback)
        self.enablecheckbox.able(self.writepreference.editenabled)
        self.enablebox.a(self.enablecheckbox)                
        self.helpbox = Div().aac(["schemahelpbox","noselect"]).ae("mousedown", self.helpboxclicked).html("?")        
        self.copybox = Div().aac(["schemacopybox","noselect"]).ae("mousedown", self.copyboxclicked).html("C")        
        self.settingsbox = Div().aac(["schemasettingsbox","noselect"]).ae("mousedown", self.settingsboxclicked).html("S")
        self.removebox = Div().aac(["schemaremovebox","noselect"]).ae("mousedown", self.removeboxclicked).html("X")        
        self.afterelementhook = Div()
        self.settingsopen = args.get("settingsopen", False)
        self.helpopen = args.get("helpopen", False)
        self.settingshook = Div()        
        self.helphook = Div()        
        self.schemacontainer.aa([self.enablebox, self.element, self.helpbox, self.copybox, self.settingsbox])
        self.itemcontainer = Div()
        self.itemcontainer.aa([self.schemacontainer, self.helphook, self.settingshook, self.afterelementhook])
        self.a(self.itemcontainer)
        self.dragelement = self.copybox
        self.dragelement.sa("draggable", True)
        self.dragelement.ae("dragstart", self.elementdragstart)
        self.dragelement.ae("drag", self.elementdrag)
        self.dragelement.ae("dragend", self.elementdragend)
        self.dragelement.ae("dragover", lambda ev: ev.preventDefault())

class NamedSchemaItem(e):
    def getitem(self):
        return self.item

    def label(self):
        return self.key

    def toobj(self):        
        return {
            "kind": "nameditem",
            "key": self.key,
            "item": self.item.toobj()
        }

    def writepreferencechangedtask(self):
        self.linkedtextinput.able(self.item.writepreference.editkey)

    def keychanged(self):
        if not ( self.keychangedcallback is None ):
            self.keychangedcallback()

    def setkeychangedcallback(self, keychangedcallback):
        self.keychangedcallback = keychangedcallback
        return self

    def setkey(self, key):
        self.key = key
        self.linkedtextinput.setText(self.key)
        return self
    
    def __init__(self, args):
        super().__init__("div")
        self.kind = "nameditem"
        #self.key = args.get("key", uid())
        self.key = args.get("key", "")
        self.item = args.get("item", SchemaItem(args))        
        self.keychangedcallback = None
        self.item.setparent(self)
        self.namedcontainer = Div().ac("namedschemaitem")
        self.namediv = Div().ac("schemaitemname")        
        self.linkedtextinput = LinkedTextInput(self, "key", {
            "textclass": "namedschemaitemrawtextinput",
            "keyupcallback": self.keychanged
        })
        self.linkedtextinput.setText(self.key)
        self.linkedtextinput.able(self.item.writepreference.editkey)
        self.namediv.a(self.linkedtextinput)        
        self.namedcontainer.aa([self.namediv, self.item])
        self.a(self.namedcontainer)

    def copy(self, item):
        self.item = schemafromobj(item.toobj())
        self.item.parent = None
        self.key = None
        if not ( item.parent is None ):
            self.key = item.parent.key        

class SchemaScalar(SchemaItem):
    def label(self):
        return self.value

    def toobj(self):
        obj = self.baseobj()
        obj["value"] = self.value
        obj["minvalue"] = self.minvalue
        obj["maxvalue"] = self.maxvalue
        return obj

    def topureobj(self):
        obj = self.value
        return obj

    def writepreferencechangedtask(self):
        self.build()

    def enablechangedtask(self):        
        if self.writepreference.check:
            if self.enabled:
                self.value = "true"
            else:
                self.value = "false"
            self.linkedtextinput.setText(self.value)

    def build(self):
        if self.writepreference.slider:
            self.enablecheckbox.rc("schemacheckenablecheckbox")
            self.linkedslider = LinkedSlider(self, "value", {
                "containerclass": "schemalinkedslidercontainerclass",
                "valuetextclass": "schemalinkedslidervaluetextclass",
                "mintextclass": "schemalinkedslidermintextclass",
                "sliderclass": "schemalinkedslidersliderclass",
                "maxtextclass": "schemalinkedslidermaxtextclass"
            })
            self.element.x().aa([self.linkedslider])
        else:            
            self.enablebox.arc(self.writepreference.check, "schemacheckenablecheckbox")            
            self.linkedtextinput = LinkedTextInput(self, "value", {"textclass":"schemascalarrawtextinput"})            
            self.linkedtextinput.able(self.writepreference.editvalue)                
            self.element.x().aa([self.linkedtextinput])

    def __init__(self, args):
        super().__init__(args)
        self.kind = "scalar"        
        #self.value = args.get("value", randscalarvalue(2, 8))
        self.value = args.get("value", "")
        self.minvalue = args.get("minvalue", 1)        
        self.maxvalue = args.get("maxvalue", 100)        
        self.element.ac("schemascalar")        
        self.writepreference.setdisabledlist(["addchild","childsopened","radio"])
        self.build()

class SchemaCollection(SchemaItem):
    def removechildi(self, i):        
        newchilds = []
        rchild = None
        for j in range(0, len(self.childs)):
            if ( j == i ):
                rchild = self.childs[j]
            else:
                newchilds.append(self.childs[j])
        self.childs = newchilds        
        self.openchilds()
        self.openchilds()
        return rchild        

    def insertchildi(self, i, child):
        newchilds = []
        for j in range(0, len(self.childs) + 1):
            if ( j == i ):
                newchilds.append(child)
            if ( j < len(self.childs) ):
                newchilds.append(self.childs[j])
        self.childs = newchilds        
        self.openchilds()
        self.openchilds()

    def movechildi(self, i, newi):        
        if len(self.childs) <= 0:
            return
        if newi < 0:
            newi = 0
        if newi >= len(self.childs):
            newi = len(self.childs) - 1
        rchild = self.removechildi(i)
        if not ( rchild is None ):
            self.insertchildi(newi, rchild)

    def getitemindex(self, item):
        for i in range(0, len(self.childs)):
            if self.childs[i].getitem() == item:
                return i
        return None

    def parentsettask(self):        
        self.opendiv.arc(not self.parent is None, "schemadictchildleftmargin")

    def enablechangedtask(self):
        self.openchilds()
        self.openchilds()

    def buildchilds(self):
        labellist = []
        self.childshook.x()
        for child in self.childs:
            self.childshook.a(child)
            if child.getitem().enabled:
                labellist.append(child.label())
        label = " , ".join(labellist)
        self.openbutton.x().a(Div().ac("schemacollectionopenbuttonlabel").html(label))

    def topureobj(self):
        pureobj = {}
        if self.writepreference.radio:
            if self.kind == "dict":
                pureobj = ["", {}]
                for nameditem in self.childs:
                    key = nameditem.key
                    item = nameditem.item
                    if item.enabled or item.writepreference.check:
                        pureobj = [key, item.topureobj()]
                        break
            elif self.kind == "list":                
                for item in self.childs:
                    if item.enabled or item.writepreference.check:
                        pureobj = item.topureobj()
                        break
        else:
            if self.kind == "dict":
                for nameditem in self.childs:
                    key = nameditem.key
                    item = nameditem.item
                    if item.enabled or item.writepreference.check:
                        pureobj[key] = item.topureobj()
            elif self.kind == "list":
                pureobj = []
                for item in self.childs:
                    if item.enabled or item.writepreference.check:
                        pureobj.append(item.topureobj())
        return pureobj

    def setradio(self, item):
        for child in self.childs:
            childitem = child.getitem()
            childeq = ( childitem == item )                
            childitem.enabled = childeq            
            childitem.enablecheckbox.setchecked(childeq)

    def remove(self, item):
        newlist = []
        for child in self.childs:
            childeq = False
            if child.kind == "nameditem":
                childeq = ( child.item == item )
            else:
                childeq = ( child == item )
            if not childeq:
                newlist.append(child)
        self.childs = newlist
        self.openchilds()
        self.openchilds()

    def getschemakinds(self):
        schemakinds = {
            "create" : "Create new",
            "scalar" : "Scalar",
            "list" : "List",
            "dict" : "Dict"
        }                        
        for nameditem in self.childs:                
            key = nameditem.key
            if not ( key == None ):
                if len(key) > 0:
                    schemakinds["#" + key] = key        
        return schemakinds

    def updatecreatecombo(self):        
        if not ( self.createcombo is None ):
            self.createcombo.setoptions(self.getschemakinds())

    def getchildbykey(self, key):
        if not ( self.kind == "dict" ):
            return None
        for nameditem in self.childs:
            if nameditem.key == key:
                return nameditem.item
        return None

    def createcallback(self, key):
        self.updatecreatecombo()
        sch = SchemaScalar({})
        if key == "list":
            sch = SchemaList({})
        elif key == "dict":
            sch = SchemaDict({})        
        if key[0] == "#":
            truekey = key[1:]
            titem = self.getchildbykey(truekey)
            if titem == None:
                print("error, no item with key", truekey)
            else:
                sch = schemafromobj(titem.toobj())
        sch.setchildparent(self)
        appendelement = sch
        if self.kind == "dict":
            appendelement = NamedSchemaItem({
                "item": sch
            }).setkeychangedcallback(self.updatecreatecombo)
        self.childs.append(appendelement)
        self.buildchilds()      
        self.updatecreatecombo()          

    def pastebuttonclicked(self):        
        try:        
            sch = schemafromobj(schemaclipboard.item.toobj())
        except:
            window.alert("No item on clipboard to paste!")
            return self
        sch.setchildparent(self)
        appendelement = sch
        if self.kind == "dict":
            appendelement = NamedSchemaItem({
                "item": sch
            }).setkeychangedcallback(self.updatecreatecombo)
            if not ( schemaclipboard.key is None ):
                appendelement.setkey(schemaclipboard.key)
        self.childs.append(appendelement)
        self.buildchilds()      
        self.updatecreatecombo()          

    def openchilds(self):
        if self.opened:
            self.opened = False
            self.createhook.x()
            self.childshook.x()
            self.openbutton.rc("schemacollectionopenbuttondone")
        else:
            self.opened = True
            self.creatediv = Div().ac("schemaitem").ac("schemacreate")
            self.createcombo = ComboBox({
                "changecallback": self.createcallback,
                "selectclass": "schemacreatecomboselect"
            })
            self.updatecreatecombo()
            self.pastebutton = Button("Paste", self.pastebuttonclicked).ac("schemapastebutton")
            self.creatediv.aa([self.createcombo, self.pastebutton])
            if self.writepreference.addchild:
                self.createhook.a(self.creatediv)
            self.openbutton.ac("schemacollectionopenbuttondone")
            self.buildchilds()

    def writepreferencechangedtask(self):        
        self.openchilds()        
        self.openchilds()        

    def __init__(self, args):
        super().__init__(args)
        self.kind = "collection"        
        self.opened = False
        self.childs = args.get("childs", [])
        self.editmode = args.get("editmode", False)        
        self.childseditable = args.get("childseditable", True)
        self.element.ac("schemacollection")                
        self.openbutton = Div().aac(["schemacollectionopenbutton","noselect"]).ae("mousedown", self.openchilds)
        self.element.aa([self.openbutton])        
        self.createcombo = None
        self.createhook = Div()
        self.childshook = Div()
        self.opendiv = Div().ac("schemacollectionopendiv")
        self.opendiv.aa([self.createhook, self.childshook])        
        self.afterelementhook.a(self.opendiv)
        self.openchilds()            
        if not self.writepreference.childsopened:
            self.openchilds()            

class SchemaList(SchemaCollection):
    def getfirstselectedindex(self):        
        i = 0
        for item in self.childs:
            if item.enabled:
                return i
            i+=1
        return None

    def toobj(self):
        listobj = []
        for item in self.childs:
            listobj.append(item.toobj())
        obj = self.baseobj()
        obj["items"] = listobj
        return obj

    def __init__(self, args):
        super().__init__(args)        
        self.kind = "list"
        self.element.ac("schemalist")
        self.writepreference.setdisabledlist(["editvalue", "slider", "check"])

class SchemaDict(SchemaCollection):
    def setchildatkey(self, key, item):
        item.setchildparent(self)
        nameditem = NamedSchemaItem({
            "key": key,
            "item": item
        })                    
        i = self.getitemindexbykey(key)
        if i is None:
            self.childs.append(nameditem)                    
        else:
            self.childs[i] = nameditem
        self.openchilds()
        self.openchilds()        

    def getfirstselectedindex(self):        
        i = 0
        for item in self.childs:
            if item.item.enabled:
                return i
            i+=1
        return None

    def getitemindexbykey(self, key):
        i = 0
        for item in self.childs:
            if item.key == key:
                return i
            i+=1
        return None

    def toobj(self):
        dictobj = []
        for item in self.childs:
            sch = {
                "key": item.key,
                "item": item.item.toobj()
            }
            dictobj.append(sch)
        obj = self.baseobj()
        obj["items"] = dictobj
        return obj

    def __init__(self, args):
        super().__init__(args)        
        self.kind = "dict"
        self.element.ac("schemadict")
        self.writepreference.setdisabledlist(["editvalue", "slider", "check"])

def schemawritepreferencefromobj(obj):
    swp = SchemaWritePreference()    
    for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
        swp[item["key"]] = getfromobj(obj, item["key"], item["default"])
    return swp

def schemafromobj(obj):        
    kind = getfromobj(obj, "kind", "dict")
    enabled = getfromobj(obj, "enabled", DEFAULT_ENABLED)
    help = getfromobj(obj, "help", DEFAULT_HELP)
    writepreference = schemawritepreferencefromobj(getfromobj(obj, "writepreference", {}))
    returnobj = {}
    if kind == "scalar":        
        returnobj = SchemaScalar({
            "value": obj["value"],
            "minvalue": obj["minvalue"],
            "maxvalue": obj["maxvalue"],
            "writepreference": writepreference
        })
    elif kind == "list":
        items = obj["items"]
        childs = []
        for item in items:
            sch = schemafromobj(item)            
            childs.append(sch)        
        returnobj = SchemaList({
            "childs": childs,
            "writepreference": writepreference
        })
        for child in returnobj.childs:
            child.setchildparent(returnobj)
    elif kind == "dict":        
        items = obj["items"]
        childs = []
        for itemobj in items:
            key = itemobj["key"]
            item = itemobj["item"]
            sch = schemafromobj(item)
            namedsch = NamedSchemaItem({
                "key": key,
                "item": sch,
                "writepreference": writepreference
            })
            childs.append(namedsch)        
        returnobj = SchemaDict({
            "childs": childs,
            "writepreference": writepreference
        })  
        for child in returnobj.childs:
            child.item.setchildparent(returnobj)
            child.setkeychangedcallback(returnobj.updatecreatecombo)
    returnobj.setenabled(enabled)    
    returnobj.help = help        
    return returnobj

def getpathlistfromschema(sch, pathlist):    
    if len(pathlist)<=0:
        return sch
    key = pathlist[0]
    pathlist = pathlist[1:]
    if key == "#":
        if sch.kind == "scalar":
            return None
        elif sch.kind == "list":
            i = sch.getfirstselectedindex()
            if i == None:
                return None
            return getpathlistfromschema(sch.childs[i], pathlist)
        elif sch.kind == "dict":
            i = sch.getfirstselectedindex()
            if i == None:
                return None
            return getpathlistfromschema(sch.childs[i].item, pathlist)
    else:
        if sch.kind == "scalar":
            return None
        elif sch.kind == "list":
            return None
        elif sch.kind == "dict":
            for child in sch.childs:
                if child.key == key:
                    return getpathlistfromschema(child.item, pathlist)
    return None

def getpathfromschema(sch, path):
    pathlist = path.split("/")
    return getpathlistfromschema(sch, pathlist)

def schemafromucioptionsobj(obj):
    ucioptions = SchemaDict({})
    for opt in obj:
        key = opt["key"]
        kind = opt["kind"]
        default = opt["default"]
        min = opt["min"]
        max = opt["max"]
        options = opt["options"]
        item = SchemaScalar({
            "value": default
        })        
        if kind == "spin":            
            item.minvalue = min
            item.maxvalue = max
            item.writepreference.slider = True
            item.build()
        elif kind == "check":
            item.value = "false"
            if default:
                item.value = "true"
            item.writepreference.check = True
            item.setenabled(default)
            item.build()
        elif kind == "combo":
            item = SchemaList({})
            item.writepreference.radio = True
            for comboopt in options:
                comboitem = SchemaScalar({
                    "value": comboopt
                })
                comboitem.setenabled(comboopt == default)
                comboitem.setchildparent(item)
                item.childs.append(comboitem)
            item.openchilds()
            item.openchilds()

        item.setchildparent(ucioptions)

        nameditem = NamedSchemaItem({
            "key": key,
            "item": item
        })

        ucioptions.childs.append(nameditem)
    return ucioptions

schemaclipboard = NamedSchemaItem({})
######################################################
class DirBrowser(e):
    def __init__(self):
        super().__init__("div")
        self.pathlist = []
        self.loadpathlist(self.pathlist)

    def loadpathlist(self):        
        getjson("/dirlist/root/{}".format(self.path()), self.build, lambda err: print(err))

    def toparentdir(self):
        if len(self.pathlist) > 0:
            self.pathlist.pop()
        self.loadpathlist()

    def opendirfactory(self, name):
        def opendir():
            self.pathlist.append(name)
            self.loadpathlist()
        return opendir

    def path(self):
        return "/".join(self.pathlist)

    def namepath(self, name):
        if len(self.pathlist) <= 0:
            return name
        return "/".join([self.path(), name])

    def build(self, statsobj):
        self.x()        
        dirs = []
        files = []
        for item in statsobj:
            if item["isdir"]:
                dirs.append(item)
            else:
                files.append(item)        
        sorteddirs = sorted(dirs, key = lambda item: item["name"].toLowerCase())
        sortedfiles = sorted(files, key = lambda item: item["name"].toLowerCase())
        sortedobj = []
        for item in sorteddirs:
            sortedobj.append(item)
        for item in sortedfiles:
            sortedobj.append(item)
        if len(self.pathlist) > 0:
            updiv = Div().aac(["dirbrowseritem", "dirbrowserdir", "noselect"]).ae("mousedown", self.toparentdir)
            updiv.a(Div().aac(["dirbrowsertoparent","dirbrowserdirname"]).html(".."))
            self.a(updiv)
        for item in sortedobj:            
            itemdiv = Div().aac(["dirbrowseritem","noselect"])
            namediv = Div().ac("dirbrowsername")
            sizediv = Div().ac("dirbrowsersize")
            if item["isdir"]:
                text = item["name"]
                itemdiv.ac("dirbrowserdir").ae("mousedown", self.opendirfactory(item["name"]))
                namediv.ac("dirbrowserdirname").html(text)
                sizediv.html("dir")
            else:
                text = "<a href='/file/{}'>{}</a>".format(self.namepath(item["name"]), item["name"])
                itemdiv.ac("dirbrowserfile")
                namediv.html(text)
                sizediv.html("{} bytes".format(item["st_size"]))
            itemdiv.a(namediv)
            itemdiv.a(Div().ac("dirbrowsermodat").html(__new__ (Date(item["st_mtime"] * 1000)).toLocaleString()))
            itemdiv.a(sizediv)
            rwxdiv = Div().ac("dirbrowserrwx").html(item["st_mode_unix_rwx"])
            itemdiv.a(rwxdiv)
            self.a(itemdiv)            
STANDARD_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
ANTICHESS_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
RACING_KINGS_START_FEN = "8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1"
HORDE_START_FEN = "rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w kq - 0 1"
THREE_CHECK_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 3+3 0 1"
CRAZYHOUSE_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[] w KQkq - 0 1"
PIECE_KINDS = ["p", "n", "b", "r", "q", "k"]
WHITE = 1
BLACK = 0
VARIANT_OPTIONS = {
    "standard": "Standard",
    "fromPosition": "From Position",
    "antichess" : "Antichess",
    "atomic": "Atomic",
    "chess960": "Chess960",
    "crazyhouse": "Crazyhouse",
    "horde": "Horde",
    "kingOfTheHill": "King of the Hill",
    "racingKings": "Racing Kings",
    "threeCheck": "Three Check"
}
PIECE_NAMES = {
    "p": "Pawn",
    "n": "Knight",
    "b": "Bishop",
    "r": "Rook",
    "q": "Queen",
    "k": "King"
}
PROMPIECEKINDS_STANDARD = ["n", "b", "r", "q"]
PROMPIECEKINDS_ANTICHESS = ["n", "b", "r", "q", "k"]

def prompiecekindsforvariantkey(variantkey):
    if variantkey == "antichess":
        return PROMPIECEKINDS_ANTICHESS
    return PROMPIECEKINDS_STANDARD

def piececolortocolorname(color):
    if color == WHITE:
        return "White"
    elif color == BLACK:
        return "Black"
    return "Invalidcolor"

def piecekindtopiecename(kind):
    if kind in PIECE_NAMES:
        return PIECE_NAMES[kind]
    return "Invalidpiece"

def getstartfenforvariantkey(variantkey):
    if variantkey == "antichess":
        return ANTICHESS_START_FEN
    if variantkey == "racingKings":
        return RACING_KINGS_START_FEN
    if variantkey == "horde":
        return HORDE_START_FEN    
    if variantkey == "threeCheck":
        return THREE_CHECK_START_FEN
    if variantkey == "crazyhouse":
        return CRAZYHOUSE_START_FEN
    return STANDARD_START_FEN

class Piece():
    def __init__(self, kind = None, color = None):
        self.kind = kind
        self.color = color

    def isempty(self):
        return self.kind is None

    def ispiece(self):
        return not self.isempty()

    def __repr__(self):
        if self.isempty():
            return "Piece[None]"
        return "Piece[{} {}]".format(piececolortocolorname(self.color), piecekindtopiecename(self.kind))

def isvalidpieceletter(pieceletter):
    if pieceletter in PIECE_KINDS:
        return True
    if pieceletter.toLowerCase() in PIECE_KINDS:
        return True
    return False

def piecelettertopiece(pieceletter):
    if isvalidpieceletter(pieceletter):
        pieceletterlower = pieceletter.toLowerCase()
        if pieceletterlower == pieceletter:
            return Piece(pieceletterlower, BLACK)
        return Piece(pieceletterlower, WHITE)
    print("warning, piece letter not valid", pieceletter)
    return Piece()

def getclassforpiece(p, style):
    kind = p.kind
    if p.color == WHITE:
        kind = "w" + kind
    return style + "piece" + kind

class Square:
    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

    def p(self, sq):
        return Square(self.file + sq.file, self.rank + sq.rank)

    def __repr__(self):
        return "Square[file: {} , rank: {}]".format(self.file, self.rank)

    def copy(self):
        return Square(self.file, self.rank)

class Move:
    def __init__(self, fromsq, tosq, prompiece = Piece()):
        self.fromsq = fromsq
        self.tosq = tosq
        self.prompiece = prompiece

    def __repr__(self):
        return "Move [from: {} , to: {} , prom: {}]".format(self.fromsq, self.tosq, self.prompiece)

class PieceStore(e):
    def dragstartfactory(self, p, pdiv, pdivcopy):
        def dragstart():
            self.parent.dragkind = "set"
            self.parent.draggedsetpiece = p
            self.parent.draggedpdiv = pdivcopy
            self.parent.movecanvashook.x()            
            pdiv.op(0.7)
        return dragstart

    def setstore(self, store):
        self.store = store
        self.container.x()
        self.pieces = {}        
        for pieceletter in self.store.split(""):
            p = piecelettertopiece(pieceletter)
            if p.color == self.color:
                if p.kind in self.pieces:
                    self.pieces[p.kind]["mul"] += 1
                else:
                    pcdiv = Div().pr().w(self.piecesize).h(self.piecesize)
                    pdiv = Div().pa().cp().ac(getclassforpiece(p, self.parent.piecestyle)).w(self.piecesize).h(self.piecesize)
                    pdivcopy = Div().pa().cp().ac(getclassforpiece(p, self.parent.piecestyle)).w(self.piecesize).h(self.piecesize)
                    pdiv.t(0).l(0).sa("draggable", True).ae("dragstart", self.dragstartfactory(p, pdiv, pdivcopy))                
                    pcdiv.a(pdiv)
                    self.pieces[p.kind] = {
                        "mul": 1,
                        "p": p,
                        "pcdiv": pcdiv
                    }        
        for pkind, pdesc in self.pieces.items():
            muldiv = Div().pa().w(self.muldivsize).h(self.muldivsize).fs(self.muldivsize * 1.3).html("{}".format(pdesc["mul"]))
            muldiv.l(self.piecesize - self.muldivsize).t(0).ac("storemuldiv")
            pdesc["pcdiv"].a(muldiv)
            self.container.a(pdesc["pcdiv"])            
        return self

    def __init__(self, args):
        super().__init__("div")
        self.parent = args.get("parent", BasicBoard({}))
        self.store = args.get("store", "")
        self.color = args.get("color", WHITE)
        self.container = args.get("containerdiv", Div())
        self.container.ac("noselect")
        self.piecesize = args.get("piecesize", self.parent.piecesize)
        self.muldivsize = int(self.piecesize / 2)        
        self.a(self.container)
        self.setstore(self.store)

class BasicBoard(e):
    def clearcanvases(self):
        self.movecanvas.clear()
        self.piececanvashook.x()

    def ucitosquare(self, squci):
        try:
            file = squci.charCodeAt(0) - "a".charCodeAt(0)
            rank = self.lastrank - ( squci.charCodeAt(1) - "1".charCodeAt(0) )
            return Square(file, rank)
        except:
            return None

    def ucitomove(self, moveuci):        
        if "@" in moveuci:
            try:
                parts = moveuci.split("@")
                sq = self.ucitosquare(parts[1])
                move = Move(sq, sq, Piece(parts[0].toLowerCase(), self.turn()))
                return move
            except:
                return None
        else:
            try:
                move = Move(self.ucitosquare(moveuci[0:2]), self.ucitosquare(moveuci[2:4]))
                try:
                    if len(moveuci) > 4:
                        move.prompiece = Piece(moveuci[4].toLowerCase(), self.turn())                    
                except:
                    print("could not parse prompiece")
                return move
            except:
                return None

    def resize(self, width, height):
        self.squaresize = 35
        self.calcsizes()
        while self.totalheight() < height:
            self.squaresize += 1
            self.calcsizes()
        self.squaresize -= 1
        self.calcsizes()
        self.build()

    def totalheight(self):
        th = self.outerheight + self.fendivheight
        if self.variantkey == "crazyhouse":
            th += 2 * self.squaresize
        return th

    def squareuci(self, sq):
        fileletter = String.fromCharCode(sq.file + "a".charCodeAt(0))
        rankletter = String.fromCharCode(self.lastrank - sq.rank + "1".charCodeAt(0))
        return fileletter + rankletter

    def moveuci(self, move):
        fromuci = self.squareuci(move.fromsq)
        touci = self.squareuci(move.tosq)
        promuci = cpick(move.prompiece.isempty(), "", move.prompiece.kind)
        return fromuci + touci + promuci

    def islightfilerank(self, file, rank):
        return ( ( ( file + rank ) % 2 ) == 0 )

    def islightsquare(self, sq):
        return self.islightfilerank(sq.file, sq.rank)

    def squarelist(self):
        squarelist = []
        for file in range(self.numfiles):
            for rank in range(self.numranks):
                squarelist.append(Square(file, rank))
        return squarelist

    def squarecoordsvect(self, sq):
        return Vect(sq.file * self.squaresize, sq.rank * self.squaresize)

    def squarecoordsmiddlevect(self, sq):
        return self.squarecoordsvect(sq).p(Vect(self.squaresize / 2, self.squaresize / 2))

    def piececoordsvect(self, sq):
        return self.squarecoordsvect(sq).p(Vect(self.squarepadding, self.squarepadding))

    def flipawaresquare(self, sq):
        if self.flip:
            return Square(self.lastfile - sq.file, self.lastrank - sq.rank)
        return sq

    def piecedragstartfactory(self, sq, pdiv):
        def piecedragstart(ev):
            if self.promoting:
                ev.preventDefault()
                return
            self.dragkind = "move"
            self.draggedsq = sq            
            self.draggedpdiv = pdiv
            self.movecanvashook.x()
            pdiv.op(0.1)
        return piecedragstart

    def piecedragfactory(self):
        def piecedrag(ev):            
            pass
        return piecedrag

    def piecedragendfactory(self, sq, pdiv):
        def piecedragend(ev):                        
            pdiv.op(0.5)
        return piecedragend

    def piecedragoverfactory(self, sq):
        def piecedragover(ev):
            ev.preventDefault()            
        return piecedragover

    def ismovepromotion(self, move):
        fromp = self.getpieceatsquare(move.fromsq)
        if ( fromp.kind == "p" ) and ( fromp.color == self.turn() ):
            if self.iswhitesturn():
                if move.tosq.rank == 0:
                    return True
            else:
                if move.tosq.rank == self.lastrank:
                    return True
        return False

    def piecedropfactory(self, sq):
        def piecedrop(ev):
            ev.preventDefault()            
            self.draggedpdiv.pv(self.piececoordsvect(self.flipawaresquare(sq)))
            self.draggedpdiv.zi(100)
            if self.dragkind == "move":                
                self.dragmove = Move(self.draggedsq, sq)
                if self.ismovepromotion(self.dragmove):
                    self.promoting = True
                    self.build()
                elif not ( self.movecallback is None ):
                    self.movecallback(self.variantkey, self.fen, self.moveuci(self.dragmove))
            elif self.dragkind == "set":
                self.container.a(self.draggedpdiv)
                if not ( self.movecallback is None ):
                    setuci = "{}@{}".format(self.draggedsetpiece.kind, self.squareuci(sq))
                    self.movecallback(self.variantkey, self.fen, setuci)
        return piecedrop

    def buildsquares(self):
        self.container.x()
        for sq in self.squarelist():
            sqclass = choose(self.islightsquare(sq), "boardsquarelight", "boardsquaredark")
            sqdiv = Div().aac(["boardsquare", sqclass]).w(self.squaresize).h(self.squaresize)
            fasq = self.flipawaresquare(sq)
            sqdiv.pv(self.squarecoordsvect(fasq))
            sqdiv.ae("dragover", self.piecedragoverfactory(sq))
            sqdiv.ae("drop", self.piecedropfactory(sq))            
            self.container.a(sqdiv)
            p = self.getpieceatsquare(sq)
            if p.ispiece():
                pdiv = Div().ac("boardpiece").w(self.piecesize).h(self.piecesize).pv(self.piececoordsvect(fasq))
                pdiv.ac(getclassforpiece(p, self.piecestyle)).sa("draggable", True)
                pdiv.ae("dragstart", self.piecedragstartfactory(sq, pdiv))
                pdiv.ae("drag", self.piecedragfactory())
                pdiv.ae("dragend", self.piecedragendfactory(sq, pdiv))
                pdiv.ae("dragover", self.piecedragoverfactory(sq))
                pdiv.ae("drop", self.piecedropfactory(sq))            
                pdiv.zi(10)
                if self.variantkey == "threeCheck":
                    if ( p.kind == "k" ):
                        mul = self.getthreelifesforcolor(p.color)
                        lifesdiv = Div().pa().t(- self.squaresize / 10).l(self.squaresize / 2 + self.squaresize / 10).w(self.squaresize / 2).h(self.squaresize / 2)
                        lifesdiv.ac("boardthreechecklifesdiv").fs(self.squaresize / 1.5).html("{}".format(mul))
                        lifesdiv.cc(p.color == WHITE, "#ff0", "#ff0")
                        pdiv.a(lifesdiv)
                self.container.a(pdiv)

    def getthreelifesforcolor(self, color):
        parts = self.threefen.split("+")
        mul = 3
        if color == WHITE:
            try:
                mul = int(parts[2])
            except:
                print("warning, could not parse white lifes from", self.threefen)
        if color == BLACK:
            try:
                mul = int(parts[0])
            except:
                print("warning, could not parse black lifes from", self.threefen)
        return mul

    def prompiececlickedfactory(self, prompiecekind):
        def prompiececlicked():
            self.dragmove.prompiece = Piece(prompiecekind, self.turn())
            self.movecallback(self.variantkey, self.fen, self.moveuci(self.dragmove))
        return prompiececlicked

    def buildprominput(self):
        promkinds = prompiecekindsforvariantkey(self.variantkey)
        promsq = self.dragmove.tosq.copy()        
        dir = cpick(promsq.rank >= ( self.numranks / 2 ), -1, 1)
        ppks = prompiecekindsforvariantkey(self.variantkey)
        for ppk in ppks:            
            fapromsq = self.flipawaresquare(promsq)
            pp = Piece(ppk, self.turn())
            psqdiv = Div().pa().cp().zi(150).w(self.squaresize).h(self.squaresize).ac("boardpromotionsquare")
            psqdiv.pv(self.squarecoordsvect(fapromsq))
            ppdiv = Div().pa().cp().zi(200).w(self.piecesize).h(self.piecesize).ac(getclassforpiece(pp, self.piecestyle))
            ppdiv.pv(self.piececoordsvect(fapromsq)).ae("mousedown", self.prompiececlickedfactory(ppk))
            self.container.aa([psqdiv, ppdiv])
            promsq = promsq.p(Square(0, dir))

    def promotecancelclick(self):
        self.promoting = False
        self.build()

    def drawmovearrow(self, move, args = {}):                        
        if move is None:
            return
        strokecolor = args.get("strokecolor", "#FFFF00")
        linewidth = args.get("linewidth", 0.2) * self.squaresize
        headwidth = args.get("headwidth", 0.2) * self.squaresize
        headheight = args.get("headheight", 0.2) * self.squaresize        
        self.movecanvas.lineWidth(linewidth)
        self.movecanvas.strokeStyle(strokecolor)
        self.movecanvas.fillStyle(strokecolor)
        tomv = self.squarecoordsmiddlevect(self.flipawaresquare(move.tosq))
        self.movecanvas.drawline(self.squarecoordsmiddlevect(self.flipawaresquare(move.fromsq)), tomv)
        dv = Vect(headwidth, headheight)            
        self.movecanvas.fillRect(tomv.m(dv), tomv.p(dv))
        if not ( move.prompiece.isempty() ):
            pf = 4
            dvp = Vect(linewidth * pf, linewidth * pf)
            move.prompiece.color = self.turn()
            ppdiv = Div().pa().cp().ac(getclassforpiece(move.prompiece, self.piecestyle)).w(linewidth * 2 * pf).h(linewidth * 2 * pf)
            ppdiv.pv(tomv.m(dvp))            
            self.piececanvashook.a(ppdiv)

    def drawuciarrow(self, uci, args = {}):
        self.drawmovearrow(self.ucitomove(uci), args)

    def buildgenmove(self):
        if "genmove" in self.positioninfo:
            if not ( genmove == "reset" ):
                genmoveuci = self.positioninfo["genmove"]["uci"]
                genmove = self.ucitomove(genmoveuci)
                if not ( genmove is None ):
                    genmove.prompiece = Piece()
                    self.drawmovearrow(genmove)

    def build(self):
        self.sectioncontainer = Div().ac("boardsectioncontainer").w(self.outerwidth)
        self.outercontainer = Div().ac("boardoutercontainer").w(self.outerwidth).h(self.outerheight)
        self.container = Div().ac("boardcontainer").w(self.width).h(self.height).t(self.margin).l(self.margin)        
        self.outercontainer.a(self.container)        
        self.buildsquares()
        self.turndiv = Div().pa().w(self.turndivsize).h(self.turndivsize).cbc(self.iswhitesturn(), "#fff", "#000")
        if self.variantkey == "racingKings":
            self.turndiv.ct(self.flip, 0, self.outerheight - self.turndivsize).cl(xor(self.isblacksturn(), self.flip), 0, self.outerwidth - self.turndivsize)
        else:
            self.turndiv.l(self.outerwidth - self.turndivsize).ct(xor(self.isblacksturn(), self.flip), 0, self.outerheight - self.turndivsize)
        self.outercontainer.a(self.turndiv)
        if self.promoting:
            self.buildprominput()
            self.container.ae("mousedown", self.promotecancelclick)
        self.fentext = RawTextInput({}).w(self.width).fs(10).setText(self.fen)
        self.fendiv = Div().ac("boardfendiv").h(self.fendivheight).a(self.fentext)
        if self.variantkey == "crazyhouse":
            self.whitestorediv = Div().ac("boardstorediv").h(self.squaresize).w(self.outerwidth)
            self.blackstorediv = Div().ac("boardstorediv").h(self.squaresize).w(self.outerwidth)
            self.whitestore = PieceStore({
                "parent": self,
                "color": WHITE,
                "store": self.crazyfen,
                "containerdiv": self.whitestorediv
            })
            self.blackstore = PieceStore({
                "parent": self,
                "color": BLACK,
                "store": self.crazyfen,
                "containerdiv": self.blackstorediv
            })            
            if self.flip:
                self.sectioncontainer.aa([self.whitestorediv, self.outercontainer, self.blackstorediv, self.fendiv])
            else:
                self.sectioncontainer.aa([self.blackstorediv, self.outercontainer, self.whitestorediv, self.fendiv])
        else:
            self.sectioncontainer.aa([self.outercontainer, self.fendiv])
        self.x().a(self.sectioncontainer)
        self.movecanvas = Canvas(self.width, self.height).pa().t(0).l(0)
        self.movecanvashook = Div().pa().t(0).l(0).zi(5).op(0.5)
        self.piececanvashook = Div().pa().t(0).l(0).zi(11).op(0.5)
        self.container.aa([self.movecanvashook, self.piececanvashook])
        self.movecanvashook.a(self.movecanvas)
        self.buildgenmove()
        return self

    def setflip(self, flip):
        self.flip = flip
        self.build()

    def calcsizes(self):
        self.lastfile = self.numfiles - 1
        self.lastrank = self.numranks - 1
        self.area = self.numfiles * self.numranks
        self.width = self.numfiles * self.squaresize
        self.height = self.numranks * self.squaresize
        self.avgsize = ( self.width + self.height ) / 2
        self.margin = self.marginratio * self.avgsize
        self.squarepadding = self.squarepaddingratio * self.squaresize
        self.piecesize = self.squaresize - 2 * self.squarepadding
        self.outerwidth = self.width + 2 * self.margin
        self.outerheight = self.height + 2 * self.margin
        self.turndivsize = self.margin
        self.fendivheight = 25

    def parseargs(self, args):
        self.squaresize = args.get("squaresize", 45)
        self.squarepaddingratio = args.get("squarepaddingratio", 0.04)
        self.marginratio = args.get("marginratio", 0.02)
        self.numfiles = args.get("numfiles", 8)
        self.numranks = args.get("numranks", 8)        
        self.piecestyle = args.get("piecestyle", "alpha")
        self.flip = args.get("flip", False)
        self.movecallback = args.get("movecallback", None)
        self.calcsizes()

    def setpieceati(self, i, p):
        if ( i >= 0 ) and ( i < self.area ):
            self.rep[i] = p
        else:
            print("warning, rep index out of range", i)

    def getpieceati(self, i):
        if ( i >= 0 ) and ( i < self.area ):            
            return self.rep[i]
        return Piece()

    def getpieceatfilerank(self, file, rank):
        i = rank * self.numfiles + file        
        return self.getpieceati(i)

    def getpieceatsquare(self, sq):
        return self.getpieceatfilerank(sq.file, sq.rank)

    def setrepfromfen(self, fen):  
        self.fen = fen
        self.crazyfen = None
        self.threefen = None
        self.rep = [Piece() for i in range(self.area)]
        fenparts = self.fen.split(" ")
        self.rawfen = fenparts[0]
        rawfenparts = self.rawfen.split("/")        
        if self.variantkey == "crazyhouse":
            self.crazyfen = ""
            if "[" in self.rawfen:
                cfenparts = self.rawfen.split("[")
                self.rawfen = cfenparts[0]
                rawfenparts = self.rawfen.split("/")
                cfenparts = cfenparts[1].split("]")
                self.crazyfen = cfenparts[0]
        i = 0
        for rawfenpart in rawfenparts:
            pieceletters = rawfenpart.split("")
            for pieceletter in pieceletters:
                if isvalidpieceletter(pieceletter):
                    self.setpieceati(i, piecelettertopiece(pieceletter))
                    i+=1
                else:
                    mul = 0
                    try:
                        mul = int(pieceletter)                        
                    except:
                        print("warning, multiplicity could not be parsed from", pieceletter)
                    for j in range(mul):
                        self.setpieceati(i, Piece())
                        i += 1
        if i < self.area:
            print("warning, raw fen did not fill board")
        elif i > self.area:
            print("warning, raw fen exceeded board")
        self.turnfen = "w"
        if len(fenparts) > 1:
            self.turnfen = fenparts[1]
        else:
            print("warning, no turn fen")
        self.castlefen = "-"
        if len(fenparts) > 2:
            self.castlefen = fenparts[2]
        else:
            print("warning, no castle fen")
        self.epfen = "-"
        if len(fenparts) > 3:
            self.epfen = fenparts[3]
        else:
            print("warning, no ep fen")
        moveclocksi = cpick(self.variantkey == "threeCheck", 5, 4)
        self.halfmoveclock = 0
        if len(fenparts) > moveclocksi:
            try:
                self.halfmoveclock = int(fenparts[moveclocksi])
            except:
                print("warning, half move clock could not be parsed from", fenparts[4])
        else:
            print("warning, no half move fen")
        self.fullmovenumber = 1
        if len(fenparts) > ( moveclocksi + 1 ):
            try:
                self.fullmovenumber = int(fenparts[moveclocksi + 1])
            except:
                print("warning, full move number could not be parsed from", fenparts[5])
        else:
            print("warning, no full move fen")
        if self.variantkey == "threeCheck":
            if len(fenparts) > 4:
                self.threefen = fenparts[4]        
        self.promoting = False

    def turn(self):
        if self.turnfen == "w":
            return WHITE
        return BLACK

    def iswhitesturn(self):
        return self.turn() == WHITE

    def isblacksturn(self):
        return self.turn() == BLACK

    def initrep(self, args):
        self.variantkey = args.get("variantkey", "standard")
        self.setrepfromfen(args.get("fen", getstartfenforvariantkey(self.variantkey)))

    def setfromfen(self, fen, positioninfo = {}):                        
        self.positioninfo = positioninfo
        self.setrepfromfen(fen)
        self.build()                

    def reset(self):
        self.setfromfen(getstartfenforvariantkey(self.variantkey))

    def __init__(self, args):
        super().__init__("div")        
        self.positioninfo = {}
        self.parseargs(args)
        self.initrep(args)
        self.build()

class MultipvInfo(e):
    def bestmovesanclickedfactory(self, moveuci):
        def bestmovesanclicked():
            if not ( self.bestmovesanclickedcallback is None ):
                self.bestmovesanclickedcallback(moveuci)
        return bestmovesanclicked

    def scorebonus(self):
        if "scorebonus" in self.infoi:
            try:
                scorebonus = int(self.infoi["scorebonus"])
                return scorebonus
            except:
                pass
        return 0

    def effscore(self):
        return self.scorenumerical + self.scorebonus()

    def bonussliderchanged(self):
        self.infoi["scorebonus"] = self.bonusslider.v()
        self.build()            
        if not ( self.bonussliderchangedcallback is None ):            
            self.bonussliderchangedcallback()

    def build(self):        
        self.bestmoveuci = self.infoi["bestmoveuci"]
        self.bestmovesan = self.infoi["bestmovesan"]
        self.scorenumerical = self.infoi["scorenumerical"]
        self.pvsan = self.infoi["pvsan"]
        self.pvpgn = self.infoi["pvpgn"]
        self.depth = self.infoi["depth"]
        self.nps = self.infoi["nps"]
        self.container = Div().ac("multipvinfocontainer")
        self.idiv = Div().ac("multipvinfoi").html("{}.".format(self.i))
        self.bestmovesandiv = Div().ac("multipvinfobestmovesan").html(self.bestmovesan)
        self.bestmovesandiv.ae("mousedown", self.bestmovesanclickedfactory(self.bestmoveuci))
        self.scorenumericaldiv = Div().ac("multipvinfoscorenumerical").html("{}".format(self.effscore()))
        self.bonussliderdiv = Div().ac("multipvinfobonussliderdiv")
        self.bonusslider = Slider().setmin(-500).setmax(500).ac("multipvinfobonusslider").sv(self.scorebonus())
        self.bonusslider.ae("change", self.bonussliderchanged)
        self.bonussliderdiv.a(self.bonusslider)
        self.depthdiv = Div().ac("multipvinfodepth").html("{}".format(self.depth))
        self.miscdiv = Div().ac("multipvinfomisc").html("nps {}".format(self.nps))
        self.pvdiv = Div().ac("multipvinfopv").html(self.pvpgn)
        self.container.aa([self.idiv, self.bestmovesandiv, self.scorenumericaldiv, self.bonussliderdiv, self.depthdiv, self.miscdiv, self.pvdiv])        
        self.bestmovesandiv.c(scorecolor(self.effscore()))
        self.scorenumericaldiv.c(scorecolor(self.effscore()))
        self.x().a(self.container)        

    def __init__(self, infoi):
        super().__init__("div")
        self.bestmovesanclickedcallback = None
        self.bonussliderchangedcallback = None
        self.infoi = infoi
        self.i = self.infoi["i"]
        self.build()
        

class Board(e):
    def flipcallback(self):
        self.basicboard.setflip(not self.basicboard.flip)

    def resetcallback(self):
        self.basicboard.reset()

    def setfromfen(self, fen, positioninfo = {}, edithistory = True):
        restartanalysis = False
        if self.analyzing.get():
            self.stopanalyzecallback()
            restartanalysis = True
        if edithistory and ( "genmove" in positioninfo ):
            genmove = positioninfo["genmove"]
            if genmove == "reset":
                self.history = []
            else:
                self.history.append({
                    "fen": self.basicboard.fen,
                    "positioninfo": self.positioninfo
                })
        self.positioninfo = positioninfo                
        self.movelist = cpick("movelist" in self.positioninfo, self.positioninfo["movelist"], [])        
        self.basicboard.setfromfen(fen, self.positioninfo)
        self.buildpositioninfo()
        self.analysisinfodiv.x()
        if restartanalysis:
            self.analyzecallbackfactory()()
        self.getstoredanalysisinfo()

    def getstoredanalysisinfo(self):
        if not self.analyzing.get():                
            self.sioreq({"kind": "retrievedb",
                "owner": "board",
                "path": "analysisinfo/{}/{}".format(self.basicboard.variantkey, self.positioninfo["zobristkeyhex"])
            })

    def setvariantcombo(self):        
        self.variantcombo.setoptions(VARIANT_OPTIONS, self.basicboard.variantkey)

    def sioreq(self, obj):        
        if not ( self.socket is None ):            
            self.socket.emit("sioreq", obj)

    def siores(self, response):
        try:            
            dataobj = response["dataobj"]            
            if dataobj == None:
                return
            if "variantkey" in dataobj:
                self.variantchanged(dataobj["variantkey"])
            elif "analysisinfo" in dataobj:                
                self.processanalysisinfo(dataobj["analysisinfo"], True)
        except:
            print("error processing siores", response)

    def variantchanged(self, variantkey):                
        self.basicboard.variantkey = variantkey
        self.basicboard.reset()
        try:
            self.basicboard.resize(self.resizewidth, self.resizeheight)            
        except:
            pass
        try:
            self.resizetabpanewidth(self.resizewidth)
        except:
            pass
        if not ( self.variantchangedcallback is None ):
            self.variantchangedcallback(self.basicboard.variantkey)
        self.basicresize()
        self.buildpositioninfo()        
        self.setvariantcombo()
        self.sioreq({"kind": "storedb",
            "path": "board/variantkey",            
            "dataobj": {
                "variantkey": self.basicboard.variantkey
            }
        })

    def setvariantcallback(self):
        self.variantchanged(self.basicboard.variantkey)

    def moveclickedfactory(self, move):
        def moveclicked():
            if not ( self.moveclickedcallback is None ):
                self.moveclickedcallback(self.basicboard.variantkey, self.basicboard.fen, move["uci"])
        return moveclicked

    def buildpositioninfo(self):
        self.movelistdiv.x().h(self.totalheight())
        for move in self.movelist:
            movediv = Div().ac("bigboardshowmove").html(move["san"])
            movediv.ae("mousedown", self.moveclickedfactory(move))
            self.movelistdiv.a(movediv)

    def delcallback(self):
        if len(self.history) > 0:
            item = self.history.pop()
            self.setfromfen(item["fen"], item["positioninfo"], False)

    def totalheight(self):
        return self.basicboard.totalheight() + self.controlpanelheight

    def controlwidth(self):
        return max(self.basicboard.outerwidth, self.controlpanelwidth)

    def totalwidth(self):
        return self.controlwidth() + self.movelistdivwidth

    def basicresize(self):        
        self.controlpanel.w(self.controlwidth()).mw(self.controlwidth())
        self.sectioncontainer.w(self.controlwidth())
        self.tabpane.resize(None, self.totalheight())

    def resizetabpanewidth(self, width):
        self.tabpane.resize(max(width - self.totalwidth(), 600), None)

    def resize(self, width, height):
        self.resizewidth = width
        self.resizeheight = height - self.controlpanelheight
        self.basicboard.resize(self.resizewidth, self.resizeheight)
        self.basicresize()
        self.buildpositioninfo()
        self.resizetabpanewidth(width)

    def analyzecallbackfactory(self, all = False, depthlimit = None, timelimit = None):
        def analyzecallback():
            self.anyinfo = False
            self.depthlimit = depthlimit
            self.timelimit = timelimit
            self.analysisstartedat = __new__(Date()).getTime()
            self.bestmoveuci = None
            self.analyzing.set(True)
            if not ( self.enginecommandcallback is None ):            
                mpv = cpick(all, 200, self.getmultipv())
                self.enginecommandcallback("analyze {} {} {}".format(self.basicboard.variantkey, mpv, self.basicboard.fen))
            if not ( self.timelimit is None ):
                setTimeout(self.stopandstoreanalysis, self.timelimit)
        return analyzecallback

    def stopanalyzecallback(self):
        self.analyzing.set(False)
        self.basicboard.clearcanvases()
        if not ( self.enginecommandcallback is None ):
            self.enginecommandcallback("stopanalyze")

    def analysismoveclicked(self, moveuci):
        if not ( self.moveclickedcallback is None ):
            self.moveclickedcallback(self.basicboard.variantkey, self.basicboard.fen, moveuci)

    def buildanalysisinfodiv(self):
        self.analysisinfodiv.x()
        self.basicboard.clearcanvases()        
        self.maxdepth = 0
        minfos = []
        for infoi in self.analysisinfo["pvitems"]:            
            try:                   
                minfo = MultipvInfo(infoi)
                minfo.bestmovesanclickedcallback = self.analysismoveclicked
                minfo.bonussliderchangedcallback = self.buildanalysisinfodiv                
                if minfo.depth > self.maxdepth:
                    self.maxdepth = minfo.depth
                minfos.append(minfo)
            except:                
                pass        
        i = 1
        for minfo in sorted(minfos, key = lambda item: item.effscore(), reverse = True):
            minfo.i = i
            minfo.build()
            if i == 1:
                self.bestmoveuci = minfo.bestmoveuci
            iw = 1 / ( 5 * i )
            self.basicboard.drawuciarrow(minfo.bestmoveuci, {
                "strokecolor": scorecolor(minfo.effscore()),
                "linewidth": iw,
                "headheight": iw
            })
            self.analysisinfodiv.a(minfo)
            i += 1

    def processanalysisinfo(self, obj, force = False):
        if ( not self.analyzing ) and ( not force ):
            return        
        self.anyinfo = True
        elapsed = __new__(Date()).getTime() - self.analysisstartedat
        self.analysisinfo = obj        
        self.buildanalysisinfodiv()
        if ( not ( self.depthlimit is None ) ) or ( not ( self.timelimit is None ) ):
            depthok = ( not ( self.depthlimit is None ) ) and ( self.maxdepth >= self.depthlimit )
            timeok = ( not ( self.timelimit is None ) ) and ( elapsed >= self.timelimit )
            if depthok and timeok:
                self.stopandstoreanalysis()
                
    def stopandstoreanalysis(self):
        if not self.anyinfo:
            return
        self.stopanalyzecallback()
        self.storeanalysiscallback()

    def makeanalyzedmovecallback(self):
        if not ( self.bestmoveuci is None ):
            if not ( self.moveclickedcallback is None ):
                self.moveclickedcallback(self.basicboard.variantkey, self.basicboard.fen, self.bestmoveuci)

    def storeanalysiscallback(self):
        if not ( self.analysisinfo is None ):
            self.sioreq({"kind": "storedb",
                "path": "analysisinfo/{}/{}".format(self.basicboard.variantkey, self.analysisinfo["zobristkeyhex"]),            
                "dataobj": {
                    "analysisinfo": self.analysisinfo
                }
            })
        else:
            window.alert("No analysis to store.")

    def getmultipv(self):
        try:
            multipv = int(self.multipvcombo.select.v())
            return multipv
        except:
            return self.defaultmultipv

    def analyzingchangedcallback(self):
        self.analysiscontrolpanel.cbc(self.analyzing.get(), "#afa", "#edd")

    def __init__(self, args):
        super().__init__("div")
        self.depthlimit = None
        self.analysisinfo = None
        self.defaultmultipv = 3
        self.bestmoveuci = None
        self.analyzing = View(self.analyzingchangedcallback, False)
        self.history = []
        self.basicboard = BasicBoard(args)        
        self.controlpanel = Div().ac("boardcontrolpanel")
        self.controlpanelheight = getglobalcssvarpxint("--boardcontrolpanelheight")
        self.controlpanelwidth = 260
        self.controlpanel.a(Button("Flip", self.flipcallback))        
        self.variantcombo = ComboBox({
            "changecallback": self.variantchanged,            
            "selectclass": "variantselect",
            "optionfirstclass": "variantoptionfirst",
            "optionclass": "variantoption"
        })
        self.setvariantcombo()
        self.variantchangedcallback = args.get("variantchangedcallback", None)
        self.moveclickedcallback = args.get("moveclickedcallback", None)
        self.enginecommandcallback = args.get("enginecommandcallback", None)
        self.socket = args.get("socket", None)
        self.controlpanel.a(self.variantcombo).w(self.basicboard.outerwidth).mw(self.basicboard.outerwidth)
        self.controlpanel.a(Button("Del", self.delcallback))
        self.controlpanel.a(Button("Reset", self.setvariantcallback))
        self.sectioncontainer = Div().ac("bigboardsectioncontainer").w(self.basicboard.outerwidth)
        self.sectioncontainer.aa([self.controlpanel, self.basicboard])
        self.verticalcontainer = Div().ac("bigboardverticalcontainer")
        self.movelistdivwidth = 100
        self.movelistdiv = Div().ac("bigboardmovelist").w(self.movelistdivwidth).mw(self.movelistdivwidth)
        self.analysisdiv = Div()
        self.analysiscontrolpanel = Div().ac("bigboardanalysiscontrolpanel")
        self.analysiscontrolpanel.a(Button("#", self.getstoredanalysisinfo))
        self.analysiscontrolpanel.a(Button("Analyze", self.analyzecallbackfactory()))
        self.analysiscontrolpanel.a(Button("Analyze all", self.analyzecallbackfactory(True)))
        self.analysiscontrolpanel.a(Button("Quick all", self.analyzecallbackfactory(True, 10, 5000)))
        self.analysiscontrolpanel.a(Button("Stop", self.stopanalyzecallback))
        self.analysiscontrolpanel.a(Button("Make", self.makeanalyzedmovecallback))
        self.analysiscontrolpanel.a(Button("Store", self.storeanalysiscallback))
        mopts = {}
        for i in range(1,21):
            mopts[str(i)] = "MultiPV {}".format(i)
        self.multipvcombo = ComboBox({
            "selectclass": "boardmultipvcomboselect",
            "optionfirstclass": "boardmultipvcombooptionfirst",
            "optionclass": "boardmultipvcombooption"
        }).setoptions(mopts, str(self.defaultmultipv))
        self.analysiscontrolpanel.a(self.multipvcombo)
        self.analysisdiv.a(self.analysiscontrolpanel)
        self.analysisinfodiv = Div()
        self.analysisdiv.a(self.analysisinfodiv)
        self.tabpane = TabPane({"kind":"normal", "id":"board"}).setTabs(
            [
                Tab("analysis", "Analysis", self.analysisdiv),
                Tab("book", "Book", Div())
            ], "analysis"
        )    
        self.verticalcontainer.aa([self.sectioncontainer, self.movelistdiv, self.tabpane])
        self.a(self.verticalcontainer)
        self.basicresize()
        self.buildpositioninfo()
        self.sioreq({"kind": "retrievedb",
            "owner": "board",
            "path": "board/variantkey"
        })
######################################################
class DirBrowser(e):
    def __init__(self):
        super().__init__("div")
        self.pathlist = []
        self.loadpathlist(self.pathlist)

    def loadpathlist(self):        
        getjson("/dirlist/root/{}".format(self.path()), self.build, lambda err: print(err))

    def toparentdir(self):
        if len(self.pathlist) > 0:
            self.pathlist.pop()
        self.loadpathlist()

    def opendirfactory(self, name):
        def opendir():
            self.pathlist.append(name)
            self.loadpathlist()
        return opendir

    def path(self):
        return "/".join(self.pathlist)

    def namepath(self, name):
        if len(self.pathlist) <= 0:
            return name
        return "/".join([self.path(), name])

    def build(self, statsobj):
        self.x()
        sortedobj = sorted(statsobj, key = lambda item: item["name"].toLowerCase())
        #sortedobj = sorted(sortedobj, key = lambda item: item["isdir"], reverse = True)                
        if len(self.pathlist) > 0:
            self.a(Div().html("..").aac(["dirbrowseritem", "dirbrowserdir"]).ae("mousedown", self.toparentdir))
        for item in sortedobj:            
            itemdiv = Div().ac("dirbrowseritem")
            if item["isdir"]:
                itemdiv.ac("dirbrowserdir").html(item["name"]).ae("mousedown", self.opendirfactory(item["name"]))                
            else:
                itemdiv.ac("dirbrowserfile").html("<a href='/file/{}'>{}</a>".format(self.namepath(item["name"]), item["name"]))
            self.a(itemdiv)
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
            elif kind == "configstored":
                window.alert("Config storing status: " + status + ".")            
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