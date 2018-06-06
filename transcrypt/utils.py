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

def putjsonbinfailed(err, json, callback):
    print("putjsonbin failed with",err)
    print("falling back to local storage")
    localStorage.setItem("jsonbin",json)
    callback(json, json)

def getlocalcontent():
    print("getting local content")
    content = localStorage.getItem("jsonbin")
    if content == None:
        print("no local jsonbin, falling back to empty dict")
        content = '{}'
    return content

def getjsonbinfailed(err, callback):
    print("getjsonbin failed with",err)    
    callback(getlocalcontent())

def putjsonbin(json, callback, id = None):

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
            lambda content: callback(json, content),
            lambda err: putjsonbinfailed(err, json, callback)
        ),
        lambda err: putjsonbinfailed(err, json, callback)
    )
    

def getjsonbin(id, callback, errcallback, version = "latest"):

    if id == "local":
        callback(getlocalcontent())
        return

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