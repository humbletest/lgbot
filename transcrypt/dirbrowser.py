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
    