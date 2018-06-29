items = [    
    {"mainkey": "A", "subkey": 3},
    {"mainkey": "A", "subkey": 8},
    {"mainkey": "B", "subkey": 3},
    {"mainkey": "A", "subkey": 11},
    {"mainkey": "B", "subkey": 15},
    {"mainkey": "A", "subkey": 15},
    {"mainkey": "B", "subkey": 8},
    {"mainkey": "B", "subkey": 11}
]

print("items", items)

sortsub = sorted(items, key = lambda item: item["subkey"])
print("sortsub", sortsub)

sortmain = sorted(sortsub, key = lambda item: item["mainkey"])
print("sortmain", sortmain)

print("sortsub", sortsub)

print("items", items)