import json
import os
import pandas as pd
from numpy import argmax, argmin
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, pairwise_distances
from sklearn.preprocessing import normalize


def getTargetsDF():
    targets = []
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
            targets.append(dfT)
            #df = df.append(dfT, sort=False)

    return targets


def metricFunc(x, y):
        xTw = sum(x)
        yTw = sum(y)

        # **2 gives more importance to the fact that both cited the same topic instead of how much they had talked about it
        # Problem: Longer profiles higher the similarity; it doesn't give value to different topic
        dist = sum(min(x[i]/xTw, y[i]/yTw) for i in range(len(x)))
        return dist

def weightedJaccard(x,y):
    num=0
    den=0
    for i in range(len(x)):
        num += min(x[i],y[i])
        den += max(x[i],y[i])

    return 1 - num/max(1,den)


class similarityEvaluator():
    def __init__(self):
        #Load all the files in a dataframe/numpy
        self.targets = getTargetsDF()

    def computeCosineSimilarity(self, dfTest):
        cosMat = []
        for i in range(len(self.targets)):
            cosMat.append(cosine_similarity(dfTest.append(self.targets[i], sort=False).fillna(0))[0,1])

        #print(cosMat)

        ind = argmax(cosMat)
        return self.targets[ind].iloc[0].name, cosMat[ind]

    def computeEuclideanDist(self, dfTest):
        eucMat = []
        for i in range(len(self.targets)):
            eucMat.append(euclidean_distances(normalize(dfTest.append(self.targets[i], sort=False).fillna(0)))[0,1])

        #print(eucMat)

        ind = argmin(eucMat)
        return self.targets[ind].iloc[0].name, eucMat[ind]


    def computeNaiveDist(self, dfTest):
        naiveMat = []
        for i in range(len(self.targets)):
            naiveMat.append(pairwise_distances(dfTest.append(self.targets[i], sort=False).fillna(0), metric=metricFunc)[0,1])

        #print(naiveMat)

        ind = argmax(naiveMat)
        return self.targets[ind].iloc[0].name, naiveMat[ind]

    def computeJaccardDist(self, dfTest):
        jacMat = []
        for i in range(len(self.targets)):
            jacMat.append(pairwise_distances(dfTest.append(self.targets[i], sort=False).fillna(0), metric=weightedJaccard)[0,1])

        #print(jacMat)

        ind = argmin(jacMat)
        return self.targets[ind].iloc[0].name, jacMat[ind]

