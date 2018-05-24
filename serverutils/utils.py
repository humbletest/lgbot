import threading
import inspect
import urllib3
import json

#############################################

http = urllib3.PoolManager()

def geturl(url):
    print("get url", url)
    r = http.request("GET", url)
    content = r.data.decode("utf-8")
    return content

def postjson(url, obj):
    print("post json", url, obj)
    r = http.request('POST', url, headers={'Content-Type': 'application/json'}, body=json.dumps(obj))
    content = r.data.decode("utf-8")
    return content

#############################################

lock = threading.Lock()

SEP = "-" * 60

class SafeLimitedUniqueQueueList:
    def __init__(self, max = 10, overflow_callback = None):
        self.items = []
        self.max = max
        self.overflow_callback = overflow_callback
    def enqueue(self, item):
        if item in self.items:
            return
        lock.acquire()        
        self.items = [ item ] + self.items
        if len(self.items) > self.max:
            removed_item = self.items.pop()
            if not ( self.overflow_callback is None ):
                self.overflow_callback(removed_item)
        lock.release()
    def dequeue(self):
        if len(self.items) == 0:
            return None
        lock.acquire() 
        item = self.items.pop()
        lock.release()
        return item

def prettylog(lines):
    print(SEP)
    for line in lines:
        print("- " + line)
    print(SEP)