import json

print("loading fbcreds")
fbcreds = json.loads(open("firebase/fbcreds.json").read())

print("fbcreds", fbcreds)

print("importing pyrebase")
import pyrebase

print("initializing pyrebase")
firebase = pyrebase.initialize_app(fbcreds)

print("creating db")
db = firebase.database()

print("setting value")
db.child("foo").set("bar")

print("getting value")
print(db.child("foo").get().val())
