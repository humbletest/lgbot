__pragma__("jsiter")

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
            lambda err: print(err)
        ),
        lambda err: print(err)
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
            lambda err: print(err)
        ),
        lambda err: print(err)
        )

__pragma__("nojsiter")