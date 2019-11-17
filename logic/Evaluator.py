import json
import os
import pandas as pd
from numpy import argmax, argmin
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, pairwise_distances
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


def metricFunc(x, y):
        xTw = sum(x)
        yTw = sum(y)

        # **0.5 gives more importance to the fact that both cited the same topic instead of how much they had talked about it
        # Problem: Longer profiles higher the similarity; it doesn't give value to different topic
        dist = sum(min(x[i]/xTw, y[i]/yTw)**0.5 for i in range(len(x)))
        return dist

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

    def computeNaiveDist(self, dfTest):
        totalDF = self.targets.append(dfTest, sort=False).fillna(0)

        #Give a function as parameter 'metric' 
        naiveMat = pairwise_distances(totalDF, metric=metricFunc)
        print(naiveMat)
        naiveSim = naiveMat[-1, :-1]
        minInd = argmax(naiveSim)
        return totalDF.iloc[minInd].name, naiveSim[minInd]

