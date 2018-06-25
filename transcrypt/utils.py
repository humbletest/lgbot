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

def striplonglines(content, maxlen = 200):
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

__pragma__("nojsiter")
