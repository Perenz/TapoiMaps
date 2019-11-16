# DISTANCE "METRIC" IDEAS

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

#### Cons
The longer a profile is the higher will be the similarity since the probability of same topics discussion increases.
It doesn't give any value to different topics discussed by different profiles


## KNN with k=1
### Euclidean distance

Perform the similarity evaluation using the Euclidean distance and return the ID of the targetProfile having lowest for which the Euclidean distance with the testProfile is the lowest

#### Cons
It does not care about the number of all the topics discussed by a user


## Recommender system

## Cosine Similarity

Perform the similarity evaluation using the



problema: cosine sim a differenza della jaccard tiene conto del numero di reference quindi es:

​	test parla 20 volte di Calcio

​	target parla 40 volte di Calcio

​	Si avra' una cos sim X



​	Se un altro target parla di calcio 60 volte

​	Si avrà una cos sim Y < X  ---> Non è un problema dato che è ciò che voglio



Use a lemmatizer?

Use subcategories to find more common topic discussion

I can expand both user and count the number of common discussion that has been added

Can do some pre elaboration on the number of added discussions to give a prio to subcategories

Then use the proportion coeficient (>=1) the multiply the cos sim founded