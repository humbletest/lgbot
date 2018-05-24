######################################################
# dom
def ce(tag):
    return document.createElement(tag)

def ge(id):
    return document.getElementById(id)

class e:
    def __init__(self, tag):
        self.e = ce(tag)

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

    # shorthand for setting value
    def sv(self, value):
        self.e.value = value
        return self

    # set inner html
    def h(self, value):
        self.e.innerHTML = value
        return self

    def x(self):
        self.h("")
        return self

    # add class
    def ac(self, klass):
        self.sa("class",klass)
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

class Div(e):
    def __init__(self):
        super().__init__("div")

class Span(e):
    def __init__(self):
        super().__init__("span")

class Input(e):
    def __init__(self, kind):
        super().__init__("input")
        self.sa("type",kind)
######################################################

