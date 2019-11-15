# IDEAS

## Naive similarity calculation

Perform the similarity evaluation between 2 profiles in a simple and brute-forced way:
```
testProfile = dict(testProfile.json)
targetProfile = dict(targetProfile.json)

simil = 0
for key in testProfile.keys():
    if key in targetProfile.keys():
        simil += max(testProfile[key], targetProfile[key])
        
max(simil)
```


## KNN with k=1
### Euclidean distance

Perform the similarity evaluation using the Euclidean distance and return the ID of the targetProfile having lowest for which the Euclidean distance with the testProfile is the lowest

#### Cons
It does not care about the number of all the topics discussed by a user


## Recommender system

## Cosine Similarity
