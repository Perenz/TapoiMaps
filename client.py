import requests
import json


jsonFile = open('./computedFiles/michelle.json')
jsonStr = jsonFile.read()
targetJson = json.loads(jsonStr)

#print(targetJson)

r = requests.get('http://127.0.0.1:5000/similarity?alg=jaccard', json=targetJson)

resp = r.json()
#print(f"{resp['id']} with a similarity of {resp['value']}")
print(resp)