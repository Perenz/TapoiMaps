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

jsonFile = open('./targetFiles/'+testJsonName)
jsonStr = jsonFile.read()
testDict = json.loads(jsonStr)

RogerTw = sum(rogerDict.get(k) for k in set(rogerDict))
emmaTw = sum(emmaDict.get(k) for k in set(emmaDict))
testTw = sum(testDict[k] for k in set(testDict))

# **0.5 gives more importance to the fact that both cited the same topic instead of how much they had talked about it

# Problem: Longer profiles higher the similarity; it doesn't give value to different topic

#Both dict values are "normalized"
distEmma = sum(min(testDict.get(key,0)/testTw, emmaDict.get(key,0)/emmaTw)**0.5 for key in set(testDict) | set(emmaDict))
distRoger = sum(min(testDict.get(key,0)/testTw, rogerDict.get(key,0)/RogerTw)**0.5 for key in set(testDict) | set(rogerDict))

print('Similarity Emma: ', distEmma)
print('Similarity Roger: ', distRoger)

print('Emma/Roger: ', 1/(distEmma/distRoger))