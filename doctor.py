import sys

from serverutils.utils import read_string_from_file
from serverutils.utils import write_string_to_file

acc = sys.argv[1]

if acc == "-r":
    print("restoring")
    write_string_to_file("config.py", read_string_from_file("config.old.py",""))
    write_string_to_file("server.py", read_string_from_file("server.old.py",""))
else:
    print("doctoring source files in [{}]".format(acc))

    config = read_string_from_file("config.py","")
    write_string_to_file("config.old.py", config)

    config = config.replace("liguibot", acc)
    write_string_to_file("config.py", config)

    server = read_string_from_file("server.py","")
    write_string_to_file("server.old.py", server)

    server = server.replace("lgbotconfig", acc + "config")
    write_string_to_file("server.py", server)
    