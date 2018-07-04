STANDARD_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
ANTICHESS_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
RACING_KINGS_START_FEN = "8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1"
HORDE_START_FEN = "rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w kq - 0 1"
THREE_CHECK_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 3+3 0 1"
CRAZYHOUSE_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[] w KQkq - 0 1"
PIECE_KINDS = ["p", "n", "b", "r", "q", "k"]
WHITE = 1
BLACK = 0
VARIANT_OPTIONS = {
    "standard": "Standard",
    "fromPosition": "From Position",
    "antichess" : "Antichess",
    "atomic": "Atomic",
    "chess960": "Chess960",
    "crazyhouse": "Crazyhouse",
    "horde": "Horde",
    "kingOfTheHill": "King of the Hill",
    "racingKings": "Racing Kings",
    "threeCheck": "Three Check"
}
PIECE_NAMES = {
    "p": "Pawn",
    "n": "Knight",
    "b": "Bishop",
    "r": "Rook",
    "q": "Queen",
    "k": "King"
}
PROMPIECEKINDS_STANDARD = ["n", "b", "r", "q"]
PROMPIECEKINDS_ANTICHESS = ["n", "b", "r", "q", "k"]

def prompiecekindsforvariantkey(variantkey):
    if variantkey == "antichess":
        return PROMPIECEKINDS_ANTICHESS
    return PROMPIECEKINDS_STANDARD

def piececolortocolorname(color):
    if color == WHITE:
        return "White"
    elif color == BLACK:
        return "Black"
    return "Invalidcolor"

def piecekindtopiecename(kind):
    if kind in PIECE_NAMES:
        return PIECE_NAMES[kind]
    return "Invalidpiece"

def getstartfenforvariantkey(variantkey):
    if variantkey == "antichess":
        return ANTICHESS_START_FEN
    if variantkey == "racingKings":
        return RACING_KINGS_START_FEN
    if variantkey == "horde":
        return HORDE_START_FEN    
    if variantkey == "threeCheck":
        return THREE_CHECK_START_FEN
    if variantkey == "crazyhouse":
        return CRAZYHOUSE_START_FEN
    return STANDARD_START_FEN

class Piece():
    def __init__(self, kind = None, color = None):
        self.kind = kind
        self.color = color

    def isempty(self):
        return self.kind is None

    def ispiece(self):
        return not self.isempty()

    def __repr__(self):
        if self.isempty():
            return "Piece[None]"
        return "Piece[{} {}]".format(piececolortocolorname(self.color), piecekindtopiecename(self.kind))

def isvalidpieceletter(pieceletter):
    if pieceletter in PIECE_KINDS:
        return True
    if pieceletter.toLowerCase() in PIECE_KINDS:
        return True
    return False

def piecelettertopiece(pieceletter):
    if isvalidpieceletter(pieceletter):
        pieceletterlower = pieceletter.toLowerCase()
        if pieceletterlower == pieceletter:
            return Piece(pieceletterlower, BLACK)
        return Piece(pieceletterlower, WHITE)
    print("warning, piece letter not valid", pieceletter)
    return Piece()

def getclassforpiece(p, style):
    kind = p.kind
    if p.color == WHITE:
        kind = "w" + kind
    return style + "piece" + kind

class Square:
    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

    def p(self, sq):
        return Square(self.file + sq.file, self.rank + sq.rank)

    def __repr__(self):
        return "Square[file: {} , rank: {}]".format(self.file, self.rank)

    def copy(self):
        return Square(self.file, self.rank)

class Move:
    def __init__(self, fromsq, tosq, prompiece = Piece()):
        self.fromsq = fromsq
        self.tosq = tosq
        self.prompiece = prompiece

    def __repr__(self):
        return "Move [from: {} , to: {} , prom: {}]".format(self.fromsq, self.tosq, self.prompiece)

