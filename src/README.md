# DISTANCE "METRIC" IDEAS

## Naive similarity calculation

Perform the similarity evaluation between 2 profiles in a simple and 'brute-forced' way:
```python
def metricFunc(x, y):
        xTw = sum(x)
        yTw = sum(y)
        dist = sum(min(x[i]/xTw, y[i]/yTw)**2 for i in range(len(x)))
        return dist
    
def computeNaiveDist(self, testDF):
        naiveMat = []
        for i in range(len(targetSDF):
            naiveMat.append(pairwise_distances(dfTest.append(targetsDF[i], 					sort=False).fillna(0), metric=metricFunc)[0,1])

        print(naiveMat)

        ind = argmax(naiveMat)
        return targetDF.id, naiveMat[ind]
```

Each value of both vectors is l1 "normalized" with the number of references for that profile so they are weighted and their value is relative to that profile.

A fixed real coefficient can be used to give more value to the fact that the two compared profiles just share a common topic instead of the number of their references for that topic



#### Cons

The longer a profile is the higher will be the similarity since the probability of same topics discussion increases.
It doesn't give any value to different topics discussed by different profiles




## Euclidean distance

Perform the similarity evaluation using the Normalized Euclidean distance and return the ID of the targetProfile for which the Euclidean distance with the testProfile is the lowest.

![Euclidean distance](./images/distance_euclidean.gif)

Better accuracy can be obtained normalizing the vector x and y.

I used a l2-normalization to keep the coefficients small

So, for each profile, every topic reference counter was divided for the total number of references made by that user.


#### Cons
It's is not the best metric with sparse data like profiles. They are sparse because we have a lot of dimensions. Moreover when the euclidean distance is used to perform distance evaluation on two vectors corresponding to words counter of a document (That's the idea of our application too) does not return meaningful results. 

Here's an [example]('http://mlwiki.org/index.php/Euclidean_Distance'):


![Euclidean distance High dimensionality](./images/Euchighdim.png)

P3 and P4 (7 common categories) must be more similar to each other than P1 and P2 (0 common categories). 



## Weighted Jaccard distance

Treating the user profile as a set allows us to apply the Jaccard similarity coefficient which is used to obtain the Jaccard distance that measures dissimilarity betweem two sets.

![Euclidean distance](./images/jaccard.svg)

This would be restrictive for our case since it doesn't give any importance to the number of references that a user had for a certain topic.

Suppose we are evaluating the similarity between two profiles x and y.
They can be seen as two vectors with all non-negative values. (Which is exactly our situation)
Then the Jaccard similarity coefficient is defined as:

![Euclidean distance](./images/wjaccard.svg)

This coefficient is weighted with reference to number of references the two profiles had with the topics
From there we can obtain the Weighted Jaccard distance as:

![Euclidean distance](./images/wjaccard2.svg)

### Cons

With the simple Jaccard distance no clue is given to number of references for each topic

The weighted Jaccard similarity resolves this problem but it is still less efficient than the cosine similarity





## Cosine Similarity

Perform the similarity evaluation using the cosine similarity 

![Euclidean distance](./images/cosine.png)



Since it measures the angle between the two profiles we don't worry about the length of the profiles but about the distance in which each profile points which is described from the topics the user talked about.

It is similar to the Weighted Jaccard coefficient but the Cosine similarity can be  performed using the scikit library which returns better performances than the implementation of the Jaccard through a callable function.




### Performances

| Distance Metric           | Calls # | Average time (s) * | Min time (s) | Max time (s) |
| ------------------------- | ------- | ------------------ | ------------ | ------------ |
| Cosine similarity         | 5       | 0.953              | 9.173        | 9.751        |
| Weighted Jaccard distance | 5       | 1.080              | 1.040        | 1.105        |
| Euclidean distance        | 5       | 0.949              | 9.107        | 9.663        |
| Naive similarity          | 5       | 1,069              | 1,004        | 1,099        |

*All the time values include debug printing operations



We can easily observe that those evaluation performed using the scikit library are 10% more efficient than those that used a function defined by us.

In addition to Cosine similarity's precision, as explained before it results more efficient than the Jaccard's one, which is the slowest. Indeed it averages a time of 1.080 s, quite similar to the Naive algorithm which showed evidents problem, both under performances and precision.

Although Euclidean distance had the best results in term of time, being a little bit better than Cosine similarity, this one gives more precise answers in term of profile matching since it doesn't have all the problems Euclidean algorithm presents which have been discussed before.



### Improve Similarity Result

Since that point we have talked about matching a test profile, presented with a json format, with target profiles in order to return the most similar one.

We talked about different matching algorithm to identify the most similar, each with its pros and cons in term of both performances and precision.

The comparison we are trying to accomplish is based on the Wikipedia's categories the users talk on twitter with the number of times this topic had been discussed. At first an easy computation on the given categories can be enough to obtain satisfactory results, with increasing targets and growing topics these provided data may not be enough.

So pre-processing the given profiles can be useful and might improve our results.
Next i am going to discuss about some elaboration that could bring significant the algorithms mentioned before.



#### Wikipedia Categories

Wikipedia provides navigation links to pages in a hierarchy of categories which define characteristics of a topic and which users can browse and find sets of pages on topic defined by those characteristics. 

Categories are organized as overlapping trees formed by creating link between inter-related categories. Any category may contain subcategories, and it is possible for a category to be a subcategory of more than one "parent". Here's an example of what is meant with overlapping trees:



![Euclidean distance](./images/wikitrees.png)



A clear use for categories is that of finding more categories which two users talk about, starting from those in their profile overview and adding the parents category to the user description associated with the same (or a lower) number of references of the main category from which the additional information had been extracted. 

What does that mean?
Referring to the next picture we can see an easy example of relations between more categories.
Suppose USER A talked a lot about Culture while USER B about Art several times.
We all agree that two profiles such those are quite correlated.
The application of the algorithms over these two profiles would obviously return a null similarity since the two don't share any categories. But, if we could expand USER B profiles adding the parent category Culture to its overview and launch the algorithms over these modified profiles the result will clearly change because now an important matching would be caught.




![Euclidean distance](./images/wikistruct.png)



This can result as a big improvement for the similarity coefficient  because the new algorithms would catch new matches that the older wouldn't get.  On the other hand this elaboration "removes" specific information from a user since the detailed given data describing a discussed and detailed category is analyzed and new wider general insights are extracted. These general information, which has been generated changing the specific nature of a profile, should bring an improvement in the similarity coefficient.

All of these can be used as a kind of conceptual similarity.

So this pre-elaboration helps the matching algorithm but its use is recommended depending on the detail level we want for our profiles.



#### Wikipedia Languages

Everybody knows Wikipedia presents its pages with a language code and several pages are available in many languages. Thus, two pages about the same topic but in different languages are related.

Profiles contains Wikipedia's topics written not only in English but also in other languages so the similarity value given by two profiles talking about the same topic but in a different language wouldn't be included in our final result.

This can be solved using some Wikipedia APIs to retrieve the translation of every topic our users talked about, their addition to the user overview would decrease the distance between the two study subjects.

On the other hand, the same problem mentioned before would be introduced; with the addition of other pages to the user profile we are adding a lot of information to the same.
So we should ask ourselves if these changes are modifying the nature and the actual meaning of the user that we want to catch.

Is it important to recognize as different two users who talk about the same topic but with different languages or is it the same for our application?

Another problem this elaboration, as well as the others mentioned before, will introduce is that it would give to the algorithm more information that needs to be processed, thus the general complexity increases and the performances would suffer it.
