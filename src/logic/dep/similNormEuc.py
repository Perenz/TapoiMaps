import math
import json

target1JsonName = 'emma.json'

target2JsonName = 'roger.json'

testJsonName = 'testRoger.json'

jsonFile = open('./computedFiles/'+target1JsonName)
jsonStr = jsonFile.read()
emmaDict = json.loads(jsonStr)

jsonFile = open('./computedFiles/'+target2JsonName)
jsonStr = jsonFile.read()
rogerDict = json.loads(jsonStr)
#print(len(rogerDict))

jsonFile = open('./targetFiles/'+testJsonName)
jsonStr = jsonFile.read()
testDict = json.loads(jsonStr)

#print(testDict)

RogerTw = sum(rogerDict.get(k) for k in set(rogerDict))
emmaTw = sum(emmaDict.get(k) for k in set(emmaDict))

print('Roger tweets', RogerTw)
print('Emma tweets', emmaTw)

print(len(set(emmaDict).intersection(set(testDict))))
print(len(set(rogerDict).intersection(set(testDict))))


normEmma = math.sqrt(sum(emmaDict[k]**2 for k in emmaDict))
normedEmma = {k:emmaDict[k]/normEmma for k in emmaDict}

normRoger = math.sqrt(sum(rogerDict[k]**2 for k in rogerDict))
normedRoger = {k:rogerDict[k]/normRoger for k in rogerDict}

normTest = math.sqrt(sum(testDict[k]**2 for k in testDict))
normedDict = {k:testDict[k]/normTest for k in testDict}

distEmma = 0
for k in set(emmaDict) & set(testDict):
    distEmma = distEmma + math.sqrt(((normedDict.get(k,0)-normedEmma.get(k,0)))**2)

distRoger = 0
for k in set(rogerDict) & set(testDict):
    distRoger = distRoger + math.sqrt(((normedDict.get(k,0)-normedRoger.get(k,0)))**2)

#distEmma = math.sqrt(sum(((testDict.get(k,0) - emmaDict.get(k,0))/(max(testDict.get(k,0), emmaDict.get(k,0))-min(testDict.get(k,0), emmaDict.get(k,0))))**2) for k in set(testDict) | set(emmaDict)))
#distRoger = math.sqrt(sum(((testDict.get(k,0) - rogerDict.get(k,0))/(max(testDict.get(k,0), rogerDict.get(k,0))-min(testDict.get(k,0), rogerDict.get(k,0))))**2) for k in set(testDict) | set(rogerDict)))


print(f"Dist Emma:{distEmma}")
print(f"Dist Roger:{distRoger}")

print('Emma/Roger: ', distEmma/distRoger)