class PieceStore(e):
    def dragstartfactory(self, p, pdiv, pdivcopy):
        def dragstart():
            self.parent.dragkind = "set"
            self.parent.draggedsetpiece = p
            self.parent.draggedpdiv = pdivcopy
            pdiv.op(0.7)
        return dragstart

    def setstore(self, store):
        self.store = store
        self.container.x()
        self.pieces = {}        
        for pieceletter in self.store.split(""):
            p = piecelettertopiece(pieceletter)
            if p.color == self.color:
                if p.kind in self.pieces:
                    self.pieces[p.kind]["mul"] += 1
                else:
                    pcdiv = Div().pr().w(self.piecesize).h(self.piecesize)
                    pdiv = Div().pa().cp().ac(getclassforpiece(p, self.parent.piecestyle)).w(self.piecesize).h(self.piecesize)
                    pdivcopy = Div().pa().cp().ac(getclassforpiece(p, self.parent.piecestyle)).w(self.piecesize).h(self.piecesize)
                    pdiv.t(0).l(0).sa("draggable", True).ae("dragstart", self.dragstartfactory(p, pdiv, pdivcopy))                
                    pcdiv.a(pdiv)
                    self.pieces[p.kind] = {
                        "mul": 1,
                        "p": p,
                        "pcdiv": pcdiv
                    }        
        for pkind, pdesc in self.pieces.items():
            muldiv = Div().pa().w(self.muldivsize).h(self.muldivsize).fs(self.muldivsize).html("{}".format(pdesc["mul"]))
            muldiv.l(self.piecesize - self.muldivsize).t(0).ac("storemuldiv")
            pdesc["pcdiv"].a(muldiv)
            self.container.a(pdesc["pcdiv"])            
        return self

    def __init__(self, args):
        super().__init__("div")
        self.parent = args.get("parent", BasicBoard({}))
        self.store = args.get("store", "")
        self.color = args.get("color", WHITE)
        self.piecesize = args.get("piecesize", self.parent.piecesize)
        self.muldivsize = int(self.piecesize / 2)
        self.container = Div().aac(["piecestorecontainer", "noselect"])
        self.a(self.container)
        self.setstore(self.store)

