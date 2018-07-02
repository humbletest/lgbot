STANDARD_START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
RACING_KINGS_START_FEN = "8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1"
HORDE_START_FEN = "rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w kq - 0 1"
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

def getstartfenforvariantkey(variantkey):
    if variantkey == "racingKings":
        return RACING_KINGS_START_FEN
    if variantkey == "horde":
        return HORDE_START_FEN
    return STANDARD_START_FEN

class Piece():
    def __init__(self, kind = None, color = None):
        self.kind = kind
        self.color = color

    def isempty(self):
        return self.kind is None

    def ispiece(self):
        return not self.isempty()

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

def getclassforpiece(p, style):
    kind = p.kind
    if p.color == WHITE:
        kind = "w" + kind
    return style + "piece" + kind

class Square(Vect):
    def __init__(self, file, rank):
        self.x = file
        self.y = rank

    def file(self):
        return self.x

    def rank(self):
        return self.y

    def __repr__(self):
        return "Sq[f:{},r:{}]".format(self.file(), self.rank())

class BasicBoard(e):
    def squareuci(self, sq):
        fileletter = String.fromCharCode(sq.file() + "a".charCodeAt(0))
        rankletter = String.fromCharCode(self.lastrank - sq.rank() + "1".charCodeAt(0))
        return fileletter + rankletter

    def islightfilerank(self, file, rank):
        return ( ( ( file + rank ) % 2 ) == 0 )

    def islightsquare(self, sq):
        return self.islightfilerank(sq.file(), sq.rank())

    def squarelist(self):
        squarelist = []
        for file in range(self.numfiles):
            for rank in range(self.numranks):
                squarelist.append(Square(file, rank))
        return squarelist

    def squarecoordsvect(self, sq):
        return Vect(sq.file() * self.squaresize, sq.rank() * self.squaresize)

    def piececoordsvect(self, sq):
        return self.squarecoordsvect(sq).p(Vect(self.squarepadding, self.squarepadding))

    def flipawaresquare(self, sq):
        if self.flip:
            return Square(self.lastfile - sq.file(), self.lastrank - sq.rank())
        return sq

    def piecedragstartfactory(self, sq, pdiv):
        def piecedragstart(ev):
            self.draggedsq = sq            
            self.draggedpdiv = pdiv
            pdiv.e.style.opacity = 0.1
        return piecedragstart

    def piecedragfactory(self):
        def piecedrag(ev):            
            pass
        return piecedrag

    def piecedragendfactory(self, sq, pdiv):
        def piecedragend(ev):                        
            pdiv.e.style.opacity = 0.5
        return piecedragend

    def piecedragoverfactory(self, sq):
        def piecedragover(ev):
            ev.preventDefault()            
        return piecedragover

    def piecedropfactory(self, sq):
        def piecedrop(ev):
            ev.preventDefault()            
            self.draggedpdiv.pv(self.piececoordsvect(self.flipawaresquare(sq)))
            self.draggedpdiv.e.style.zIndex = 100
            moveuci = self.squareuci(self.draggedsq) + self.squareuci(sq)
            if not ( self.movecallback is None ):
                self.movecallback(self.variantkey, self.fen, moveuci)
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
                self.container.a(pdiv)

    def build(self):
        self.outercontainer = Div().ac("boardoutercontainer").w(self.outerwidth).h(self.outerheight)
        self.container = Div().ac("boardcontainer").w(self.width).h(self.height).t(self.margin).l(self.margin)
        self.outercontainer.a(self.container)
        self.x().a(self.outercontainer)
        self.buildsquares()
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

    def parseargs(self, args):
        self.squaresize = args.get("squaresize", 50)
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

    def getpieceati(self, i):
        if ( i >= 0 ) and ( i < self.area ):            
            return self.rep[i]
        return Piece()

    def getpieceatfilerank(self, file, rank):
        i = rank * self.numfiles + file        
        return self.getpieceati(i)

    def getpieceatsquare(self, sq):
        return self.getpieceatfilerank(sq.file(), sq.rank())

    def setrepfromfen(self, fen):  
        self.fen = fen
        self.rep = [Piece() for i in range(self.area)]
        fenparts = self.fen.split(" ")
        rawfen = fenparts[0]
        rawfenparts = rawfen.split("/")
        i = 0
        for rawfenpart in rawfenparts:
            pieceletters = rawfenpart.split("")
            for pieceletter in pieceletters:
                if isvalidpieceletter(pieceletter):
                    self.setpieceati(i, piecelettertopiece(pieceletter))
                    i+=1
                else:
                    try:
                        mul = int(pieceletter)
                        for j in range(mul):
                            self.setpieceati(i, Piece())
                            i += 1
                    except:
                        pass

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
        self.a(self.controlpanel)
        self.a(self.basicboard)
