import requests
import json


jsonFile = open('./computedFiles/michelle.json')
jsonStr = jsonFile.read()
targetJson = json.loads(jsonStr)

#print(targetJson)

r = requests.post('http://127.0.0.1:5000/similarity?alg=cosinea', json=targetJson)

if(r.status_code==200):
    resp = r.json
else:
    r.raise_for_status()
#print(f"{resp['id']} with a similarity of {resp['value']}")
print(resp)