class BasicBoard(e):
    def squareuci(self, sq):
        fileletter = String.fromCharCode(sq.file + "a".charCodeAt(0))
        rankletter = String.fromCharCode(self.lastrank - sq.rank + "1".charCodeAt(0))
        return fileletter + rankletter

    def moveuci(self, move):
        fromuci = self.squareuci(move.fromsq)
        touci = self.squareuci(move.tosq)
        promuci = cpick(move.prompiece.isempty(), "", move.prompiece.kind)
        return fromuci + touci + promuci

    def islightfilerank(self, file, rank):
        return ( ( ( file + rank ) % 2 ) == 0 )

    def islightsquare(self, sq):
        return self.islightfilerank(sq.file, sq.rank)

    def squarelist(self):
        squarelist = []
        for file in range(self.numfiles):
            for rank in range(self.numranks):
                squarelist.append(Square(file, rank))
        return squarelist

    def squarecoordsvect(self, sq):
        return Vect(sq.file * self.squaresize, sq.rank * self.squaresize)

    def piececoordsvect(self, sq):
        return self.squarecoordsvect(sq).p(Vect(self.squarepadding, self.squarepadding))

    def flipawaresquare(self, sq):
        if self.flip:
            return Square(self.lastfile - sq.file, self.lastrank - sq.rank)
        return sq

    def piecedragstartfactory(self, sq, pdiv):
        def piecedragstart(ev):
            if self.promoting:
                ev.preventDefault()
                return
            self.dragkind = "move"
            self.draggedsq = sq            
            self.draggedpdiv = pdiv
            pdiv.op(0.1)
        return piecedragstart

    def piecedragfactory(self):
        def piecedrag(ev):            
            pass
        return piecedrag

    def piecedragendfactory(self, sq, pdiv):
        def piecedragend(ev):                        
            pdiv.op(0.5)
        return piecedragend

    def piecedragoverfactory(self, sq):
        def piecedragover(ev):
            ev.preventDefault()            
        return piecedragover

    def ismovepromotion(self, move):
        fromp = self.getpieceatsquare(move.fromsq)
        if ( fromp.kind == "p" ) and ( fromp.color == self.turn() ):
            if self.iswhitesturn():
                if move.tosq.rank == 0:
                    return True
            else:
                if move.tosq.rank == self.lastrank:
                    return True
        return False

    def piecedropfactory(self, sq):
        def piecedrop(ev):
            ev.preventDefault()            
            self.draggedpdiv.pv(self.piececoordsvect(self.flipawaresquare(sq)))
            self.draggedpdiv.zi(100)
            if self.dragkind == "move":                
                self.dragmove = Move(self.draggedsq, sq)
                if self.ismovepromotion(self.dragmove):
                    self.promoting = True
                    self.build()
                elif not ( self.movecallback is None ):
                    self.movecallback(self.variantkey, self.fen, self.moveuci(self.dragmove))
            elif self.dragkind == "set":
                self.container.a(self.draggedpdiv)
                if not ( self.movecallback is None ):
                    setuci = "{}@{}".format(self.draggedsetpiece.kind, self.squareuci(sq))
                    self.movecallback(self.variantkey, self.fen, setuci)
        return piecedrop

    def buildsquares(self):
        self.container.x()
        for sq in self.squarelist():
            sqclass = choose(self.islightsquare(sq), "boardsquarelight", "boardsquaredark")
            sqdiv = Div().aac(["boardsquare", sqclass]).w(self.squaresize).h(self.squaresize)            
            fasq = self.flipawaresquare(sq)
            sqdiv.pv(self.squarecoordsvect(fasq))
            sqdiv.ae("dragover", self.piecedragoverfactory(sq))
            sqdiv.ae("drop", self.piecedropfactory(sq))            
            self.container.a(sqdiv)
            p = self.getpieceatsquare(sq)
            if p.ispiece():
                pdiv = Div().ac("boardpiece").w(self.piecesize).h(self.piecesize).pv(self.piececoordsvect(fasq))
                pdiv.ac(getclassforpiece(p, self.piecestyle)).sa("draggable", True)
                pdiv.ae("dragstart", self.piecedragstartfactory(sq, pdiv))
                pdiv.ae("drag", self.piecedragfactory())
                pdiv.ae("dragend", self.piecedragendfactory(sq, pdiv))
                pdiv.ae("dragover", self.piecedragoverfactory(sq))
                pdiv.ae("drop", self.piecedropfactory(sq))            
                if self.variantkey == "threeCheck":
                    if ( p.kind == "k" ):
                        mul = self.getthreelifesforcolor(p.color)
                        lifesdiv = Div().pa().t(- self.squaresize / 10).l(self.squaresize / 2 + self.squaresize / 10).w(self.squaresize / 2).h(self.squaresize / 2)
                        lifesdiv.ac("boardthreechecklifesdiv").fs(self.squaresize / 1.5).html("{}".format(mul))
                        lifesdiv.cc(p.color == WHITE, "#ff0", "#ff0")
                        pdiv.a(lifesdiv)
                self.container.a(pdiv)

    def getthreelifesforcolor(self, color):
        parts = self.threefen.split("+")
        mul = 3
        if color == WHITE:
            try:
                mul = int(parts[2])
            except:
                print("warning, could not parse white lifes from", self.threefen)
        if color == BLACK:
            try:
                mul = int(parts[0])
            except:
                print("warning, could not parse black lifes from", self.threefen)
        return mul

    def prompiececlickedfactory(self, prompiecekind):
        def prompiececlicked():
            self.dragmove.prompiece = Piece(prompiecekind, self.turn())
            self.movecallback(self.variantkey, self.fen, self.moveuci(self.dragmove))
        return prompiececlicked

    def buildprominput(self):
        promkinds = prompiecekindsforvariantkey(self.variantkey)
        promsq = self.dragmove.tosq.copy()        
        dir = cpick(promsq.rank >= ( self.numranks / 2 ), -1, 1)
        ppks = prompiecekindsforvariantkey(self.variantkey)
        for ppk in ppks:            
            fapromsq = self.flipawaresquare(promsq)
            pp = Piece(ppk, self.turn())
            psqdiv = Div().pa().cp().zi(150).w(self.squaresize).h(self.squaresize).ac("boardpromotionsquare")
            psqdiv.pv(self.squarecoordsvect(fapromsq))
            ppdiv = Div().pa().cp().zi(200).w(self.piecesize).h(self.piecesize).ac(getclassforpiece(pp, self.piecestyle))
            ppdiv.pv(self.piececoordsvect(fapromsq)).ae("mousedown", self.prompiececlickedfactory(ppk))
            self.container.aa([psqdiv, ppdiv])
            promsq = promsq.p(Square(0, dir))

    def promotecancelclick(self):
        self.promoting = False
        self.build()

    def build(self):
        self.sectioncontainer = Div().ac("boardsectioncontainer").w(self.outerwidth)
        self.outercontainer = Div().ac("boardoutercontainer").w(self.outerwidth).h(self.outerheight)
        self.container = Div().ac("boardcontainer").w(self.width).h(self.height).t(self.margin).l(self.margin)
        self.outercontainer.a(self.container)        
        self.buildsquares()
        self.turndiv = Div().pa().w(self.turndivsize).h(self.turndivsize).cbc(self.iswhitesturn(), "#fff", "#000")
        if self.variantkey == "racingKings":
            self.turndiv.ct(self.flip, 0, self.outerheight - self.turndivsize).cl(xor(self.isblacksturn(), self.flip), 0, self.outerwidth - self.turndivsize)
        else:
            self.turndiv.l(self.outerwidth - self.turndivsize).ct(xor(self.isblacksturn(), self.flip), 0, self.outerheight - self.turndivsize)
        self.outercontainer.a(self.turndiv)
        if self.promoting:
            self.buildprominput()
            self.container.ae("mousedown", self.promotecancelclick)
        self.fentext = RawTextInput({}).w(self.width).fs(10).setText(self.fen)
        self.fendiv = Div().ac("boardfendiv").a(self.fentext)
        if self.variantkey == "crazyhouse":
            self.whitestore = PieceStore({
                "parent": self,
                "color": WHITE,
                "store": self.crazyfen
            })
            self.blackstore = PieceStore({
                "parent": self,
                "color": BLACK,
                "store": self.crazyfen
            })
            self.whitestorediv = Div().ac("boardstorediv").h(self.squaresize).a(self.whitestore)
            self.blackstorediv = Div().ac("boardstorediv").h(self.squaresize).a(self.blackstore)
            if self.flip:
                self.sectioncontainer.aa([self.whitestorediv, self.outercontainer, self.blackstorediv, self.fendiv])
            else:
                self.sectioncontainer.aa([self.blackstorediv, self.outercontainer, self.whitestorediv, self.fendiv])
        else:
            self.sectioncontainer.aa([self.outercontainer, self.fendiv])
        self.x().a(self.sectioncontainer)
        return self

    def setflip(self, flip):
        self.flip = flip
        self.build()

    def calcsizes(self):
        self.lastfile = self.numfiles - 1
        self.lastrank = self.numranks - 1
        self.area = self.numfiles * self.numranks
        self.width = self.numfiles * self.squaresize
        self.height = self.numranks * self.squaresize
        self.avgsize = ( self.width + self.height ) / 2
        self.margin = self.marginratio * self.avgsize
        self.squarepadding = self.squarepaddingratio * self.squaresize
        self.piecesize = self.squaresize - 2 * self.squarepadding
        self.outerwidth = self.width + 2 * self.margin
        self.outerheight = self.height + 2 * self.margin
        self.turndivsize = self.margin

    def parseargs(self, args):
        self.squaresize = args.get("squaresize", 45)
        self.squarepaddingratio = args.get("squarepaddingratio", 0.04)
        self.marginratio = args.get("marginratio", 0.02)
        self.numfiles = args.get("numfiles", 8)
        self.numranks = args.get("numranks", 8)        
        self.piecestyle = args.get("piecestyle", "alpha")
        self.flip = args.get("flip", False)
        self.movecallback = args.get("movecallback", None)
        self.calcsizes()

    def setpieceati(self, i, p):
        if ( i >= 0 ) and ( i < self.area ):
            self.rep[i] = p
        else:
            print("warning, rep index out of range", i)

    def getpieceati(self, i):
        if ( i >= 0 ) and ( i < self.area ):            
            return self.rep[i]
        return Piece()

    def getpieceatfilerank(self, file, rank):
        i = rank * self.numfiles + file        
        return self.getpieceati(i)

    def getpieceatsquare(self, sq):
        return self.getpieceatfilerank(sq.file, sq.rank)

    def setrepfromfen(self, fen):  
        self.fen = fen
        self.crazyfen = None
        self.threefen = None
        self.rep = [Piece() for i in range(self.area)]
        fenparts = self.fen.split(" ")
        self.rawfen = fenparts[0]
        rawfenparts = self.rawfen.split("/")        
        if self.variantkey == "crazyhouse":
            self.crazyfen = ""
            if "[" in self.rawfen:
                cfenparts = self.rawfen.split("[")
                self.rawfen = cfenparts[0]
                rawfenparts = self.rawfen.split("/")
                cfenparts = cfenparts[1].split("]")
                self.crazyfen = cfenparts[0]
        i = 0
        for rawfenpart in rawfenparts:
            pieceletters = rawfenpart.split("")
            for pieceletter in pieceletters:
                if isvalidpieceletter(pieceletter):
                    self.setpieceati(i, piecelettertopiece(pieceletter))
                    i+=1
                else:
                    mul = 0
                    try:
                        mul = int(pieceletter)                        
                    except:
                        print("warning, multiplicity could not be parsed from", pieceletter)
                    for j in range(mul):
                        self.setpieceati(i, Piece())
                        i += 1
        if i < self.area:
            print("warning, raw fen did not fill board")
        elif i > self.area:
            print("warning, raw fen exceeded board")
        self.turnfen = "w"
        if len(fenparts) > 1:
            self.turnfen = fenparts[1]
        else:
            print("warning, no turn fen")
        self.castlefen = "-"
        if len(fenparts) > 2:
            self.castlefen = fenparts[2]
        else:
            print("warning, no castle fen")
        self.epfen = "-"
        if len(fenparts) > 3:
            self.epfen = fenparts[3]
        else:
            print("warning, no ep fen")
        moveclocksi = cpick(self.variantkey == "threeCheck", 5, 4)
        self.halfmoveclock = 0
        if len(fenparts) > moveclocksi:
            try:
                self.halfmoveclock = int(fenparts[moveclocksi])
            except:
                print("warning, half move clock could not be parsed from", fenparts[4])
        else:
            print("warning, no half move fen")
        self.fullmovenumber = 1
        if len(fenparts) > ( moveclocksi + 1 ):
            try:
                self.fullmovenumber = int(fenparts[moveclocksi + 1])
            except:
                print("warning, full move number could not be parsed from", fenparts[5])
        else:
            print("warning, no full move fen")
        if self.variantkey == "threeCheck":
            if len(fenparts) > 4:
                self.threefen = fenparts[4]        
        self.promoting = False

    def turn(self):
        if self.turnfen == "w":
            return WHITE
        return BLACK

    def iswhitesturn(self):
        return self.turn() == WHITE

    def isblacksturn(self):
        return self.turn() == BLACK

    def initrep(self, args):
        self.variantkey = args.get("variantkey", "standard")
        self.setrepfromfen(args.get("fen", getstartfenforvariantkey(self.variantkey)))

    def setfromfen(self, fen):
        self.setrepfromfen(fen)
        self.build()

    def reset(self):
        self.setfromfen(getstartfenforvariantkey(self.variantkey))

    def __init__(self, args):
        super().__init__("div")        
        self.parseargs(args)
        self.initrep(args)
        self.build()

