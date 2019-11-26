import json
import os
import math

def normalizal2Dict(dic):
    '''
        Takes a dict and applies a l2 normalization on it

        Returns the normalized dict
    '''
    norm = math.sqrt(sum(dic[k]**2 for k in dic))
    normDict = {k:dic[k]/norm for k in dic}

    return normDict

def naiveMetric(x, y):  
    '''
    Callable function used to perform a naive similarity coefficent in the scikit pairwise_distances
    '''
    #Evaluate the l1 norm
    xTw = sum(x[k] for k in x)
    yTw = sum(y[k] for k in y)

    # **1/2 gives more importance to the fact that both cited the same topic instead of how much they had talked about it
    return sum(min(x.get(i,0)/xTw, y.get(i,0)/yTw)**(1/2) for i in set(x) | set(y))

def cosineSim_norm(dic1, dic2):
    '''
    function used to perform a l2 normalized cosine similarity between two dict
    '''
    dic1 = normalizal2Dict(dic1)
    dic2 = normalizal2Dict(dic2)

    return sum(dic1.get(k,0)*dic2.get(k,0) for k in set(dic1) | set(dic2))


def weightedJaccard(x,y):
    '''
    function used to perform the weighted jaccard distance between two dict
    '''
    num=0
    den=0

    for k in set(x) | set(y):
        num += min(x.get(k,0), y.get(k,0))
        den += max(x.get(k,0), y.get(k,0))

    #Avoid division by zero
    return num/max(1,den)

def normEuclidean(x,y):
    '''
    function used to perform the l2 normalized euclidean distance between two dict
    '''
    x=normalizal2Dict(x)
    y=normalizal2Dict(y)

    return math.sqrt(sum((x.get(k,0)-y.get(k,0))**2 for k in set(x) | set(y)))

def getTargets():
    '''
    Load the stored json files representing the user Profiles
    They are saved in dictionaries
    '''
    targets = []
    for file in os.listdir('./computedFiles'):
        if file.endswith('.json'):
            #print(file.split('.')[0])

            try:
                jsonFile = open('./computedFiles/'+file)
                jsonStr = jsonFile.read()
                data = json.loads(jsonStr)
            except json.JSONDecodeError:
                data = None
                           
            id = file.split('.')[0]

            #Load the profile json in targets
            if not data is None:
                targets.append({'id':id, 'data':data})

    return targets


class similarityEvaluator():
    '''
    Class used to run different algorithms for the evaluation of a similarity value
    '''
    def __init__(self):
        #Load all the files in dicts
        self.targets = getTargets()

    def computeCosineSimilarity(self, dfTest):
        '''
        Given a dataset representing a json profile compute the cosine similarity between it and 
        the stored users

        Returns the id of the most similar one
        '''
        cosMat = []
        #For each target
        for t in self.targets:
            cosMat.append(cosineSim_norm(dfTest, t['data']))
            
        #Get index of the max
        maxN = round(max(cosMat), 6)

        maxIDs = [self.targets[i]['id'] for i,j in enumerate(cosMat) if round(j, 6)==maxN]

        return maxIDs, maxN

    def computeEuclideanDist(self, dfTest):
        '''
        Given a dataset representing a json profile compute the Euclidean Distnace between it and 
        the stored users

        Returns the id of the most similar one
        '''
        eucMat = []
        for t in self.targets:
            eucMat.append(normEuclidean(dfTest, t['data']))


        minN = round(min(eucMat), 6)
        maxIDs = [self.targets[i]['id'] for i,j in enumerate(eucMat) if round(j, 6)==minN]

        return maxIDs, minN


    def computeNaiveDist(self, dfTest):
        '''
        Given a dataset representing a json profile compute an algorithm for the evaluation of a similarity value between it and 
        the stored users

        Returns the id of the most similar one
        '''
        naiveMat = []
        for t in self.targets:
            naiveMat.append(naiveMetric(dfTest, t['data']))

        print(naiveMat)

        maxN = round(max(naiveMat), 6)
        maxNames = [self.targets[i]['id'] for i,j in enumerate(naiveMat) if round(j, 6)==maxN]
        return maxNames, maxN

    def computeJaccardDist(self, dfTest):
        '''
        Given a dataset representing a json profile compute the Weighted Jaccard Similarity between it and 
        the stored users

        Returns the id of the most similar one
        '''
        jacMat = []
        for t in self.targets:
            jacMat.append(weightedJaccard(dfTest, t['data']))

        print(jacMat)
        
        maxN = round(max(jacMat), 6)
        maxIDs = [self.targets[i]['id'] for i,j in enumerate(jacMat) if round(j, 6)==maxN]
      

        return maxIDs, maxN

