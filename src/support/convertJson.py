import json
import re

jsonFileName = 'roger.json'

jsonFile = open('./jsonFiles/'+jsonFileName)
jsonStr = jsonFile.read()
jsonDict = json.loads(jsonStr)

newDict = {key:2 for key in jsonDict.keys()}

#Remove 'http://en.wikipedia.org/wiki/Category:' from keys' names
newDict = {key[38:]:jsonDict[key] for key in jsonDict.keys()}

jsonFile.close()

with open('./computedFiles/'+jsonFileName, 'w') as newJson:
    json.dump(newDict, newJson, separators=(',\n\t', ':'))

#print(newDict)