class Board(e):
    def flipcallback(self):
        self.basicboard.setflip(not self.basicboard.flip)

    def resetcallback(self):
        self.basicboard.reset()

    def setfromfen(self, fen):
        self.basicboard.setfromfen(fen)

    def setvariantcombo(self):        
        self.variantcombo.setoptions(VARIANT_OPTIONS, self.basicboard.variantkey)

    def variantchanged(self, variantkey):
        self.basicboard.variantkey = variantkey
        self.basicboard.reset()
        if not ( self.variantchangedcallback is None ):
            self.variantchangedcallback(self.basicboard.variantkey)

    def setvariantcallback(self):
        self.variantchanged(self.basicboard.variantkey)

    def __init__(self, args):
        super().__init__("div")
        self.basicboard = BasicBoard(args)        
        self.controlpanel = Div().ac("boardcontrolpanel")
        self.controlpanel.a(Button("Flip", self.flipcallback))        
        self.variantcombo = ComboBox({
            "changecallback": self.variantchanged,
            "selectclass": "variantselect",
            "optionfirstclass": "variantoptionfirst",
            "optionclass": "variantoption"
        })
        self.setvariantcombo()
        self.variantchangedcallback = args.get("variantchangedcallback", None)
        self.controlpanel.a(self.variantcombo).w(self.basicboard.outerwidth)
        self.controlpanel.a(Button("Reset", self.setvariantcallback))
        self.sectioncontainer = Div().ac("bigboardsectioncontainer").w(self.basicboard.outerwidth)
        self.sectioncontainer.aa([self.controlpanel, self.basicboard])
        self.a(self.sectioncontainer)
