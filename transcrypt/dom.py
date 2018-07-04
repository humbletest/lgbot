######################################################
# dom
SCROLL_BAR_WIDTH = getScrollBarWidth()

def ce(tag):
    return document.createElement(tag)

def ge(id):
    return document.getElementById(id)

def addEventListener(object, kind, callback):
    object.addEventListener(kind, callback, False)

class e:
    def __init__(self, tag):
        self.e = ce(tag)

    # background color
    def bc(self, color):
        self.e.style.backgroundColor = color
        return self

    # cursor pointer
    def cp(self):
        self.e.style.cursor = "pointer"
        return self

    # conditional background color
    def cbc(self, cond, colortrue, colorfalse):
        self.e.style.backgroundColor = cpick(cond, colortrue, colorfalse)
        return self

    # z-index
    def zi(self, zindex):
        self.e.style.zIndex = zindex
        return self

    # opacity
    def op(self, opacity):
        self.e.style.opacity = opacity
        return self

    # monospace
    def ms(self):
        self.e.style.fontFamily = "monospace"
        return self

    # append element
    def a(self, e):
        self.e.appendChild(e.e)
        return self

    # append list of elements
    def aa(self, es):
        for e in es:
            self.a(e)
        return self

    # shorthand for setAttribute
    def sa(self, key, value):
        self.e.setAttribute(key,value)
        return self

    # shorthand for removeAttribute
    def ra(self, key):
        self.e.removeAttribute(key)
        return self

    # shorthand for getAttribute
    def ga(self, key):
        return self.e.getAttribute(key)

    # shorthand for setting value
    def sv(self, value):
        self.e.value = value
        return self

    # set inner html
    def html(self, value):
        self.e.innerHTML = value
        return self

    # clear
    def x(self):
        #self.html("")
        while self.e.firstChild:
            self.e.removeChild(self.e.firstChild)
        return self

    # width
    def w(self, w):
        self.e.style.width = w + "px"
        return self

    def mw(self, w):
        self.e.style.minWidth = w + "px"
        return self

    # height
    def h(self, h):
        self.e.style.height = h + "px"
        return self

    def mh(self, h):
        self.e.style.minHeight = h + "px"
        return self

    # top
    def t(self, t):
        self.e.style.top = t + "px"
        return self

    # left
    def l(self, l):
        self.e.style.left = l + "px"
        return self

    # conditional left
    def cl(self, cond, ltrue, lfalse):
        self.e.style.left = cpick(cond, ltrue, lfalse) + "px"
        return self

    # conditional top
    def ct(self, cond, ttrue, tfalse):
        self.e.style.top = cpick(cond, ttrue, tfalse) + "px"
        return self

    # position vector
    def pv(self, v):
        return self.l(v.x).t(v.y)

    # position absolute
    def pa(self):
        self.e.style.position = "absolute"
        return self

    # position relative
    def pr(self):
        self.e.style.position = "relative"
        return self

    # margin left
    def ml(self, ml):
        self.e.style.marginLeft = ml + "px"
        return self

    # margin right
    def mr(self, mr):
        self.e.style.marginRight = mr + "px"
        return self

    # margin top
    def mt(self, mt):
        self.e.style.marginTop = mt + "px"
        return self

    # margin bottom
    def mb(self, mb):
        self.e.style.marginBottom = mb + "px"
        return self

    # add class
    def ac(self, klass):
        self.e.classList.add(klass)
        return self

    # add classes
    def aac(self, klasses):
        for klass in klasses:
            self.e.classList.add(klass)
        return self

    # remove class
    def rc(self, klass):
        self.e.classList.remove(klass)
        return self

    # add or remove class based on condition
    def arc(self, cond, klass):
        if cond:
            self.e.classList.add(klass)
        else:
            self.e.classList.remove(klass)
        return self

    # return value
    def v(self):
        return self.e.value

    def focusme(self):                
        self.e.focus()
        return self

    # focus later
    def fl(self):                
        setTimeout(self.focusme, 50)
        return self

    # add event listener
    def ae(self, kind, callback):
        self.e.addEventListener(kind, callback)
        return self

    # disable
    def disable(self):
        return self.sa("disabled", True)

    # enable
    def enable(self):
        return self.ra("disabled")

    # able
    def able(self, able):
        if able:
            return self.enable()
        return self.disable()

    # font size
    def fs(self, size):
        self.e.style.fontSize = size + "px"
        return self

class Div(e):
    def __init__(self):
        super().__init__("div")

class Span(e):
    def __init__(self):
        super().__init__("span")

class Input(e):
    def __init__(self, kind):
        super().__init__("input")
        self.sa("type", kind)

class Select(e):
    def __init__(self):
        super().__init__("select")

class Option(e):
    def __init__(self, key, displayname, selected = False):
        super().__init__("option")
        self.sa("name", key)
        self.sa("id", key)
        self.sv(key)
        self.html(displayname)
        if selected:
            self.sa("selected", True)

class Slider(Input):
    def setmin(self, min):
        self.sa("min", min)
        return self

    def setmax(self, max):
        self.sa("max", max)
        return self

    def __init__(self):
        super().__init__("range")

class CheckBox(Input):
    def setchecked(self, checked):
        self.e.checked = checked
        return self

    def getchecked(self):
        return self.e.checked

    def __init__(self, checked = False):
        super().__init__("checkbox")
        self.setchecked(checked)

class TextArea(e):
    def __init__(self):
        super().__init__("textarea")

    def setText(self, content):
        self.sv(content)
        return self

    def getText(self):
        return self.v()
######################################################

