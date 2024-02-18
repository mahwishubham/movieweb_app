'''
Flask Movie App
'''
import uuid
from flask import Flask, jsonify, request, render_template, redirect
from datamanager.json_data_manager import JSONDataManager
from schema.movies import Movie
from schema.user import User

app = Flask(__name__)

data_manager = JSONDataManager('users.json', 'movies.json')

@app.route('/')
def home():
    """
    Home route which acts as the landing page of our MovieWeb App.

    :return: A welcome message.
    """
    return render_template('home.html')

@app.route('/users', methods=['GET'])
def get_users():
    """
    Endpoint to fetch all the users.

    :return: List of all users.
    """

    users = data_manager.get_all_users()
    # Check the request's "Accept" header
    if request.headers.get('Accept') == 'application/json':
        return jsonify(users)  # Return JSON response

    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_movies(user_id):
    """
    Endpoint to fetch a specific user's favorite movies.

    :param user_id: The ID of the user.
    :return: List of the user's favorite movies.
    """
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user(user_id)

    return render_template('user_movies.html', movies=movies, user=user)

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Endpoint to add a new user.

    :return: Status of the operation.
    """
    user_data = request.get_json()
    user_data['id'] = uuid.uuid1().int>>64
    new_user = User(**user_data)
    data_manager.create_user(new_user)
    return jsonify({'status': 'User added successfully'})

@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    """
    Endpoint to add a new movie to a user's favorite list.

    :param user_id: The ID of the user.
    :return: Status of the operation.
    """
    movie_data = request.get_json()

    # check if user is sending complete movie data.
    keys_to_check = ['id', 'name', 'director', 'year', 'rating', 'poster_url', 'imdbID']
    if all(key in movie_data for key in keys_to_check):
        movie = Movie(**movie_data)
    # Check if the user is searching for a movie with movie id or name etc.
    else:
        movie = data_manager.get_movie(movie_data)
    # if movie not in database, add the movie to database
    if not movie:
        movie = data_manager.omdb(movie_data.get('name'))
    user = data_manager.get_user(user_id)
    if not user.movies.get(movie.id):
        user.movies[movie.id] = movie.to_dict()

    data_manager.update_user(user_id, user.__dict__)
    return jsonify({'status': 'Movie added successfully to user favorites'})

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['PUT'])
def update_user_movie(user_id, movie_id):
    """
    Endpoint to update details of a specific movie in a user's list.

    :param movie_id: The ID of the movie.
    :param user_id: The ID of the user.
    :return: Status of the operation.
    """
    res = request.get_json()
    if not data_manager.get_user(user_id):
        return jsonify({'status': 'User Not Found!'})
    data_manager.update_user_movie(movie_id, user_id, res)
    return jsonify({'status': 'Movie updated successfully'})

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_user_movie(user_id, movie_id):
    """
    Endpoint to delete a specific movie from a user's favorite list.

    :param movie_id: The ID of the movie.
    :param user_id: The ID of the user
    :return: Status of the operation.
    """
    data_manager.delete_user_movie(user_id, movie_id)
    return jsonify({'status': 'Movie deleted successfully from user favorites'})

# =======================================================================
#   EXTRA FEATURES
# =======================================================================

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data_manager.delete_user(user_id)
    return jsonify({'status': 'User Deleted'})

@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Endpoint to fetch all the movies.
    :return: List of all movies
    """

    movies = data_manager.get_all_movies()
    # Check the request's "Accept" header
    if request.headers.get('Accept') == 'application/json':
        return jsonify(movies)  # Return JSON response

    return render_template('movies.html', movies=movies)

@app.route('/add_movie', methods=['POST'])
def new_movie():
    """
    Endpoint to add new movie into our database
    :return: Status of operation
    """
    movie_title = request.get_json().get('title')
    read_movie_from_omdb = data_manager.omdb(movie_title)
    if read_movie_from_omdb:
        return jsonify({'status': 'Movie Added'})
    else:
        return jsonify({'status': 'Failed to add a movie'})

@app.route('/movies/update_movie/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """
    Endpoint to update details of a specific movie in a user's list.

    :param movie_id: The ID of the movie.
    :return: Status of the operation.
    """
    res = request.get_json()
    res['id'] = movie_id
    if not data_manager.get_movie(res):
        return jsonify({'status': 'Movie Not Found!'})
    data_manager.update_movie(movie_id, res)
    return jsonify({'status': 'Movie updated successfully'})

@app.route('/movies/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """
    Endpoint to delete a specific movie from a user's favorite list.

    :param movie_id: The ID of the movie.
    :return: Status of the operation.
    """

    data_manager.delete_movie(movie_id)
    return jsonify({'status': 'Movie deleted successfully from Movie Database'})

@app.route('/movies/get_movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Endpoint to get a movie by its ID.

    :param movie_id: The ID of the movie.
    :return: The movie data in JSON format.
    """
    movie = data_manager.get_movie({'id': movie_id})
    if movie:
        movie = movie.__dict__
    else:
        movie = {}
    return jsonify(movie)


@app.errorhandler(404)
def page_not_found(event):
    """
    404 Error Handler
    """
    print(event)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
