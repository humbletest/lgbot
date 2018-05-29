__pragma__("jsiter")

def putjsonbin(json, callback, id = None):
    method = "POST"
    url = "https://api.jsonbin.io/b"        
    if not ( id is None ):
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
            lambda content: callback(json, content),
            lambda err: print(err)
        ),
        lambda err: print(err)
        )
    

def getjsonbin(id, callback, version = "latest"):
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
            lambda err: print(err)
        ),
        lambda err: print(err)
        )

__pragma__("nojsiter")######################################################
# dom
def ce(tag):
    return document.createElement(tag)

def ge(id):
    return document.getElementById(id)

def addEventListener(object, kind, callback):
    object.addEventListener(kind, callback, False)

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
        self.html("")
        return self

    # width
    def w(self, w):
        self.e.style.width = w + "px"
        return self

    # height
    def h(self, h):
        self.e.style.height = h + "px"
        return self

    # top
    def t(self, t):
        self.e.style.top = t + "px"
        return self

    # left
    def l(self, l):
        self.e.style.left = l + "px"
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

    # remove class
    def rc(self, klass):
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
        self.sa("type",kind)

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
######################################################

######################################################
# constants
WINDOW_SAFETY_MARGIN = 10
######################################################

######################################################
# widgets
class Button(Input):
    def __init__(self, caption, callback = None):
        super().__init__("button")        
        self.sv(caption)
        if not ( callback is None):
            self.ae("mousedown", callback)

class RawTextInput(Input):
    def keyup(self, ev):
        if not ( self.callback is None ):
            if ev.keyCode == 13:
                if not ( self.entercallback is None ):
                    self.entercallback(self.v())
            else:
                if not ( self.keycallback is None ):
                    self.keycallback(ev.keyCode, self.v())

    def __init__(self, args):
        super().__init__("text")                
        self.entercallback = args.get("entercallback", None)
        self.keycallback = args.get("keycallback", None)
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
        tinpclass = args.get("tinpclass", "textinputtext")
        sbtnclass = args.get("sbtnclass", "textinputbutton")
        self.container = Div().ac(contclass)
        self.onsubmitcallback = args.get("submitcallback", None)
        args["entercallback"] = self.submitcallback
        self.tinp = RawTextInput(args).ac(tinpclass)
        self.sbtn = Button("Submit", self.submitcallback).ac(sbtnclass)        
        self.container.aa([self.tinp, self.sbtn])
        self.a(self.container)

    def focus(self):
        self.tinp.fl()
        return self

class LogItem(e):
    def __init__(self, content, kind = "normal"):
        super().__init__("div")
        tdiv = Div().ac("logtimediv").html("{}".format(__new__ (Date()).toLocaleString()))
        cdiv = Div().ac("logcontentdiv").html(content)
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

class Tab(e):
    def __init__(self, key, displayname, element):
        self.key = key
        self.displayname = displayname
        self.element = element
        self.tabelement = None

class TabPane(e):
    def __init__(self, args):        
        super().__init__("div")
        self.kind = args.get("kind", "child")
        self.width = args.get("width", 600)
        self.height = args.get("height", 400)
        self.marginleft = args.get("marginleft", 0)
        self.margintop = args.get("margintop", 0)
        self.tabsheight = args.get("tabsheight", 40)
        if self.kind == "main":
            self.width = window.innerWidth - 2 * WINDOW_SAFETY_MARGIN
            self.height = window.innerHeight - 2 * WINDOW_SAFETY_MARGIN
            self.marginleft = WINDOW_SAFETY_MARGIN
            self.margintop = WINDOW_SAFETY_MARGIN
        self.contentheight = self.height - self.tabsheight
        self.tabsdiv = Div().ac("tabpanetabsdiv").w(self.width).h(self.tabsheight)
        self.contentdiv = Div().ac("tabpanecontentdiv").w(self.width).h(self.contentheight)
        self.container = Div().ac("tabpanecontainer").w(self.width).h(self.height).ml(self.marginleft).mt(self.margintop)
        self.container.aa([self.tabsdiv, self.contentdiv])        
        self.a(self.container)        
        self.tabs = []
        self.seltab = None

    def tabSelectedCallback(self, tab):
        self.selectByKey(tab.key)
        pass

    def setTabs(self, tabs, key):
        self.tabs = tabs
        self.tabsdiv.x()
        for tab in self.tabs:
            tabelement = Div().ac("tabpanetab").html(tab.displayname)
            self.tabsdiv.a(tabelement)
            tab.tabelement = tabelement
            tab.tabelement.ae("mousedown", self.tabSelectedCallback.bind(self, tab))
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

    def setTabElementByKey(self, key, tabelement, show = True):
        tab = self.getTabByKey(key)
        if tab == None:
            return self
        tab.element = tabelement        
        if show:
            self.contentdiv.x().a(tab.element)    
        return self

    def selectByKey(self, key):
        self.seltab = self.getTabByKey(key, True)
        if self.seltab == None:
            return self
        self.contentdiv.x().a(self.seltab.element)
        return self

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
        self.select = Select().ac(self.selectclass)
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

SCHEMA_KINDS = {
    "create" : "Create new",
    "scalar" : "Scalar",
    "list" : "List",
    "dict" : "Dict"
}

class SchemaItem(e):
    def toobj(self):
        return {
            "kind": "schemaitem"
        }

    def __init__(self, args):
        super().__init__("div")
        self.kind = "item"
        self.element = Div().ac("schemaitem")
        self.a(self.element)

