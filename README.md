# API

### 1. @app.route('/users', methods=['GET'])
This route is used to get the list of users in our database

### 2.@app.route('/users/<int:user_id>', methods=['GET'])
This route is used to get information about a particular user in the database

### 3.@app.route('/add_user', methods=['POST'])
This route is used to add a new user into the database.
Initially this user is not watching any movies.

### 4.@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
This route is used to add a movie to users watched list

### 5.@app.route('/users/update_movie/<int:movie_id>', methods=['PUT'])
This route is used to update the movie in the database

### 6.@app.route('/users/delete_movie/<int:movie_id>', methods=['DELETE'])
This route is used to delete a movie in the database. If a movie is deleted, it will also get
removed from the database of users who have watched this movie.

### 3.@app.route('/add_movie', methods=['POST'])
This route is used to add a new movie in the database. We will be using the title of the movie that we want to add.