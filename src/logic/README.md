# TapoiMaps

## Introduction

TapoiMaps is a simple API developed as exercise for an interview at U-Hopper.
It allows consumers to evaluate the similarity of a user profile against a set of existing ones.
Each profile is represented through the topics discussed (According to Wikipedia's titles) togheter with the number of times each topich as been mentioned.

```json
{
    "http://en.wikipedia.org/wiki/Category:Love": 1,
    "http://en.wikipedia.org/wiki/Category:Feudalism": 3,
    "http://en.wikipedia.org/wiki/Category:Human_behaviour": 2,
    "http://en.wikipedia.org/wiki/Category:2011_singles": 21,
    "http://en.wikipedia.org/wiki/Category:Primary_historical_works": 1,
}
```

After a bit of pre-elaboration I extracted a more compact representation of the user profile removing Wikipedia URI and keeping only the category

```json
{
    "Love": 1,
    "Feudalism": 3,
    "Human_behaviour": 2,
    "2011_singles": 21,
    "Primary_historical_works": 1,
}
```

I used profiles structured like this one to evaluate the similarity.





## System architecture

I developed a Web Service over HTTP using the architecture style knew as REST.

So I implemented the system thinking at some of the  architectural constraint which have to be respected to create a RESTful API.




+ ### Uniform Interface

I followed a familiar approach similar to other APIs
The resources inside the system are accessible through a logical URI which name is releated to the content of the resource.
The resource representations as well as the requests follow the  well defined format represented by Json and certain guidlines such as naming convention.
HTTP GET requests allow the user to acces the resources but not to modify them.



+ ### Client - Server and stateless

There isn't any type of relationship between the client and the server. The server is able to evolve separately from the client which knows only the URIs of the resource and not their organization. 
Obviously the communications betweeen the 2 are all stateless. The server does not store anything about the requests the client had sent, each request is treat as a new one.
The system does not use an authentication system



+ ### Layering

I did not layered my system, so I created a single web server which serve the HTTP requests and also store all the data required from the algorithms to process and return a valid response to the client. This would absolutely be one of the focus point to improve the scalability of the system. The use of different servers for the execution of differenced tasks would help to keep good performances with a high number of profiles and users.



In conclusion, I did not follow all the constraints, which define a truly RESTful API, I  violated some of them which were not necessary because of the reduced dimensions and complexities of the system.






## Documentation

### Get ID of the most similar profile

It takes a JSON object representing a user profile and perform the evaluation of the similarity coefficient  for  every profile stored precedently.
The ID of the most similar is returned with the value of the similarity associated



<hr>

**URL: ** http://**localhost/5000**/similarity

**METHOD: ** GET

**BODY: **

A json representing an user profile

```json
{
    "Love": 1,
    "Feudalism": 3,
    "Human_behaviour": 2,
    "2011_singles": 21,
    "Primary_historical_works": 1,
}
```


**PARAMETERS: **


+ **alg**
> Tells the server which algorithm run to evaluate the similarity between the profiles
>
> default = cosine
>
> > **cosine**, is used the cosine similarity
> >
> > >The returned value represents the similarity between 2 profile, 1 means no differences
> >
> > **euclidean**, is used the (l2) normalized euclidean distance
> >
> > > The returned value represents the distance between 2 profiles, 0 means no differences
> >
> > **naive**, is used a personalized algorithm
> >
> > >The returned value represents the similarity between 2 profiles, the higher the more similar are the 2 users
> >
> > **jaccard**, is used the Weighted Jaccard similarity
> >
> > >The returned value represents the similarity between 2 profiles, 1 means no differences



**RESPONSE 200: **(application/json)

```json
{
	"ID":"Roger",
    "metric":"cosine",
    "similarity":0.897
}
```

<hr>

