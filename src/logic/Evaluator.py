import json
import os
import pandas as pd
from numpy import argmax, argmin
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, pairwise_distances
from sklearn.preprocessing import normalize


def getTargetsDF():
    '''
    Load the stored json files representing the user Profiles
    They are saved in pandas dataframes
    '''
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

            targets.append(dfT)

    return targets


def naiveMetric(x, y):  
    '''
    Callable function used to perform a naive similarity coefficent in the scikit pairwise_distances
    '''
    xTw = sum(x)
    yTw = sum(y)

    # **2 gives more importance to the fact that both cited the same topic instead of how much they had talked about it
    # Problem: Longer profiles higher the similarity; it doesn't give value to different topic
    dist = sum(min(x[i]/xTw, y[i]/yTw) for i in range(len(x)))
    return dist

def weightedJaccard(x,y):
    '''
    Callable function used to perform the jaccard similarity in the scikit pairwise_distances
    '''
    num=0
    den=0
    for i in range(len(x)):
        num += min(x[i],y[i])
        den += max(x[i],y[i])

    return 1 - num/max(1,den)


class similarityEvaluator():
    '''
    Class used to run different algorithms for the evaluation of a similarity value
    '''
    def __init__(self):
        #Load all the files in a dataframe/numpy
        self.targets = getTargetsDF()

    def computeCosineSimilarity(self, dfTest):
        '''
        Given a dataset representing a json profile compute the cosine similarity between it and 
        the stored users

        Returns the id of the most similar one
        '''
        cosMat = []
        for i in range(len(self.targets)):
            cosMat.append(cosine_similarity(dfTest.append(self.targets[i], sort=False).fillna(0))[0,1])

        #print(cosMat)

        ind = argmax(cosMat)
        return self.targets[ind].iloc[0].name, cosMat[ind]

    def computeEuclideanDist(self, dfTest):
        '''
        Given a dataset representing a json profile compute the Euclidean Distnace between it and 
        the stored users

        Returns the id of the most similar one
        '''
        eucMat = []
        for i in range(len(self.targets)):
            eucMat.append(euclidean_distances(normalize(dfTest.append(self.targets[i], sort=False).fillna(0)))[0,1])

        #print(eucMat)

        ind = argmin(eucMat)
        return self.targets[ind].iloc[0].name, eucMat[ind]


    def computeNaiveDist(self, dfTest):
        '''
        Given a dataset representing a json profile compute an algorithm for the evaluation of a similarity value between it and 
        the stored users

        Returns the id of the most similar one
        '''
        naiveMat = []
        for i in range(len(self.targets)):
            naiveMat.append(pairwise_distances(dfTest.append(self.targets[i], sort=False).fillna(0), metric=naiveMetric)[0,1])

        #print(naiveMat)

        ind = argmax(naiveMat)
        return self.targets[ind].iloc[0].name, naiveMat[ind]

    def computeJaccardDist(self, dfTest):
        '''
        Given a dataset representing a json profile compute the Weighted Jaccard Similarity between it and 
        the stored users

        Returns the id of the most similar one
        '''
        jacMat = []
        for i in range(len(self.targets)):
            jacMat.append(pairwise_distances(dfTest.append(self.targets[i], sort=False).fillna(0), metric=weightedJaccard)[0,1])

        #print(jacMat)

        ind = argmin(jacMat)
        return self.targets[ind].iloc[0].name, jacMat[ind]

