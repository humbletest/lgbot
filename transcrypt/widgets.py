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

