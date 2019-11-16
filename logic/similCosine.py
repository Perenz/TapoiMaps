import math
import json
import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def normalizaDict(dic):
    norm = math.sqrt(sum(dic[k]**2 for k in dic))
    normedDict = {k:dic[k]/norm for k in dic}

    return normedDict

def cosine_dic(dic1, dic2):
    dic1 = normalizaDict(dic1)
    dic2 = normalizaDict(dic2)

    num=0
    for k in set(dic1) | set(dic2):
        num += dic1.get(k,0)*dic2.get(k,0)

    return num


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



'''
RogerTw = sum(rogerDict.get(k) for k in set(rogerDict))
emmaTw = sum(emmaDict.get(k) for k in set(emmaDict))
testTw = sum(testDict[k] for k in set(testDict))
'''

'''
print(len(set(targets[0]['data']).intersection(set(testDict))))
print(len(set(targets[2]['data']).intersection(set(testDict))))

distEmma = cosine_dic(testDict, targets[0]['data'])

distRoger = cosine_dic(testDict, targets[2]['data'])
'''

dfTest = pd.DataFrame(testDict, index=['test'])
dfEmma = pd.DataFrame(targets[0]['data'], index=['emma'])
dfRoger = pd.DataFrame(targets[2]['data'], index=['roger'])

df = dfTest.append([dfEmma, dfRoger], sort=False).fillna(0)

cosMat = cosine_similarity(df)

cosSim = cosMat[0, 1:]

print(cosMat)
print(cosSim)

maxInd = np.argmax(cosSim)+1


print(cosMat[0,maxInd])
print(df.iloc[maxInd].name)



#print(df)

#print('Emma similarity: ', distEmma)
#print('Roger similarity: ', distRoger)
