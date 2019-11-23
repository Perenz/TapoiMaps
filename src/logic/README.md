# TapoiMaps

## Introduction

TapoiMaps is a simple API developed as exercise for an interview at U-Hopper.
It allows consumers to evaluate the similarity of a user profile against a set of existing ones.
Each profile is represented through the topics discussed (According to Wikipedia's titles) together with the number of times each topic as been mentioned.

```json
{
    "http://en.wikipedia.org/wiki/Category:Love": 1,
    "http://en.wikipedia.org/wiki/Category:Feudalism": 3,
    "http://en.wikipedia.org/wiki/Category:Human_behaviour": 2,
    "http://en.wikipedia.org/wiki/Category:2011_singles": 21,
    "http://en.wikipedia.org/wiki/Category:Primary_historical_works": 1,
}
```

After a bit of pre-elaboration I extracted a more compact representation of the user profile removing Wikipedia URI and keeping only the category name.

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

I followed a familiar approach similar to other APIs.
The resources inside the system are accessible through a logical URI which name is related to the content of the resource.
The resource representations as well as the requests follow the  well defined format represented by Json and certain guidelines such as naming convention.
HTTP GET requests allow the user to access the resources but not to modify them. 
Resource adding operations can be performed through POST Requests and can be removed using DELETED Requests. 



+ ### Client - Server and stateless

There isn't any type of relationship between the client and the server. The server is able to evolve separately from the client which knows only the URIs of the resource and not their organization. 
Obviously the communications between the 2 are completely stateless. The server does not store anything about the requests the client had sent, each request is treat as a new one.
The application does not use an authentication system.



+ ### Layering

I did not layered my system, so I created a single web server which serve all the HTTP requests and also store all the data required from the algorithms to process and return a valid response to the client. This would absolutely be one of the focus point to improve the scalability of the system. The use of different servers, each used to perform specific field-related operation, for the execution of differenced tasks would help to keep good performances with a high number of profiles and users.





In conclusion, I did not follow all the constraints, which define a truly RESTful API, I  violated some of them which were not necessary because of the reduced dimensions and complexities of the system.



### Storage

I did not use any type of database to store the profiles and I saved them locally on the Web Server with a Json format. So with an higher number of observation for each profile and an increasing amount of users the process would become slower. Since the reduced complexity of the system my idea was that of storing the files locally without using an external storage support. Because of that I started looking for something faster and scalable.
This decision also implies the necessity of restarting the web service after the addition/delete of a file json representing an user profile if these operation are done manually and not using the available API.

I looked for some pandas compatible format alternatives to Json that would speed up the operations. This would have allowed me to speed up the initialization of the web server which compute the uploading of all the user profiles in different dataframes and would allow me to switch the storage system architecture in a way which performs the reading of the profiles only when it is required. This will decrease the amount of memory used by the application because profiles are not permanently loaded as dataframes but on the other hand the number of reading operation from the files representing the users rises because we have to load all the dataframes at every requests to evaluate the similarity.

Because of this I looked for an alternative format that would help my application to scale, being faster and lighter. 

According to [this article](https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d) I find many interesting facts.

Some format had been valuated under 5 metrics which include file size, save time (save dataframe onto a disk) and load time (load dumped dataframe into memory) . What matters more for our application is the load_time since it's the time required from the operation of reading the stored file uploading it as dataframe while saving operations (PUT /profiles) are quite rare.
The mentioned study shows some well-known information, like the slowness of a CSV file, but also some others that could help us take a decision such as, for example, the impressive results in term of load time for parquet and feather.
We can notice how feather and parquet have great values for the memory consumption during the operation of saving and loading. Parquet also shows impressive results in term of file size.

Changing approach and treating the data as Pandas Categorical does return different insights. Binary formats reach fantastic scores with parquet being the slower in term of save operations but in the average for load time. Talking about file size parquet and feather obtain more or less the same results but parquet shows noticeable overhead in memory consumption during the operation of loading since it requires an extra amount of resources to un-compress the data back into a dataframe.

To sum up, even though feather shows better general results I think that for our system the best choice is the parquet format. Indeed feather is not expected to be used as a long-term file storage while parquet is. 
In addition, parquet is supported by many different systems that perform analytics such as Spark and AWS Services which would help our application scaling.



## Scalability

I already mentioned a bunch of choices or possible improvements that could help against the huge scalability challenge; for instance the use of third parties libraries like scikit, the introduction of a lighter format or the layering of the system architecture would all promote the application scalability. Anyway, now I'm going to talk about actual solutions that allow out web service to keep good performances with an higher number of user, requests and, therefore, traffic.



### Load sharing through redirection

A distributed architecture (as mentioned before) consisting of independent servers sharing the load is a fundamental key for implementing a web server. Most suggest using some form of Weighted Round-Robin implemented using the DNS server, this approach requires each server to handle requests for all the data stored; a problem that can be solved in two different ways: a first one which requires that each server must store its own copy of all the data or a second alternative  implying to access the data from other HTTP servers (doing requests) or some database servers (doing requests), both generate significant back-end traffic which requires additional resources to be processed not allowing the application to scale properly.
Thus, a  "redirection-based" hierarchical architecture is often preferred since it eliminates bottlenecks in the server and allows the introduction of new hardware to handle increases in load. Here, two levels of server are used, each storing partitioned data according to their content. There are redirection servers used to distribute the users requests to the corresponding normal HTTP servers which respond to client's requests.
This kind of approach results completely transparent to the user and achieves better caching efficiency compared with other load balancing schemes guaranteeing a great scaling.  



### Horizontal scalability

Thinking about our specific application should be said that we are facing a structure that fits well for horizontal scalability. The addition of more machines would give us the opportunity to distribute the data over multiple servers. Thus each of these servers would perform the similarity coefficient evaluation over a restricted set of the target profiles. Then the results obtained from each machine can be merged together to extract global insights.
So every server becomes faster and the performance raise.
In addition, while horizontal scaling is less suitable for Relational DB as it relies on consistency and atomicity, NoSQL databases take advantages of horizontal scalability since they follow the de-normalization concept so duplicates can be stored. Our application doesn't involve neither strict atomic transactions or elevate number of joints so horizontal scaling used together with NoSQL DB would boost the productivity





### Storage support

As mentioned before the efficiency may raise using a database to store our files representing the profiles. Although we can observe a kind of relational structure in our data, since Wiki categories could be seen as a big table containing thousands of rows which are related to user profiles, I don't think this solution would guarantee the best performances.
I would rather use systems designed for document store which compose one of the main categories of NoSQL databases. These types of database fits perfect with our necessity of storing semi structured data encoded in standard format such as Json.
I will focus on two of the most famous DBMS from the mentioned class: MongoDB and CouchDB. The two differs in several aspects, starting from the DB structure. CouchDB stores JSON format offering CRUD operations above them, MongoDB use a less strict structure allowing schema-free data storing in a binary format, so documents are not required to have a predefined structure so different documents in the collection can have different columns; a feature that fits perfectly for our system. While CouchDB achieves scalability through master-slave replication (The master perform the writes and then passes the updated information to the slaves which can perform read anytime) MongoDB does it horizontally supporting automatic sharding, distributing documents over servers and uses replication just for failover.
MongoDB provides faster read speeds and it is the better choice for a rapidly growing database that could be our case because of the profiles' size so i would recommend it more than CouchDB.

A third alternative would be that of adopting a graph database storing each profile and each category as a single node; references from an user for a specific topic could be represented using weighted edges. Scalability is usually great for these types of graphs and they are much more adequate to handle changing data with evolutionary pattern. On the contrary Relational and NoSQL DBMS are typically faster in performing the same operations on a large number of data.


