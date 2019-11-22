import requests
import src.logic.Evaluator
import json



jsonFile = open('./computedFiles/michelle.json')
jsonStr = jsonFile.read()
targetJson = json.loads(jsonStr)

#print(targetJson)

# https://tapoimaps.herokuapp.com:5000
# http://127.0.0.1:5000/similarity?alg=jaccard
#r = requests.post('http://127.0.0.1:5000/similarity?alg=cosine', json=targetJson)

#r = requests.post('http://127.0.0.1:5000/profiles?name=prova1', json=targetJson)

r = requests.delete('http://127.0.0.1:5000/profiles?name=prova1')


resp = r.json()
r.raise_for_status()
#print(f"{resp['id']} with a similarity of {resp['value']}")
print(resp)