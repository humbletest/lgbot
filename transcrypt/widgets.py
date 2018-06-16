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
        self.cdiv.html(self.content)
        if self.kind == "cmd":
            self.cdiv.ac("logcontentcmd")
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
        self.maxitems = args.get("maxitems", 20)
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

    def resize(self):
        if self.kind == "main":
            self.width = window.innerWidth - 2 * WINDOW_SAFETY_MARGIN
            self.height = window.innerHeight - 2 * WINDOW_SAFETY_MARGIN
            self.marginleft = WINDOW_SAFETY_MARGIN
            self.margintop = WINDOW_SAFETY_MARGIN
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
        pass

    def setTabs(self, tabs, key):
        self.tabs = tabs
        self.tabsdiv.x()
        for tab in self.tabs:
            tabelement = Div().aac(["tabpanetab","noselect"]).html(tab.displayname)
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

    def innercontentheight(self):
        return self.contentheight - SCROLL_BAR_WIDTH

    def innercontentwidth(self):
        return self.width - SCROLL_BAR_WIDTH

    def resizecontent(self, element):
        try:
            element.resize(self.innercontentwidth(), self.innercontentheight())
        except:
            pass

    def setTabElementByKey(self, key, tabelement):
        tab = self.getTabByKey(key)
        if tab == None:
            return self
        tab.element = tabelement        
        self.resizecontent(tab.element)
        return self

    def selectByKey(self, key):
        self.seltab = self.getTabByKey(key, True)
        if self.seltab == None:
            return self
        element = self.seltab.element
        self.contentdiv.x().a(element)
        self.resizecontent(element)       
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
        self.e.checked = checked
        return self

    def getchecked(self):
        return self.e.checked

    def updatevar(self):        
        self.parent[self.varname] = self.getchecked()

    def changed(self):        
        self.updatevar()
        if not ( self.changecallback is None):
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
        self.rawtextinputclass = args.get("textclass", "defaultlinkedtextinputtext")
        self.rawtextinput = RawTextInput({
            "keycallback": self.keyup,
            "tinpclass": self.rawtextinputclass
        })
        self.text = args.get("text", "")        
        self.setText(self.text)
        patchclasses(self, args)
        self.keyupcallback = args.get("keyupcallback", None)
        self.a(self.rawtextinput)

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

