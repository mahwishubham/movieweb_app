'''
Flask Movie App
'''

from flask import Flask, jsonify, request, render_template, redirect
from datamanager.json_data_manager import JSONDataManager
from schema.movies import Movie
from schema.user import User
import uuid

app = Flask(__name__)

data_manager = JSONDataManager('users.json', 'movies.json')

@app.route('/')
def home():
    """
    Home route which acts as the landing page of our MovieWeb App.

    :return: A welcome message.
    """
    return "<h1>Welcome to MovieWeb App!</h1>"

@app.route('/users', methods=['GET'])
def get_users():
    """
    Endpoint to fetch all the users.

    :return: List of all users.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_movies(user_id):
    """
    Endpoint to fetch a specific user's favorite movies.

    :param user_id: The ID of the user.
    :return: List of the user's favorite movies.
    """
    user = data_manager.get_user(user_id)
    movies = []
    for mov_id in user.watched_movies:
        movies.append(data_manager.get_movie({'id': mov_id}))
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



@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    """
    Endpoint to add a new movie to a user's favorite list.

    :param user_id: The ID of the user.
    :return: Status of the operation.
    """
    movie_data = request.get_json()
    movie = data_manager.get_movie(movie_data)
    if not movie:
        movie = data_manager.omdb(movie_data.get('name'))
    user = data_manager.get_user(user_id)
    if movie.id not in user.watched_movies:
        user.watched_movies.append(movie.id)
    movie.watched_by.append(user.id)
    data_manager.update_user(user_id, user.__dict__)
    data_manager.update_movie(movie.id, movie.__dict__)
    return jsonify({'status': 'Movie added successfully to user favorites'})

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
    return jsonify({'status': 'Movie deleted successfully from user favorites'})

if __name__ == '__main__':
    app.run(debug=True)
