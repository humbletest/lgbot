import yaml
import os
import sys
import time
import threading

from selenium import webdriver

###################################################

from serverutils.process import PopenProcess

###################################################

ANSI = {
    "NONE" : "",
    "BLACK" : '\033[30m',
    "RED" : '\033[31m', 
    "GREEN" : '\033[32m',
    "YELLOW" : '\033[33m',
    "BLUE" : '\033[34m',
    "MAGENTA" : '\033[35m',
    "CYAN" : '\033[36m',
    "WHITE" : '\033[37m',
    "BRIGHTBLACK" : '\033[90m',
    "BRIGHTRED" : '\033[91m',
    "BRIGHTGREEN" : '\033[92m',
    "BRIGHTYELLOW" : '\033[93m',
    "BRIGHTBLUE" : '\033[94m',
    "BRIGHTMAGENTA" : '\033[95m',
    "BRIGHTCYAN" : '\033[96m',
    "BRIGHTWHITE" : '\033[97m',
        
    "ENDC" : '\033[0m',

    "BOLD" : '\033[1m',
    "UNDERLINE" : '\033[4m'
}

###################################################

browser = webdriver.Chrome()
browser.set_window_position(int(os.environ["BROWSER_WINDOW_LEFT"]), int(os.environ["BROWSER_WINDOW_TOP"]))
browser.set_window_size(int(os.environ["BROWSER_WINDOW_WIDTH"]), int(os.environ["BROWSER_WINDOW_HEIGHT"]))
browserinit = True

###################################################

def rf(path, default):    
    try:
        return open(path).read()
    except:
        return default

def ry(path, default):    
    try:
        return yaml.load(open(path))
    except:
        return default

def procreadline(sline):
    print(sline)

def runcmd(cmd):
    proc = PopenProcess(cmd, procreadline)
    returncode = proc.wait_for_return_code()
    return returncode

def getlastmod(path):
    stat = os.stat(path)
    return stat.st_mtime

###################################################

class BuildCommandFailedException(BaseException):
    def __init__(self, rulename, cmd):
        self.rulename = rulename
        self.cmd = cmd

class BDep:
    def __init__(self, path):
        self.path = path

class BRule:
    def __init__(self, name, rdef):
        self.name = name
        self.deps = []
        for ddef in rdef["deps"]:
            self.deps.append(BDep(ddef))
        self.cmds = rdef["cmds"]
        self.run = rdef.get("run", False)        
        self.color = rdef.get("color", "NONE")
        self.restart = rdef.get("restart", False)
        self.refresh = rdef.get("refresh", False)

class BTask:
    def __init__(self, name, cmds, color = "NONE"):
        self.name = name
        self.cmds = cmds
        self.color = color
        self.proc = None

    def procreadline(self, sline):
        print(ANSI[self.color] + self.name + ANSI["ENDC"] + " > " + ANSI[self.color] + sline)

    def procreaderror(self, sline):
        print(ANSI[self.color] + self.name + ANSI["BRIGHTWHITE"] + " ! " + ANSI["BRIGHTRED"] + sline)

    def run(self):        
        print(ANSI["GREEN"])
        print("running task: {} {}".format(ANSI["BRIGHTGREEN"], self.name))
        pargs = []
        if len(self.cmds) > 1:
            pargs = self.cmds[1:]        
        print(ANSI[self.color])
        self.proc = PopenProcess(
            self.cmds[0],
            self.procreadline,
            read_error_callback = self.procreaderror,
            proc_args = pargs,
            ignore_cwd = True
            )

    def kill(self):
        print(ANSI["RED"])
        print("killing task: {} {}".format(ANSI["BRIGHTRED"], self.name))
        self.proc.kill()

    def is_alive():
        return self.proc.is_alive()

class BDef:
    def __init__(self):
        self.rules = []        
        self.path = "bdef.yml"
        self.bdef = None
        self.cache = {}
        self.tasks = {}
    def fromdef(self, bdef):        
        self.bdef = bdef
        for ( name , rdef ) in self.bdef.items():            
            self.rules.append(BRule(name, rdef))
        return self
    def frompath(self, path = "bdef.yml"):
        self.path = path
        self.fromdef(yaml.load(open(path)))
        return self
    def cachepath(self):
        return self.path + ".cache"
    def putcache(self):
        yaml.dump(self.cache, open(self.cachepath(),"w"))
        return self
    def getcache(self):
        self.cache = ry(self.cachepath(),{})
        self.putcache()
        return self
    def getlastmodfromcache(self, path):
        if path in self.cache:
            return self.cache[path]
        return 0
    def updatecache(self):
        for rule in self.rules:            
            for dep in rule.deps:
                path = dep.path
                lastmod = getlastmod(path)
                self.cache[path] = lastmod
        self.putcache()
    def build(self, loop = False):        
        t = time.time()
        self.getcache()
        somechange = False
        for rule in self.rules:
            changed = False
            for dep in rule.deps:
                path = dep.path
                lastmodcache = self.getlastmodfromcache(path)
                lastmod = getlastmod(dep.path)
                if lastmod > lastmodcache:                    
                    changed = True
                    break
            if changed:
                somechange = True            
            if rule.run:
                if loop:                   
                    if rule.refresh:
                        browser.refresh()
                    elif rule.name in self.tasks:
                        task = self.tasks[rule.name]                        
                        if changed:                            
                            if rule.restart:                                
                                sys.exit(0)                                                    
                            else:
                                task.kill()
                                task.run()
                    else:
                        task = BTask(rule.name, rule.cmds, rule.color)
                        self.tasks[rule.name] = task                          
                        task.run()
                        time.sleep(1)
            elif changed:                
                print(ANSI["CYAN"])
                print("building {}".format(rule.name))                
                for cmd in rule.cmds:                    
                    print(ANSI["YELLOW"])
                    print("running command {}".format(cmd))
                    print(ANSI["YELLOW"])
                    returncode = runcmd(cmd)                    
                    print(ANSI["ENDC"])
                    if returncode > 0:
                        raise BuildCommandFailedException(rule.name, cmd)
                    else:
                        print(ANSI["GREEN"])
                        print("{} {} success".format(rule.name, cmd))                        
            else:
                if not loop:
                    print(ANSI["MAGENTA"])
                    print("{} up to date".format(rule.name))
        elapsed = time.time() - t
        if ( not loop ) or somechange:
            print(ANSI["BRIGHTGREEN"])
            print("build succeeded in {:.2f} seconds".format(elapsed))
            print(ANSI["ENDC"])        
        self.updatecache()
        return somechange

###################################################

b = BDef().frompath()

###################################################

def build_thread_func():
    global browserinit
    time.sleep(10)
    while True:        
        somechange = b.build(loop = True)        
        if somechange or browserinit:
            if browserinit:
                time.sleep(1)                
                browser.get('http://localhost:5000')
                browserinit = False
            else:                
                browser.refresh()
        time.sleep(1)

###################################################

bth = threading.Thread(target = build_thread_func)
bth.start()
#b.build(loop = True)

###################################################
