import sys
import json

from serverutils.utils import read_string_from_file

import pyrebase

acc = sys.argv[1]

print("set remote", acc)

fbcreds = json.loads(open("firebase/fbcreds.json").read())
firebase = pyrebase.initialize_app(fbcreds)

db = firebase.database()

localconfig = read_string_from_file("localconfig.json","{}")

print("setting remote from localconfig {} characters".format(len(localconfig)))

db.child(acc).set(localconfig)

print("done")
