__pragma__("jsiter")

def putjsonbinfailed(err, json, callback):
    print("putjsonbin failed with",err)
    print("falling back to local storage")
    localStorage.setItem("jsonbin",json)
    callback(json, json)

def getjsonbinfailed(err, callback):
    print("getjsonbin failed with",err)
    print("falling back to local storage")
    content = localStorage.getItem("jsonbin")
    if content == None:
        print("no local jsonbin, falling back empty dict")
        content = '{"kind":"dict","enabled":true}'
    callback(content)

def putjsonbin(json, callback, id = None):
    method = "POST"
    url = "https://api.jsonbin.io/b"        
    if not ( id is None ):
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
    

def getjsonbin(id, callback, version = "latest"):
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
            lambda err: getjsonbinfailed(err, callback)
        ),
        lambda err: getjsonbinfailed(err, callback)
        )

__pragma__("nojsiter")