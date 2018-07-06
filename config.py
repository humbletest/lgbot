from serverutils.utils import read_string_from_file
from serverutils.utils import write_string_to_file

import json

import os

#########################################################

def APP_MODE():
    return os.environ["APP_MODE"]

def IS_DEV():
    return APP_MODE() == "dev"

def IS_PROD():
    return APP_MODE() == "prod"

SELECTMOVE_WITHOUT_ENGINE_LIST = [
    "random",
    "capturerandom"
]

#########################################################

class UciOption:
    def __init__(self,
        name,
        value
    ):
        self.name = name
        self.value = str(value)

    def __repr__(self):
        return("[UciOption '{}' : '{}']".format(self.name, self.value))

class Config:
    def __init__(
        self,
        path = "localconfig.json"
    ):
        self.path = path
        self.fromfile()

    def __repr__(self):
        repr = "[config {}]\n".format(self.path)
        for fieldname in self.fieldnames:
            value = self.__dict__[fieldname]
            repr+=" - {:15} : {} {}\n".format(fieldname, value, type(value))
        repr += " - needs engine : {}".format(self.needsengine())
        return repr

    def parse(self,
        obj,
        key,
        default = None,
        devdefault = None,
        proddefault = None,
        kinds = [ str, int, float ],
        reg = True,
        conv = None,
        check = None
    ):
        value = default
        if IS_DEV() and ( not ( devdefault is None ) ):
            value = devdefault
        elif IS_PROD() and ( not ( proddefault is None ) ):
            value = proddefault
        devkey = key + ":dev"
        prodkey = key + ":prod"
        if ( key in obj ) or ( devkey in obj ) or ( prodkey in obj ):
            temp = None
            if IS_DEV() and ( devkey in obj ):
                temp = obj[devkey]
            elif IS_PROD() and ( prodkey in obj ):
                temp = obj[prodkey]
            elif ( key in obj ):
                temp = obj[key]                        
            if type(temp) in kinds:
                ok = True
                if not ( conv is None ):
                    try:
                        temp = conv(temp)                        
                    except:
                        print("warning: conv failed on", key, temp)
                        ok = False
                if ok:
                    if not ( check is None ):
                        ok = check(temp)
                    if ok:                        
                        value = temp
                    else:
                        print("warning: check failed on", key, temp)

        self.__dict__[key] = value
        if reg:
            self.fieldnames.append(key)            

    def fromconfigobj(self, configobj):
        self.configobj = configobj
        self.config = configobj.get("config", {})
        self.configschema = configobj.get("configschema", {})
        self.globalobj = self.config.get("global", {})
        self.profilelistobj = self.config.get("profile", ["profile", {}])
        self.profilekey = self.profilelistobj[0]
        self.profileobj = self.profilelistobj[1]        
        self.fieldnames = []        
        self.parse(self.globalobj, "simpleserverurl", devdefault = "http://localhost:4000", proddefault = "http://localhost:4000")        
        self.parse(self.globalobj, "flaskserverurl", devdefault = "http://localhost:5000", proddefault = "http://liguibot.herokuapp.com")        
        self.parse(self.globalobj, "autostartbot", default = 10, conv = int, check = lambda i: i>=0 and i<=300)
        self.parse(self.globalobj, "autostartengine", default = 10, conv = int, check = lambda i: i>=0 and i<=300)
        self.parse(self.profileobj, "token", default = "xxxxxxxxxxxxxxxx")        
        self.parse(self.profileobj, "concurrency", default = 1, conv = int, check = lambda i: i>=1 and i<=10)        
        self.parse(self.profileobj, "enginename", devdefault = "stockfish9.exe", proddefault = "stockfish9")
        self.parse(self.profileobj, "multipv", default = 1, conv = int, check = lambda i: i>=1 and i<=500)        
        self.parse(self.profileobj, "selectmove", default = "best")        
        self.parse(self.profileobj, "ponder", default = "none")        
        self.parse(self.profileobj, "accept", kinds = [ dict ], reg = False, default = {})
        self.parse(self.accept, "opponent", kinds = [ list ], default = ['bot', 'human'])
        self.parse(self.accept, "timecontrol", kinds = [ list ], default = ['ultraBullet', 'bullet', 'blitz', 'rapid', 'classical', 'correspondence'])
        self.parse(self.accept, "variant", kinds = [ list ], default = ['standard', 'fromPosition', 'antichess', 'atomic', 'chess960', 'crazyhouse', 'horde', 'kingOfTheHill', 'racingKings', 'threeCheck'])
        self.parse(self.accept, "mode", kinds = [ list ], default = ['casual', 'rated'])
        self.parse(self.profileobj, "book", kinds = [ dict ], reg = False, default = {})
        self.parse(self.book, "strategy", default = "best")
        self.parse(self.book, "minweight", default = 1, conv = int, check = lambda i: i>=0 and i<=10000)
        self.ucioptions = []
        try:
            ucioptionsobj = self.profileobj.get("ucioptions", {})            
            for uciname in ucioptionsobj:                
                ucivalue = ucioptionsobj[uciname]                
                self.ucioptions.append(UciOption(uciname, ucivalue))
        except:
            print("warning: there was a problem parsing uci options")
        self.fieldnames.append("ucioptions")                
        return self

    def needsengine(self):
        if self.selectmove in SELECTMOVE_WITHOUT_ENGINE_LIST:
            return False
        return True

    def fromjsonstr(self, configjsonstr):
        try:
            configobj = json.loads(configjsonstr)
        except:
            print("config string could not be parsed")
            return self        
        return self.fromconfigobj(configobj)

    def fromfile(self, path = None, setpath = True):
        if path is None:
            path = self.path
        if setpath:
            self.path = path
        configjsonstr = read_string_from_file(path, "{}")        
        return self.fromjsonstr(configjsonstr)

config = Config()

if __name__ == "__main__":
    print(config)