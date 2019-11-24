## Documentation

### Get ID of the most similar profile

It takes a JSON object representing a user profile and perform the evaluation of the similarity coefficient  for  every profile stored previously.
The ID of the most similar is returned with the value of the similarity associated



**URL: ** /similarity

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

### Get all profiles

Return a list of all the profile's IDs memorized inside the application



**URL: ** /profiles

**METHOD: ** GET

**RESPONSE 200: **(application/json)

```json
[
  {
    "id": "emma"
  }, 
  {
    "id": "michelle"
  }, 
  {
    "id": "roger"
  }, 
  {
    "id": "tim"
  }
]
```

<hr>


### Get profile whole description

Given a profile ID returns the whole profile overview in json format.



**URL: ** /profiles/<id>


<id> must be an existing profile's ID

**METHOD: ** GET

**RESPONSE 200: **(application/json)

```json
{
	"id":'Stefano',
	"data":	{
        "Love": 1,
        "Feudalism": 3,
        "Human_behaviour": 2,
        "2011_singles": 21,
        "Primary_historical_works": 1
    }
}
```

<hr>

### Add a new profile

It takes a JSON object representing a user profile,  an argument for the profile ID and stores the new named profile in the application

**URL: ** /profiles


**METHOD: ** POST

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

+ **id**

>Tells the application the ID of the new uploaded profile
>It must be new and not already in use

**RESPONSE 200: **(application/json)

```json
{
	"message":"Profile add correctly",
	"id":'roger'
}
```

<hr>

### Remove an existing profile

It takes an argument for the profile ID and deletes that profile from the application storage

**URL: ** /profiles


**METHOD: ** DELETE


**PARAMETERS: **

+ **id**

>Tells the application the ID of the new uploaded profile
>It must exist

**RESPONSE 200: **(application/json)

```json
{
	"message":"Profile removed correctly",
	"id":'roger'
}
```

<hr>







