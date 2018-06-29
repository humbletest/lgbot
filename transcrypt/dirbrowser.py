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
            updiv = Div().aac(["dirbrowseritem", "dirbrowserdir"]).ae("mousedown", self.toparentdir)
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
            self.a(itemdiv)            
