Our current JSON structure does not efficiently support searching movies watched by a user due to its nested nature. An optimal approach for this would be to de-normalize the data structure.

In this new structure, you will have two main collections: one for users and one for movies. Each movie will have an attribute that contains a list of user_ids representing users who have watched the movie. This way, you can directly find all the users who watched a certain movie. For users, you can have a list of watched movie_ids.

Here's an example of the proposed structure:

**Users**
```
[
  {
    "id": 1,
    "name": "Alice",
    "watched_movies": [1, 2]
  },
  {
    "id": 2,
    "name": "Bob",
    "watched_movies": []
  }
]
```

**Movies**
```
[
  {
    "id": 1,
    "name": "Inception",
    "director": "Christopher Nolan",
    "year": 2010,
    "rating": 8.8
  },
  {
    "id": 2,
    "name": "The Dark Knight",
    "director": "Christopher Nolan",
    "year": 2008,
    "rating": 9.0
  }
]
```

This design allows you to efficiently find the movies watched by a user and users who watched a specific movie. It is also beneficial when you migrate to MongoDB because MongoDB supports efficient querying of such data structures.

Please note that this structure does have redundancy - both the User document and the Movie document need to be updated when a User watches a Movie. This is a `trade-off` you often have to make in NoSQL databases to increase the efficiency of reads at the cost of making writes slightly more complex.