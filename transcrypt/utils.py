MAX_CONTENT_LENGTH = 1000
MAX_LINE_LENGTH = 500

MATE_SCORE = 10000
MATE_LIMIT = MATE_SCORE * 0.9
WINNING_MOVE_LIMIT = 1000
DOUBLE_EXCLAM_LIMIT = 500
EXCLAM_LIMIT = 350
PROMISING_LIMIT = 250
INTERESTING_LIMIT = 150
DRAWISH_LIMIT = 80

LICH_API_GAMES_EXPORT = "games/export"
#LICH_API_GAMES_EXPORT = "api/games/user"

def uci_variant_to_variantkey(uci_variant, chess960 = False):
    if uci_variant == "chess":
        if chess960:
            return "chess960"
        else:
            return "standard"
    if uci_variant == "giveaway":
        return "antichess"
    if uci_variant == "kingofthehill":
        return "kingOfTheHill"
    if uci_variant == "racingkings":
        return "racingKings"
    if uci_variant == "3check":
        return "threeCheck"
    return uci_variant

def scoreverbal(score):
    if abs(score) < MATE_LIMIT:
        return str(score)
    if score >= 0:
        return "#{}".format(MATE_SCORE - score)
    return "#{}".format(- MATE_SCORE - score)

def scorecolor(score):
    if score > MATE_LIMIT:
        return "#0f0"
    if score > WINNING_MOVE_LIMIT:
        return "#0e0"
    if score > DOUBLE_EXCLAM_LIMIT:
        return "#0c0"
    if score > EXCLAM_LIMIT:
        return "#0a0"
    if score > PROMISING_LIMIT:
        return "#090"
    if score > INTERESTING_LIMIT:
        return "#070"
    if score > DRAWISH_LIMIT:
        return "#050"
    if score > 0:
        return "#033"
    if score > (-DRAWISH_LIMIT):
        return "#330"
    if score > (-INTERESTING_LIMIT):
        return "#500"
    if score > (-PROMISING_LIMIT):
        return "#900"
    if score > (-EXCLAM_LIMIT):
        return "#a00"
    if score > (-DOUBLE_EXCLAM_LIMIT):
        return "#c00"
    if score > WINNING_MOVE_LIMIT:
        return "#e00"
    return "#f00"

class View:
    def __init__(self, callback, value = None):
        self.callback = callback
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.callback()

def xor(b1, b2):
    if b1 and b2:
        return False
    if b1 or b2:
        return True
    return False

def cpick(cond, vtrue, vfalse):
    if cond:
        return vtrue
    return vfalse

def simulateserverlag(range = 1000, min_lag = 10):    
    if "localhost" in window.location.host:
        return int(min_lag + Math.random() * range)
    return min_lag

def choose(cond, choicetrue, choicefalse):
    if cond:
        return choicetrue
    return choicefalse

class Vect:
    def __init__(self, x, y):
        try:
            self.x = float(x)
            self.y = float(y)
        except:
            self.x = 0.0
            self.y = 0.0
            print("vect init failed on", x, y)

    def p(self, v):
        return Vect(self.x + v.x, self.y + v.y)

    def s(self, s):
        return Vect(self.x * s, self.y * s)

    def m(self, v):
        return self.p(v.s(-1))
    
    def copy(self):
        return Vect(self.x, self.y)

    def __repr__(self):
        return "Vect[x: {}, y: {}]".format(self.x, self.y)

def getClientVect(ev):
    return Vect(ev.clientX, ev.clientY)

def getglobalcssvar(key):
    return getComputedStyle(window.document.documentElement).getPropertyValue(key)

def getglobalcssvarpxint(key, default):
    try:
        px = getglobalcssvar(key)
        pxint = int(px.replace("px",""))
        return pxint
    except:
        return default

