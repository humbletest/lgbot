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

class LinkedCheckBox(Input):
    def setchecked(self, checked):
        print("setting checked", checked)
        self.e.checked = checked
        return self

    def getchecked(self):
        return self.e.checked

    def updatevar(self):        
        self.parent[self.varname] = self.getchecked()

    def changed(self):        
        self.updatevar()

    def __init__(self, parent, varname, args = {}):
        super().__init__("checkbox")                                        
        self.parent = parent
        self.varname = varname
        self.setchecked(self.parent[self.varname])
        self.ae("change", self.changed)

class LabeledLinkedCheckBox(e):
    def __init__(self, label, parent, varname, args = {}):
        super().__init__("div")
        self.lcb = LinkedCheckBox(parent, varname, args)
        self.container = Div().ac("labeledlinkedcheckboxcontainer")
        self.ldiv = Div().html(label)
        self.container.aa([self.ldiv, self.lcb])
        self.a(self.container)

SCHEMA_WRITE_PREFERENCE_DEFAULTS = [
    {"key":"addchild","display":"Add child","default":True},
    {"key":"removechild","display":"Remove child","default":True},
    {"key":"childsopened","display":"Childs opened","default":False},
    {"key":"editenabled","display":"Edit enabled","default":True},
    {"key":"editkey","display":"Edit key","default":True},
    {"key":"editvalue","display":"Edit value","default":True},    
    {"key":"edithelp","display":"Edit help","default":True},
    {"key":"showhelpashtml","display":"Show help as HTML","default":True}
]

class SchemaWritePreference:
    def __init__(self):
        for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
            self[item["key"]] = item["default"]

    def form(self):
        formdiv = Div()
        print("dict", self.__dict__)
        fes = []        

        for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
            fes.append(LabeledLinkedCheckBox(item["display"], self, item["key"]))        

        formdiv.aa(fes)
        return formdiv

    def toobj(self):        
        obj = {}
        for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
            obj[item["key"]] = self[item["key"]]
        return obj

SCHEMA_KINDS = {
    "create" : "Create new",
    "scalar" : "Scalar",
    "list" : "List",
    "dict" : "Dict"
}

DEFAULT_HELP = "No help available for this item."
DEFAULT_ENABLED = True

class SchemaItem(e):
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

    def enablecallback(self):        
        self.enabled = self.enablecheckbox.getchecked()

    def setenabled(self, enabled):
        self.enabled = enabled
        self.enablecheckbox.setchecked(self.enabled)

    def settingsboxclicked(self):
        if self.settingsopen:
            self.settingshook.x()
            self.settingsopen = False
        else:
            self.settingsdiv = Div().ac("schemasettingsdiv").a(self.writepreference.form())
            self.settingshook.a(self.settingsdiv)
            self.settingsopen = True

    def helpboxclicked(self, event):
        event.stopPropagation()
        if self.helpopen:
            self.helphook.x()
            self.helpopen = False
        else:
            self.helpdiv = Div().ac("schemahelpdiv")
            self.helpcontentdiv = Div().ac("schemahelpcontentdiv").html(self.help)
            self.helpdiv.a(self.helpcontentdiv)
            self.helphook.a(self.helpdiv)
            self.helpopen = True

    def __init__(self, args):
        super().__init__("div")
        self.kind = "item"
        self.enabled = args.get("enabled", DEFAULT_ENABLED)
        self.help = args.get("help", DEFAULT_HELP)
        self.writepreference = SchemaWritePreference()
        self.element = Div().ac("schemaitem")
        self.schemacontainer = Div().ac("schemacontainer")
        self.enablebox = Div().ac("schemaenablebox")
        self.enablecheckbox = CheckBox(self.enabled).ae("change", self.enablecallback)
        self.enablebox.a(self.enablecheckbox)        
        self.settingsbox = Div().ac("schemasettingsbox").ae("mousedown", self.settingsboxclicked)        
        self.helpbox = Div().aac(["schemahelpbox","noselect"]).ae("mousedown", self.helpboxclicked).html("?")
        self.settingsbox.a(self.helpbox)
        self.afterelementhook = Div()
        self.settingsopen = args.get("settingsopen", False)
        self.helpopen = args.get("helpopen", False)
        self.settingshook = Div()        
        self.helphook = Div()        
        self.schemacontainer.aa([self.enablebox, self.element, self.settingsbox])     
        self.itemcontainer = Div()
        self.itemcontainer.aa([self.schemacontainer, self.helphook, self.settingshook, self.afterelementhook])
        self.a(self.itemcontainer)

class NamedSchemaItem(e):
    def textchangedcallback(self, keycode, content):        
        self.name = content

    def namedivclicked(self):
        self.editmode = not self.editmode        
        self.rawtextinput.able(self.editmode)        

    def toobj(self):        
        return {
            "kind": "nameditem",
            "name": self.name,
            "item": self.item.toobj()
        }
    
    def __init__(self, args):
        super().__init__("div")
        self.kind = "nameditem"
        self.name = args.get("name", "foo")        
        self.item = args.get("item", SchemaItem(args))
        self.editmode = args.get("editmode", False)        
        self.namedcontainer = Div().ac("namedschemaitem")
        self.namediv = Div().ac("schemaitemname")
        args["keycallback"] = self.textchangedcallback        
        self.rawtextinput = RawTextInput(args).ac("namedschemaitemrawtextinput").sv(self.name).able(self.editmode)
        self.namediv.a(self.rawtextinput)
        self.namediv.ae("mousedown", self.namedivclicked)
        self.namedcontainer.aa([self.namediv, self.item])
        self.a(self.namedcontainer)

class SchemaScalar(SchemaItem):
    def textchangedcallback(self, keycode, content):        
        self.value = content

    def divclicked(self):
        self.editmode = not self.editmode        
        self.rawtextinput.able(self.editmode)        

    def toobj(self):
        obj = self.baseobj()
        obj["value"] = self.value
        return obj

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
        self.afterelementhook.a(self.opendiv)

class SchemaList(SchemaCollection):
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

class SchemaDict(SchemaCollection):
    def toobj(self):
        dictobj = []
        for item in self.childs:
            sch = {
                "name": item.name,
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

def schemawritepreferencefromobj(obj):
    swp = SchemaWritePreference()    
    for item in SCHEMA_WRITE_PREFERENCE_DEFAULTS:
        swp[item["key"]] = getfromobj(obj, item["key"], item["default"])
    return swp

def schemafromobj(obj):    
    print("schema from obj", obj)
    kind = getfromobj(obj, "kind", "dict")
    enabled = getfromobj(obj, "enabled", DEFAULT_ENABLED)
    enabled = getfromobj(obj, "help", DEFAULT_HELP)
    writepreference = schemawritepreferencefromobj(getfromobj(obj, "writepreference", {}))
    returnobj = {}
    if kind == "scalar":        
        returnobj = SchemaScalar({
            "value": obj["value"]
        })
    elif kind == "list":
        items = obj["items"]
        childs = []
        for item in items:
            sch = schemafromobj(item)
            childs.append(sch)        
        returnobj = SchemaList({
            "childs": childs
        })
    elif kind == "dict":        
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
        returnobj = SchemaDict({
            "childs": childs
        })
    returnobj.setenabled(enabled)
    returnobj.writepreference = writepreference
    return returnobj

######################################################

