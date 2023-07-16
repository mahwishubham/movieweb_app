'''
Flask Movie App
'''

from flask import Flask, jsonify, request
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
    return "Welcome to MovieWeb App!"

@app.route('/users', methods=['GET'])
def get_users():
    """
    Endpoint to fetch all the users.

    :return: List of all users.
    """
    users = data_manager.get_all_users()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_movies(user_id):
    """
    Endpoint to fetch a specific user's favorite movies.

    :param user_id: The ID of the user.
    :return: List of the user's favorite movies.
    """
    user = data_manager.get_user(user_id)
    return jsonify(user.watched_movies)

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Endpoint to add a new user.

    :return: Status of the operation.
    """
    user_data = request.get_json()
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
    new_movie = Movie(**movie_data)
    data_manager.create_movie(new_movie)
    user = data_manager.get_user(user_id)
    user.watched_movies.append(new_movie.id)
    data_manager.update_user(user_id, user.__dict__)
    return jsonify({'status': 'Movie added successfully to user favorites'})

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['PUT'])
def update_movie(user_id, movie_id):
    """
    Endpoint to update details of a specific movie in a user's list.

    :param user_id: The ID of the user.
    :param movie_id: The ID of the movie.
    :return: Status of the operation.
    """
    movie_data = request.get_json()
    data_manager.update_user_movie(user_id, movie_id, movie_data)
    return jsonify({'status': 'Movie updated successfully'})

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(user_id, movie_id):
    """
    Endpoint to delete a specific movie from a user's favorite list.

    :param user_id: The ID of the user.
    :param movie_id: The ID of the movie.
    :return: Status of the operation.
    """
    data_manager.delete_movie(movie_id)
    user = data_manager.get_user(user_id)
    user.watched_movies.remove(movie_id)
    data_manager.update_user(user_id, user.__dict__)
    return jsonify({'status': 'Movie deleted successfully from user favorites'})

if __name__ == '__main__':
    app.run(debug=True)
