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

    def selectByKey(self, key):
        if len(self.tabs) == 0:
            self.seltab = None
            return self
        self.seltab = self.tabs[0]
        for tab in self.tabs:
            tab.tabelement.rc("tabpaneseltab")
            if tab.key == key:
                self.seltab = tab                                
                tab.tabelement.ac("tabpaneseltab")
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
    def __init__(self, args):
        super().__init__("div")
        self.element = Div().ac("schemaitem")
        self.a(self.element)

class SchemaCollection(SchemaItem):
    def textchangedcallback(self, keycode, content):        
        self.name = content
        pass

    def buildchilds(self):
        self.childshook.x()
        for child in self.childs:
            self.childshook.a(child)

    def createcallback(self, key):
        self.createcombo.setoptions(SCHEMA_KINDS)
        sch = SchemaCollection({})
        if key == "scalar":
            sch = SchemaItem({})
        self.childs.append(sch)
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
        self.name = args.get("name", "SchemaCollection")
        self.opened = args.get("opened", False)
        self.childs = args.get("childs", [])
        self.editmode = args.get("editmode", False)        
        self.childseditable = args.get("childseditable", True)
        self.element.ac("schemacollection")
        args["keycallback"] = self.textchangedcallback
        self.rawtextinput = RawTextInput(args).ac("schemacollectionrawtextinput").sv(self.name).able(self.editmode)
        self.openbutton = Div().ac("schemacollectionopenbutton").ae("mousedown", self.openchilds)
        self.element.aa([self.rawtextinput, self.openbutton])        
        self.createhook = Div()
        self.childshook = Div()
        self.opendiv = Div().ac("schemacollectionopendiv")
        self.opendiv.aa([self.createhook, self.childshook])
        self.container = Div()
        self.container.aa([self.element, self.opendiv])
        self.a(self.container)

######################################################

