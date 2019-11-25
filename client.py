import requests
import json



jsonFile = open('./testFiles/testRoger.json')
jsonStr = jsonFile.read()
targetJson = json.loads(jsonStr)

#print(targetJson)

# https://tapoimaps.herokuapp.com:5000
# http://127.0.0.1:5000/similarity?alg=jaccard
#r = requests.get('http://127.0.0.1:5000/similarity?alg=jaccard', json=targetJson)

#r = requests.get('http://127.0.0.1:5000/profiles')

#r = requests.get('http://127.0.0.1:5000/profiles/tim')

#r = requests.post('http://127.0.0.1:5000/profiles?id=prova', json=targetJson)

r = requests.delete('http://127.0.0.1:5000/profiles?id=prova')


resp = r.json()
r.raise_for_status()
#print(f"{resp['id']} with a similarity of {resp['value']}")
print(resp)