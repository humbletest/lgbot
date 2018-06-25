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
        print(schemaclipboard.toobj())
    
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
        self.key = args.get("key", uid())
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
        self.item = item
        self.key = None
        if not ( self.item.parent is None ):
            self.key = self.item.parent.key
        self.item.setparent(None)

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
        self.value = args.get("value", randscalarvalue(2, 8))
        self.minvalue = args.get("minvalue", 1)        
        self.maxvalue = args.get("maxvalue", 100)        
        self.element.ac("schemascalar")        
        self.writepreference.setdisabledlist(["addchild","childsopened","radio"])
        self.build()

class SchemaCollection(SchemaItem):
    def parentsettask(self):
        print("pst")
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

