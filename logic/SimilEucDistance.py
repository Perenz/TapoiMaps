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
print(len(rogerDict))

jsonFile = open('./computedFiles/'+testJsonName)
jsonStr = jsonFile.read()
testDict = json.loads(jsonStr)

#print(testDict)

RogerTw = sum(rogerDict.get(k) for k in set(rogerDict))
emmaTw = sum(emmaDict.get(k) for k in set(emmaDict))

print('Roger tweets', RogerTw)
print('Emma tweets', emmaTw)


distEmma = math.sqrt(sum((testDict.get(k,0) - emmaDict.get(k,0))**2 for k in set(testDict) | set(emmaDict)))
distRoger = math.sqrt(sum((testDict.get(k,0) - rogerDict.get(k,0))**2 for k in set(testDict) | set(rogerDict)))


print(f"Dist Emma:{distEmma}")
print(f"Dist Roger:{distRoger}")

