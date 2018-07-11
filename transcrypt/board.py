class Board(e):
    def flipcallback(self):
        self.basicboard.setflip(not self.basicboard.flip)

    def resetcallback(self):
        self.basicboard.reset()

    def setfromfen(self, fen, positioninfo = {}, edithistory = True):
        restartanalysis = False
        if self.analyzing.get():
            self.stopanalyzecallback()
            restartanalysis = True
        if edithistory and ( "genmove" in positioninfo ):
            genmove = positioninfo["genmove"]
            if genmove == "reset":
                self.history = []
            else:
                self.history.append({
                    "fen": self.basicboard.fen,
                    "positioninfo": self.positioninfo
                })
        self.positioninfo = positioninfo                
        self.movelist = cpick("movelist" in self.positioninfo, self.positioninfo["movelist"], [])        
        self.basicboard.setfromfen(fen, self.positioninfo)
        self.buildpositioninfo()
        self.analysisinfodiv.x()
        if restartanalysis:
            self.analyzecallbackfactory()()
        self.getstoredanalysisinfo()

    def getstoredanalysisinfo(self):
        if not self.analyzing.get():                
            self.sioreq({"kind": "retrievedb",
                "owner": "board",
                "path": "analysisinfo/{}/{}".format(self.basicboard.variantkey, self.positioninfo["zobristkeyhex"])
            })

    def setvariantcombo(self):        
        self.variantcombo.setoptions(VARIANT_OPTIONS, self.basicboard.variantkey)

    def sioreq(self, obj):        
        if not ( self.socket is None ):            
            self.socket.emit("sioreq", obj)

    def posclickedfactory(self, i):
        def poslicked():
            self.gamei = i
            pinfo = self.positioninfos[i]
            self.setfromfen(pinfo["fen"], pinfo["positioninfo"])
            for j in range(len(self.positioninfos)):
                self.posdivs[j].arc(j == self.gamei, "boardposdivselected")                                                
        return poslicked

    def selectgamei(self, i):
        if len(self.positioninfos) > 0:
            self.posclickedfactory(i)()            

    def gametobegin(self):
        self.gamei = 0
        self.selectgamei(self.gamei)            

    def gameback(self):
        self.gamei -= 1
        if self.gamei < 0:
            self.gamei = 0
        self.selectgamei(self.gamei)            

    def gameforward(self):
        self.gamei += 1
        if self.gamei >= len(self.positioninfos):
            self.gamei = len(self.positioninfos) - 1
        self.selectgamei(self.gamei)            

    def gametoend(self):
        self.gamei = len(self.positioninfos) - 1
        self.selectgamei(self.gamei)            

    def buildgame(self):
        self.gamediv.x()        
        self.posdivs = []
        i = 0
        for pinfo in self.positioninfos:
            fen = pinfo["fen"]
            posinfo = pinfo["positioninfo"]
            genmove = "*"
            if "genmove" in posinfo:
                genmove = posinfo["genmove"]["san"]
            posdiv = Div().ac("boardposdiv")
            self.posdivs.append(posdiv)
            posdiv.ae("mousedown", self.posclickedfactory(i))            
            movediv = Div().ac("boardposmovediv").html(genmove)
            fendiv = Div().ac("boardposfendiv")
            showboard = BasicBoard({
                "show": True,
                "showfen": False,
                "positioninfo": posinfo,
                "fen": fen,
                "squaresize": 20,
                "flip": self.flip
            })
            fendiv.a(showboard)
            posdiv.aa([movediv, fendiv])
            self.gamediv.a(posdiv)
            i += 1
        self.gamei = 0
        self.selectgamei(self.gamei)

    def siores(self, response):
        try:                        
            if "dataobj" in response:
                dataobj = response["dataobj"]            
                if "variantkey" in dataobj:
                    self.variantchanged(dataobj["variantkey"])
                elif "analysisinfo" in dataobj:                
                    self.processanalysisinfo(dataobj["analysisinfo"], True)                
            
            if "historyobj" in response:
                historyobj = response["historyobj"]
                uci_variant = historyobj["uci_variant"]
                chess960 = historyobj["chess960"]
                pgn = historyobj["pgn"]
                pgninfo = PgnInfo(self).setcontent(pgn)
                vk = uci_variant_to_variantkey(uci_variant, chess960)
                self.variantchanged(vk, False)         
                self.flip = pgninfo.meblack()
                self.basicboard.setflip(self.flip)
                self.positioninfos = historyobj["positioninfos"]
                self.buildgame()
                self.tabpane.selectByKey("analysis")
        except:
            print("error processing siores", response)

    def variantchanged(self, variantkey, docallback = True):                
        self.basicboard.variantkey = variantkey
        self.basicboard.reset()
        try:
            self.basicboard.resize(self.resizewidth, self.resizeheight)            
        except:
            pass
        try:
            self.resizetabpanewidth(self.resizewidth)
        except:
            pass
        if ( not ( self.variantchangedcallback is None ) ) and ( docallback ):
            self.variantchangedcallback(self.basicboard.variantkey)
        self.basicresize()
        self.buildpositioninfo()        
        self.setvariantcombo()
        self.sioreq({"kind": "storedb",
            "path": "board/variantkey",            
            "dataobj": {
                "variantkey": self.basicboard.variantkey
            }
        })

    def setvariantcallback(self):
        self.variantchanged(self.basicboard.variantkey)

    def moveclickedfactory(self, move):
        def moveclicked():
            if not ( self.moveclickedcallback is None ):
                self.moveclickedcallback(self.basicboard.variantkey, self.basicboard.fen, move["uci"])
        return moveclicked

    def buildpositioninfo(self):
        self.movelistdiv.x().h(self.totalheight())
        for move in self.movelist:
            movediv = Div().ac("bigboardshowmove").html(move["san"])
            movediv.ae("mousedown", self.moveclickedfactory(move))
            self.movelistdiv.a(movediv)

    def delcallback(self):
        if len(self.history) > 0:
            item = self.history.pop()
            self.setfromfen(item["fen"], item["positioninfo"], False)

    def totalheight(self):
        return self.basicboard.totalheight() + self.controlpanelheight

    def controlwidth(self):
        return max(self.basicboard.outerwidth, self.controlpanelwidth)

    def totalwidth(self):
        return self.controlwidth() + self.movelistdivwidth

    def basicresize(self):        
        self.controlpanel.w(self.controlwidth()).mw(self.controlwidth())
        self.sectioncontainer.w(self.controlwidth())
        self.tabpane.resize(None, self.totalheight())

    def resizetabpanewidth(self, width):
        self.tabpane.resize(max(width - self.totalwidth(), 600), None)

    def resizetask(self):
        self.resizewidth = self.resizeorigwidth
        self.resizeheight = self.resizeorigheight - self.controlpanelheight
        self.basicboard.resize(self.resizewidth, self.resizeheight)
        self.basicresize()
        self.buildpositioninfo()
        self.resizetabpanewidth(self.resizeorigwidth)

    def resize(self, width, height):
        self.resizeorigwidth = width
        self.resizeorigheight = height        
        self.resizetask()

    def analyzecallbackfactory(self, all = False, depthlimit = None, timelimit = None):
        def analyzecallback():
            self.anyinfo = False
            self.depthlimit = depthlimit
            self.timelimit = timelimit
            self.analysisstartedat = __new__(Date()).getTime()
            self.bestmoveuci = None
            self.analyzing.set(True)
            if not ( self.enginecommandcallback is None ):            
                mpv = cpick(all, 200, self.getmultipv())
                self.enginecommandcallback("analyze {} {} {}".format(self.basicboard.variantkey, mpv, self.basicboard.fen))            
        return analyzecallback

    def stopanalyzecallback(self):
        self.analyzing.set(False)
        self.basicboard.clearcanvases()
        if not ( self.enginecommandcallback is None ):
            self.enginecommandcallback("stopanalyze")

    def analysismoveclicked(self, moveuci):
        if not ( self.moveclickedcallback is None ):
            self.moveclickedcallback(self.basicboard.variantkey, self.basicboard.fen, moveuci)

    def buildanalysisinfodiv(self):
        self.analysisinfodiv.x()
        self.basicboard.clearcanvases()        
        self.maxdepth = 0
        minfos = []
        for infoi in self.analysisinfo["pvitems"]:            
            try:                   
                minfo = MultipvInfo(infoi)
                minfo.bestmovesanclickedcallback = self.analysismoveclicked
                minfo.bonussliderchangedcallback = self.buildanalysisinfodiv                
                if minfo.depth > self.maxdepth:
                    self.maxdepth = minfo.depth
                minfos.append(minfo)
            except:                
                pass        
        i = 1
        for minfo in sorted(minfos, key = lambda item: item.effscore(), reverse = True):
            minfo.i = i
            minfo.build()
            if i == 1:
                self.bestmoveuci = minfo.bestmoveuci
            iw = 1 / ( 5 * i )
            self.basicboard.drawuciarrow(minfo.bestmoveuci, {
                "strokecolor": scorecolor(minfo.effscore()),
                "linewidth": iw,
                "headheight": iw
            })
            self.analysisinfodiv.a(minfo)
            i += 1

    def processanalysisinfo(self, obj, force = False):
        if ( not self.analyzing ) and ( not force ):
            return        
        self.anyinfo = True
        elapsed = __new__(Date()).getTime() - self.analysisstartedat
        self.analysisinfo = obj        
        self.buildanalysisinfodiv()        
        if ( self.analyzing.get() ) and ( not ( self.depthlimit is None ) ) or ( not ( self.timelimit is None ) ):
            depthok = ( self.depthlimit is None ) or ( self.maxdepth >= self.depthlimit )
            timeok = ( self.timelimit is None ) or ( elapsed >= self.timelimit )
            if depthok and timeok:
                self.stopandstoreanalysis()
                
    def stopandstoreanalysis(self):
        self.stopanalyzecallback()
        if not self.anyinfo:
            return
        self.storeanalysiscallback()

    def makeanalyzedmovecallback(self):
        if not ( self.bestmoveuci is None ):
            if not ( self.moveclickedcallback is None ):
                self.moveclickedcallback(self.basicboard.variantkey, self.basicboard.fen, self.bestmoveuci)

    def storeanalysiscallback(self):
        if not ( self.analysisinfo is None ):
            self.sioreq({"kind": "storedb",
                "path": "analysisinfo/{}/{}".format(self.basicboard.variantkey, self.analysisinfo["zobristkeyhex"]),            
                "dataobj": {
                    "analysisinfo": self.analysisinfo
                }
            })
        else:
            window.alert("No analysis to store.")

    def getmultipv(self):
        try:
            multipv = int(self.multipvcombo.select.v())
            return multipv
        except:
            return self.defaultmultipv

    def analyzingchangedcallback(self):
        self.analysiscontrolpanel.cbc(self.analyzing.get(), "#afa", "#edd")

    def getconfigscalar(self, path, default):
        if self.configschema is None:
            return default
        found = getscalarfromschema(self.configschema, path)
        if found is None:
            return default
        return found

    def getconfigbool(self, path, default):
        s = self.getconfigscalar(path, None)
        if s is None:
            return default
        if s == "true":
            return True
        if s == "false":
            return False
        return default

    def gamesloadedok(self, content):
        self.pgnlist = PgnList(self).setcontent(content)
        self.gamesdiv.x()
        self.gamesdiv.a(Button("Reload", self.loadgames))        
        self.gamesdiv.a(self.gamesloadingdiv.x())
        self.gamesdiv.a(self.pgnlist)

    def loadgames(self):
        self.gamesloadingdiv.html("Games loading...")
        if not ( self.username is None ):
            lichapiget("games/export/{}?max=25".format(self.username), self.usertoken, self.gamesloadedok, lambda err: print(err))

    def setconfigschema(self, configschema):
        self.configschema = configschema
        self.username = self.getconfigscalar("global/username", None)
        self.usertoken = self.getconfigscalar("global/usertoken", None)
        self.showfen = self.getconfigbool("global/showfen", True)        
        self.basicboard.showfen = self.showfen
        self.resizetask()
        self.loadgames()

    def storeforward(self):        
        self.storeanalysiscallback()
        self.gameforward()

    def storemake(self):
        self.storeanalysiscallback()
        self.makeanalyzedmovecallback()

    def __init__(self, args):
        super().__init__("div")
        self.resizeorigwidth = 800
        self.resizeorigheight = 400
        self.showfen = True
        self.flip = False
        self.gamesloadingdiv = Div()
        self.positioninfos = []
        self.pgnlist = None
        self.username = None
        self.usertoken = None
        self.configschema = None
        self.depthlimit = None
        self.analysisinfo = None
        self.defaultmultipv = 3
        self.bestmoveuci = None
        self.analyzing = View(self.analyzingchangedcallback, False)
        self.history = []
        self.basicboard = BasicBoard(args)        
        self.controlpanel = Div().ac("boardcontrolpanel")
        self.controlpanelheight = getglobalcssvarpxint("--boardcontrolpanelheight")
        self.controlpanelwidth = 260
        self.controlpanel.a(Button("Flip", self.flipcallback))        
        self.variantcombo = ComboBox({
            "changecallback": self.variantchanged,            
            "selectclass": "variantselect",
            "optionfirstclass": "variantoptionfirst",
            "optionclass": "variantoption"
        })
        self.setvariantcombo()
        self.variantchangedcallback = args.get("variantchangedcallback", None)
        self.moveclickedcallback = args.get("moveclickedcallback", None)
        self.enginecommandcallback = args.get("enginecommandcallback", None)
        self.socket = args.get("socket", None)        
        self.controlpanel.a(self.variantcombo).w(self.basicboard.outerwidth).mw(self.basicboard.outerwidth)
        self.controlpanel.a(Button("Del", self.delcallback))
        self.controlpanel.a(Button("Reset", self.setvariantcallback))
        self.sectioncontainer = Div().ac("bigboardsectioncontainer").w(self.basicboard.outerwidth)
        self.sectioncontainer.aa([self.controlpanel, self.basicboard])
        self.verticalcontainer = Div().ac("bigboardverticalcontainer")
        self.movelistdivwidth = 100
        self.movelistdiv = Div().ac("bigboardmovelist").w(self.movelistdivwidth).mw(self.movelistdivwidth)
        self.analysisdiv = Div()
        self.analysisdiv.a(Button("<<", self.gametobegin))
        self.analysisdiv.a(Button("<", self.gameback))
        self.analysisdiv.a(Button(">", self.gameforward))
        self.analysisdiv.a(Button(">>", self.gametoend))
        self.analysisdiv.a(Button("Store >", self.storeforward))
        self.analysisdiv.a(Button("Store Make", self.storemake))
        self.analysisdiv.a(Button("Store Stop", self.stopandstoreanalysis))
        self.analysiscontrolpanel = Div().ac("bigboardanalysiscontrolpanel")
        self.analysiscontrolpanel.a(Button("#", self.getstoredanalysisinfo))
        self.analysiscontrolpanel.a(Button("Analyze", self.analyzecallbackfactory()))
        self.analysiscontrolpanel.a(Button("Analyze all", self.analyzecallbackfactory(True)))
        self.analysiscontrolpanel.a(Button("Quick all", self.analyzecallbackfactory(True, 5, None)))
        self.analysiscontrolpanel.a(Button("Stop", self.stopanalyzecallback))
        self.analysiscontrolpanel.a(Button("Make", self.makeanalyzedmovecallback))
        self.analysiscontrolpanel.a(Button("Store", self.storeanalysiscallback))
        mopts = {}
        for i in range(1,21):
            mopts[str(i)] = "MultiPV {}".format(i)
        self.multipvcombo = ComboBox({
            "selectclass": "boardmultipvcomboselect",
            "optionfirstclass": "boardmultipvcombooptionfirst",
            "optionclass": "boardmultipvcombooption"
        }).setoptions(mopts, str(self.defaultmultipv))
        self.analysiscontrolpanel.a(self.multipvcombo)
        self.analysisdiv.a(self.analysiscontrolpanel)
        self.analysisinfodiv = Div()
        self.analysisdiv.a(self.analysisinfodiv)
        self.gamesdiv = Div()
        self.gamediv = Div()
        self.pgntext = PgnText()
        self.tabpane = TabPane({"kind":"normal", "id":"board"}).setTabs(
            [
                Tab("analysis", "Analysis", self.analysisdiv),
                Tab("game", "Game", self.gamediv),
                Tab("pgn", "Pgn", self.pgntext),
                Tab("games", "Games", self.gamesdiv)
            ], "analysis"
        )    
        self.verticalcontainer.aa([self.sectioncontainer, self.movelistdiv, self.tabpane])
        self.a(self.verticalcontainer)
        self.basicresize()
        self.buildpositioninfo()
        self.sioreq({"kind": "retrievedb",
            "owner": "board",
            "path": "board/variantkey"
        })