def striplonglines(content, maxlen = MAX_LINE_LENGTH):
    lines = content.split("\n")    
    strippedlines = []
    for line in lines:        
        if len(line) > maxlen:   
            sline = "{} ... [ truncated {} characters ]".format(line.substring(0,maxlen), len(line) - maxlen)
            strippedlines.append(sline)
        else:
            strippedlines.append(line)
    content = "\n".join(strippedlines)    
    return content

# https://stackoverflow.com/questions/13382516/getting-scroll-bar-width-using-javascript
def getScrollBarWidth():
    outer = document.createElement("div")
    outer.style.visibility = "hidden"
    outer.style.width = "100px"
    outer.style.msOverflowStyle = "scrollbar" # needed for WinJS apps

    document.body.appendChild(outer)

    widthNoScroll = outer.offsetWidth
    # force scrollbars
    outer.style.overflow = "scroll"

    # add innerdiv
    inner = document.createElement("div")
    inner.style.width = "100%"
    outer.appendChild(inner)       

    widthWithScroll = inner.offsetWidth

    # remove divs
    outer.parentNode.removeChild(outer)

    return widthNoScroll - widthWithScroll

def randint(range):
    return int(Math.random()*range)

def randscalarvalue(baselen, pluslen):
    len = baselen + randint(pluslen)
    buff = ""
    for i in range(len):
        if (i % 2) == 1:        
            buff += ["a", "e", "i", "o", "u"][randint(5)]
        else:
            buff += ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"][randint(21)]
    return buff

def uid():
    uid = randscalarvalue(8, 0)
    return uid

def getfromobj(obj, key, default):
    if key in obj:
        return obj[key]    
    return default    

def patchclasses(selfref, args):
    items = args.get("patchclasses", [])
    for item in items:
        parts = item.split("/")
        membername = parts[0]
        action = parts[1]
        classname = parts[2]
        if action == "a":
            selfref[membername].ac(classname)
        elif action == "r":
            selfref[membername].rc(classname)

def parsejson(jsonstr, callback, errcallback):
    try:
        obj = JSON.parse(jsonstr)
        callback(obj)
    except:
        errcallback("error parsing json")

__pragma__("jsiter")

def putjsonbin(json, id, callback, errcallback):

    method = "POST"
    url = "https://api.jsonbin.io/b"        

    if id == "local":
        pass
    elif not ( id is None ):
        url = url + "/" + id        
        method = "PUT"    
    
    args = {
        "method": method,
        "headers": {
            "Content-Type": "application/json",
            "private": False
        },
        "body": json
    }        
    
    fetch(url, args).then(
        lambda response: response.text().then(
            lambda content: callback(content),
            lambda err: errcallback(err)
        ),
        lambda err: errcallback(err)
    )

def getjsonbin(id, callback, errcallback, version = "latest"):

    args = {
        "method": "GET",
        "headers": {
            "Content-Type": "application/json",
            "private": False
        }
    }

    fetch("https://api.jsonbin.io/b/" + id + "/" + version, args).then(
        lambda response: response.text().then(
            lambda content: callback(content),
            lambda err: errcalback(err)
        ),
        lambda err: errcallback(err)
    )

def getjson(path, callback, errcallback):

    args = {
        "method": "GET",
        "headers": {
            "Content-Type": "application/json"
        }
    }

    fetch(path, args).then(
        lambda response: response.text().then(
            lambda content: parsejson(content, callback, errcallback),
            lambda err: errcalback(err)
        ),
        lambda err: errcallback(err)
    )

def lichapiget(path, token, callback, errcallback):

    args = {
        "method": "GET"
    }

    if ( not ( token is None ) ) and ( False ):
        args["headers"] = {
            "Authorization": "Bearer {}".format(token)
        }

    fetch("https://lichess.org/" + path, args).then(
        lambda response: response.text().then(
            lambda content: callback(content),
            lambda err: errcalback(err)
        ),
        lambda err: errcallback(err)
    )

__pragma__("nojsiter")
