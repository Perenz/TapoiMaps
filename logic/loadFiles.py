import json
import os

targets = []
for file in os.listdir('./computedFiles'):
    if file.endswith('.json'):
        #print(file.split('.')[0])

        jsonFile = open('./computedFiles/'+file)
        jsonStr = jsonFile.read()
        data = json.loads(jsonStr)
        
        targets.append({'name':file.split('.')[0], 'data':data})

jsonFile = open('./targetFiles/testRoger.json')
jsonStr = jsonFile.read()
testDict = json.loads(jsonStr)