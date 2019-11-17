import json
import os
import pandas as pd
from numpy import argmax, argmin
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.preprocessing import normalize


def getTargetsDF():
    df = pd.DataFrame()
    for file in os.listdir('./computedFiles'):
        if file.endswith('.json'):
            #print(file.split('.')[0])

            jsonFile = open('./computedFiles/'+file)
            jsonStr = jsonFile.read()
            data = json.loads(jsonStr)
            
            name = file.split('.')[0]

            dfT = pd.DataFrame(data, index=[name])

            #print(dfT)

            df = df.append(dfT, sort=False)

    return df.fillna(0)


class similarityEvaluator():
    def __init__(self):
        #Load all the files in a dataframe/numpy
        self.targets = getTargetsDF()

    def computeCosineSimilarity(self, dfTest):
        totalDF = self.targets.append(dfTest, sort=False).fillna(0)
        cosMat = cosine_similarity(totalDF)
        print(cosMat)

        #print(dfTest)
        cosSim = cosMat[-1, :-1]

        maxInd = argmax(cosSim)
        return totalDF.iloc[maxInd].name, cosSim[maxInd]

    def computeEuclideanDist(self, dfTest):
        totalDF = self.targets.append(dfTest, sort=False).fillna(0)
        normDf = normalize(totalDF)
        eucMat = euclidean_distances(normDf)
        print(eucMat)

        eucSim = eucMat[-1, :-1]
        minInd = argmin(eucSim)
        return totalDF.iloc[minInd].name, eucSim[minInd]

