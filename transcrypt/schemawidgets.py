######################################################
# schema

SCHEMA_WRITE_PREFERENCE_DEFAULTS = [
    {"key":"addchild","display":"Add child","default":True},
    {"key":"removechild","display":"Remove child","default":True},
    {"key":"childsopened","display":"Childs opened","default":False},
    {"key":"editenabled","display":"Edit enabled","default":True},
    {"key":"editkey","display":"Edit key","default":True},
    {"key":"editvalue","display":"Edit value","default":True},        
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

    def helpboxclicked(self):
        event.stopPropagation()
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
        if ( not ( self.childparent is None ) ) and self.writepreference.removechild:
            self.schemacontainer.x().aa([self.enablebox, self.element, self.helpbox, self.settingsbox, self.removebox])
        else:
            self.schemacontainer.x().aa([self.enablebox, self.element, self.helpbox, self.settingsbox])

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
        self.enablecheckbox = CheckBox(self.enabled).ae("change", self.enablecallback)
        self.enablecheckbox.able(self.writepreference.editenabled)
        self.enablebox.a(self.enablecheckbox)                
        self.helpbox = Div().aac(["schemahelpbox","noselect"]).ae("mousedown", self.helpboxclicked).html("?")        
        self.settingsbox = Div().aac(["schemasettingsbox","noselect"]).ae("mousedown", self.settingsboxclicked).html("S")
        self.removebox = Div().aac(["schemaremovebox","noselect"]).ae("mousedown", self.removeboxclicked).html("X")        
        self.afterelementhook = Div()
        self.settingsopen = args.get("settingsopen", False)
        self.helpopen = args.get("helpopen", False)
        self.settingshook = Div()        
        self.helphook = Div()        
        self.schemacontainer.aa([self.enablebox, self.element, self.helpbox, self.settingsbox])
        self.itemcontainer = Div()
        self.itemcontainer.aa([self.schemacontainer, self.helphook, self.settingshook, self.afterelementhook])
        self.a(self.itemcontainer)

class NamedSchemaItem(e):
    def toobj(self):        
        return {
            "kind": "nameditem",
            "key": self.key,
            "item": self.item.toobj()
        }

    def writepreferencechangedtask(self):
        self.linkedtextinput.able(self.item.writepreference.editkey)
    
    def __init__(self, args):
        super().__init__("div")
        self.kind = "nameditem"
        self.key = args.get("key", "foo")        
        self.item = args.get("item", SchemaItem(args))        
        self.item.parent = self
        self.namedcontainer = Div().ac("namedschemaitem")
        self.namediv = Div().ac("schemaitemname")        
        self.linkedtextinput = LinkedTextInput(self, "key", {"textclass":"namedschemaitemrawtextinput"})
        self.linkedtextinput.setText(self.key)
        self.linkedtextinput.able(self.item.writepreference.editkey)
        self.namediv.a(self.linkedtextinput)        
        self.namedcontainer.aa([self.namediv, self.item])
        self.a(self.namedcontainer)

class SchemaScalar(SchemaItem):
    def toobj(self):
        obj = self.baseobj()
        obj["value"] = self.value
        return obj

    def writepreferencechangedtask(self):
        self.linkedtextinput.able(self.writepreference.editvalue)        

    def __init__(self, args):
        super().__init__(args)
        self.kind = "scalar"        
        self.value = args.get("value", "bar")        
        self.element.ac("schemascalar")
        args["keycallback"] = self.textchangedcallback
        self.linkedtextinput = LinkedTextInput(self, "value", {"textclass":"schemascalarrawtextinput"})
        self.linkedtextinput.setText(self.value)        
        self.linkedtextinput.able(self.writepreference.editvalue)        
        self.element.ae("mousedown", self.divclicked)
        self.element.aa([self.linkedtextinput])
        self.writepreference.setdisabledlist(["addchild","removechild","childsopened"])

class SchemaCollection(SchemaItem):
    def buildchilds(self):
        self.childshook.x()
        for child in self.childs:
            self.childshook.a(child)

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

    def createcallback(self, key):
        self.createcombo.setoptions(SCHEMA_KINDS)
        sch = SchemaScalar({})
        if key == "list":
            sch = SchemaList({})
        elif key == "dict":
            sch = SchemaDict({})
        sch.setchildparent(self)
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
            if self.writepreference.addchild:
                self.createhook.a(self.creatediv)
            self.openbutton.ac("schemacollectionopenbuttondone")
            self.buildchilds()

    def writepreferencechangedtask(self):
        self.opened = True
        self.openchilds()
        self.opened = not self.writepreference.childsopened
        self.openchilds()

    def __init__(self, args):
        super().__init__(args)
        self.kind = "collection"        
        self.opened = False
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
        if self.writepreference.childsopened:
            self.openchilds()

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
        self.writepreference.setdisabledlist(["editvalue"])

class SchemaDict(SchemaCollection):
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
        self.writepreference.setdisabledlist(["editvalue"])

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
    returnobj.setenabled(enabled)    
    returnobj.help = help    
    return returnobj

######################################################

