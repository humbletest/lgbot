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

#https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/

class FileUploader(e):
    def fileinputchanged(self):
        self.files = self.fileinput.files()
        self.handlefiles()

    def preventdefaults(self, ev):
        ev.preventDefault()
        ev.stopPropagation()

    def highlight(self):
        self.droparea.ac("highlight")

    def unhighlight(self):
        self.droparea.rc("highlight")

    def log(self, html):
        self.infoitems.append(html)
        self.infoitems.reverse()
        self.info.html("<br>".join(self.infoitems))
        self.infoitems.reverse()

    def loginfo(self, content):
        try:
            json = JSON.parse(content)
            if json["success"]:
                path = "/uploads/{}".format(json["savefilename"])                
                self.log("uploaded <span class='fileuploadfilename'>{}</span> <a href='{}' target='_blank' rel='noopener noreferrer'>{}</a>".format(json["filename"], path, path))    
            else:
                self.log("File upload failed.", json["status"])
        except:            
            self.log("Error parsing response as JSON.")

    def uploadfile(self, file):        
        if self.url is None:
            print("no upload url")
            return

        formdata = __new__ (FormData())

        formdata.append('files', file)

        __pragma__("jsiter")

        args = {
            "method": 'POST',
            "body": formdata
        }

        __pragma__("nojsiter")

        fetch(self.url, args).then(
            lambda response: response.text().then(
                lambda content: self.loginfo(content),
                lambda err: self.loginfo(err)    
            ),
            lambda err: self.loginfo(err)
        )

    def handlefiles(self, files = self.files):
        for i in range(files.length):
            print("uploading file {}".format(i))
            self.uploadfile(files.item(i))

    def handledrop(self, ev):
        self.dt = ev.dataTransfer
        self.files = self.dt.files

        self.handlefiles()

    def build(self):
        self.x()
        self.droparea = Div().ac("fileuploaddroparea")
        self.form = Form().ac("fileuploadform")
        self.desc = P().ac("fileuploadp").html("Upload {}s with the file dialog or by dragging and dropping them onto the dashed region".format(self.acceptdisplay))
        self.fileinput = FileInput().ac("fileuploadfileelem").setmultiple(self.multiple).setaccept(self.accept)        
        self.fileinput.sa("id", "fileinputelement")
        self.fileinput.ae("change", self.fileinputchanged)
        self.button = Label().ac("fileuploadbutton").sa("for", "fileinputelement").html("Select some {}s".format(self.acceptdisplay))
        self.form.aa([self.desc, self.fileinput, self.button])
        self.droparea.a(self.form)
        for eventname in ["dragenter", "dragover", "dragleave", "drop"]:
            self.droparea.aef(eventname, self.preventdefaults)
        for eventname in ["dragenter", "dragover"]:
            self.droparea.aef(eventname, self.highlight)
        for eventname in ["dragleave", "drop"]:
            self.droparea.aef(eventname, self.unhighlight)
        self.droparea.aef("drop", self.handledrop)
        self.info = Div().ac("fileuploadinfo")
        self.infoitems = []
        self.aa([self.droparea, self.info])

    def __init__(self, args = {}):
        super().__init__("div")
        self.url = args.get("url", None)
        self.multiple = args.get("multiple", True)
        self.accept = args.get("accept", "image/*")
        self.acceptdisplay = args.get("acceptdisplay", "image")
        self.build()

######################################################