class NamedSchemaItem(e):
    def textchangedcallback(self, keycode, content):        
        self.name = content

    def namedivclicked(self):
        self.editmode = not self.editmode        
        self.rawtextinput.able(self.editmode)        

    def toobj(self):
        return {
            "kind": "namedschemaitem",
            "name": self.name,
            "item": self.item.toobj()
        }
    
    def __init__(self, args):
        super().__init__("div")
        self.kind = "nameditem"
        self.name = args.get("name", "foo")        
        self.item = args.get("item", SchemaItem(args))
        self.editmode = args.get("editmode", False)        
        self.element = Div().ac("namedschemaitem")
        self.namediv = Div().ac("schemaitemname")
        args["keycallback"] = self.textchangedcallback        
        self.rawtextinput = RawTextInput(args).ac("namedschemaitemrawtextinput").sv(self.name).able(self.editmode)
        self.namediv.a(self.rawtextinput)
        self.namediv.ae("mousedown", self.namedivclicked)
        self.element.aa([self.namediv, self.item])
        self.a(self.element)

class SchemaScalar(SchemaItem):
    def textchangedcallback(self, keycode, content):        
        self.value = content

    def divclicked(self):
        self.editmode = not self.editmode        
        self.rawtextinput.able(self.editmode)        

    def toobj(self):
        return {
            "kind": "schemascalar",
            "value": self.value
        }

    def __init__(self, args):
        super().__init__(args)
        self.kind = "scalar"        
        self.value = args.get("value", "bar")
        self.editmode = args.get("editmode", False)                
        self.element.ac("schemascalar")
        args["keycallback"] = self.textchangedcallback
        self.rawtextinput = RawTextInput(args).ac("schemascalarrawtextinput").sv(self.value).able(self.editmode)        
        self.element.ae("mousedown", self.divclicked)
        self.element.aa([self.rawtextinput])
        self.a(self.element)

class SchemaCollection(SchemaItem):
    def buildchilds(self):
        self.childshook.x()
        for child in self.childs:
            self.childshook.a(child)

    def createcallback(self, key):
        self.createcombo.setoptions(SCHEMA_KINDS)
        sch = SchemaScalar({})
        if key == "list":
            sch = SchemaList({})
        elif key == "dict":
            sch = SchemaDict({})
        appendelement = sch
        if self.kind == "dict":
            appendelement = NamedSchemaItem({
                "item": sch
            })
        self.childs.append(appendelement)
        self.buildchilds()

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
                "changecallback": self.createcallback
            })
            self.createcombo.setoptions(SCHEMA_KINDS)
            self.creatediv.a(self.createcombo)
            self.createhook.a(self.creatediv)
            self.openbutton.ac("schemacollectionopenbuttondone")
            self.buildchilds()

    def __init__(self, args):
        super().__init__(args)
        self.kind = "collection"
        self.name = args.get("name", "SchemaCollection")
        self.opened = args.get("opened", False)
        self.childs = args.get("childs", [])
        self.editmode = args.get("editmode", False)        
        self.childseditable = args.get("childseditable", True)
        self.element.ac("schemacollection")                
        self.openbutton = Div().ac("schemacollectionopenbutton").ae("mousedown", self.openchilds)
        self.element.aa([self.openbutton])        
        self.createhook = Div()
        self.childshook = Div()
        self.opendiv = Div().ac("schemacollectionopendiv")
        self.opendiv.aa([self.createhook, self.childshook])
        self.container = Div()
        self.container.aa([self.element, self.opendiv])
        self.a(self.container)

class SchemaList(SchemaCollection):
    def toobj(self):
        obj = []
        for item in self.childs:
            obj.append(item.toobj())
        return {
            "kind": "schemalist",
            "items": obj
        }

    def __init__(self, args):
        super().__init__(args)        
        self.kind = "list"
        self.element.ac("schemalist")

class SchemaDict(SchemaCollection):
    def toobj(self):
        obj = []
        for item in self.childs:
            sch = {
                "name": item.name,
                "item": item.item.toobj()
            }
            obj.append(sch)
        return {
            "kind": "schemadict",
            "items": obj
        }

    def __init__(self, args):
        super().__init__(args)        
        self.kind = "dict"
        self.element.ac("schemadict")

def schemafromobj(obj):
    kind = obj["kind"]
    if kind == "schemascalar":        
        return SchemaScalar({
            "value": obj["value"]
        })
    elif kind == "schemalist":
        items = obj["items"]
        childs = []
        for item in items:
            sch = schemafromobj(item)
            childs.append(sch)        
        return SchemaList({
            "childs": childs
        })
    elif kind == "schemadict":        
        items = obj["items"]
        childs = []
        for itemobj in items:
            name = itemobj["name"]
            item = itemobj["item"]
            sch = schemafromobj(item)
            namedsch = NamedSchemaItem({
                "name": name,
                "item": sch
            })
            childs.append(namedsch)        
        return SchemaDict({
            "childs": childs
        })

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

if "id" in queryparams:    
    id = queryparams["id"]
    getjsonbin(id, getbincallback)

srcdiv = Div()
schemajson = None
######################################################

######################################################
# client functions
def docwln(content):    
    li = LogItem("<pre>" + content + "</pre>")
    mainlog.log(li)    

def cmdinpcallback(cmd):
    socket.emit('sioreq', {"kind":"cmd", "data": cmd})

def serializeputjsonbincallback(json, content):        
    try:
        obj = JSON.parse(content)        
        binid = None
        if "id" in obj:
            binid = obj["id"]                
        if "parentId" in obj:
            binid = obj["parentId"]                
        if binid is None:
            print("no binid")
        else:            
            href = window.location.protocol + "//" + window.location.host + "/?id=" + binid
            print("href", href)
            document.location.href = href
            pass
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

startup()

