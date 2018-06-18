from serverutils.utils import read_string_from_file
from serverutils.utils import write_string_to_file

import json

def getint(obj, key, default):
    if not ( key in obj ):
        return default
    try:
        intvalue = int(obj[key])
        return intvalue
    except:
        return default

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
            repr+=" - {:15} : {}\n".format(fieldname, self.__dict__[fieldname])
        return repr

    def fromconfigobj(self, configobj):
        self.configobj = configobj
        self.config = configobj.get("config", {})
        self.configschema = configobj.get("configschema", {})
        self.globalobj = self.config.get("global", {})
        self.profilelistobj = self.config.get("profile", ["profile", {}])
        self.profilekey = self.profilelistobj[0]
        self.profileobj = self.profilelistobj[1]        
        self.fieldnames = [
            "token",
            "concurrency",
            "multipv",
            "selectmove",
            "ucioptions"
        ]
        self.token = self.profileobj.get("token", "xxxxxxxxxxxxxxxx")
        self.concurrency = getint(self.profileobj, "concurrency", 1)
        self.multipv = getint(self.profileobj, "multipv", 1)
        self.selectmove = self.profileobj.get("selectmove", "best")
        self.ucioptions = []
        try:
            ucioptionsobj = self.profileobj.get("ucioptions", {})            
            for uciname in ucioptionsobj:                
                ucivalue = ucioptionsobj[uciname]                
                self.ucioptions.append(UciOption(uciname, ucivalue))
        except:
            print("warning: there was a problem parsing uci options")
        return self

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