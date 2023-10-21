'''
Flask Movie App
'''
import os
from flask import Flask, render_template, jsonify, request
from schema import db
from dotenv import load_dotenv
from datamanager.sql_data_manager import SQLDataManager
from schema.user import User


load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspaces/movieweb_app/data/movies123.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with the Flask app
db.init_app(app)

# Pushes an application context so we can create our tables.
# This is necessary because Flask uses context-bound operations.
with app.app_context():
    db.create_all()  # Creates all tables based on the models defined.

data_manager = SQLDataManager()


# [GREEN]
@app.route('/')
def home():
    """
    This will be the home page of our application.
    We have the creative liberty to design this as a simple welcome screen or a more elaborate dashboard.
    :return: A welcome message.
    """
    return render_template('home.html')

# [GREEN]
@app.route('/users', methods=['GET'])
def get_users():
    """
    This route will present a list of all users registered in our MovieWeb App.

    :return: List of all users.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_movies(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    movies = user.watched_movies  # This already gives you a list of Movie objects
    return render_template('user_movies.html', movies=movies, user=user)

@app.route('/users/movies/search', methods=['GET', 'POST'])
def user_movies_search():
    """
    Endpoint to fetch a specific user's favorite movies.

    :body user_id: The ID of the user.
    :return: List of the user's favorite movies.
    """
    user_id = None

    if request.method == 'POST':
        user_id = request.form.get('userId') or request.json.get('userId')
    else:
        user_id = request.args.get('userId')
    
    if user_id is None:
        return render_template('user_movies_search.html', error="User ID is required")

    user_id = int(user_id)
    user = data_manager.get_user(user_id)
    if user:
        # Fetching movies directly from the user's watched_movies relationship
        movies = user.watched_movies
        return render_template('user_movies_search.html', user=user, movies=movies)

    return render_template('user_movies_search.html', error="User not found")


@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    req = request.get_json()
    movie = data_manager.get_movie(req)

    if not movie and req.get('name'):
        movie = data_manager.omdb(req.get('name'))
        if not movie:
            return jsonify({'status': f"Movie {req.get('name')} not found in OMDB list."}), 404

    user = data_manager.get_user(user_id)
    if not user:
        return jsonify({'status': f"User with user id {user_id} not found"}), 404

    if movie not in user.watched_movies:
        user.watched_movies.append(movie)
        data_manager.update_user(user_id, user.__dict__)

    return jsonify({'status': 'Movie added successfully to user favorites'})

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(user_id, movie_id):
    status = data_manager.delete_user_movie(user_id, movie_id)
    if status:
        return jsonify({'status': 'Movie deleted successfully from your favorites list.'})
    else:
        return jsonify({'status': f"Movie deletion failed. For User {user_id} and Movie {movie_id}"}), 404

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

@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    """
    Endpoint to remove a user
    :return: Status of the operation
    """
    data_manager.delete_user(user_id)
    return jsonify({'status': 'User deleted successfully'})

@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Endpoint to fetch all the movies.
    :return: List of all movies
    """

    movies = data_manager.get_all_movies()
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
    '''
    404 Error Handler
    '''
    print(event)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
