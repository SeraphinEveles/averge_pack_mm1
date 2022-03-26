import commentjson
import os
import re

items = []
funcs = []
itemToFunc = {}

with open(os.path.join(".", "resources", "tests", "output", "itemCodes.json"), "r") as itemsFile:
    items = commentjson.load(itemsFile)

dirname = os.path.join(".", "scripts")
for filename in os.listdir(dirname):
    if os.path.isfile(os.path.join(dirname, filename)):
        print(f"Reading: {filename}")
        with open(os.path.join(dirname, filename), "r") as funcsFile:
            lines = funcsFile.read().split("\n")
            funcName = ""
            for line in lines:
                func = re.search(r"function ([^\(]*)", line.strip())
                if func:
                    funcName = func.group(1)
                    funcs.append(funcName)
                item = re.search(r"has\(\"(.*)\"\)", line.strip())
                if item:
                    itemName = item.group(1)
                    if itemName not in items:
                        print(f"> {funcName}")
                        print(f">  '{itemName}' not a valid item code")
                    else:
                      if funcName != "canGoMode":
                        if itemName not in itemToFunc:
                          itemToFunc[itemName] = []
                        itemToFunc[itemName].append(funcName)
funcs = set(funcs)
funcs = list(funcs)
funcs.sort()

with open(os.path.join(".", "resources", "tests", "output", "funcNames.json"), "w+") as funcsJSON:
    funcsJSON.write(commentjson.dumps(funcs, indent=2))
with open(os.path.join(".", "resources", "tests", "output", "itemToFunc.json"), "w+") as iFuncJSON:
    iFuncJSON.write(commentjson.dumps(itemToFunc, indent=2))
