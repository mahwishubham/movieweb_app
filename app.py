'''
Flask Movie App
'''
import uuid
from flask import Flask, jsonify, request, render_template, redirect
from datamanager.json_data_manager import JSONDataManager
# from schema.movies import Movie
from schema.user import User

app = Flask(__name__)

data_manager = JSONDataManager('users.json', 'movies.json')

@app.route('/')
def home():
    """
    Home route which acts as the landing page of our MovieWeb App.

    :return: A welcome message.
    """
    return render_template('base.html')

@app.route('/users', methods=['GET'])
def get_users():
    """
    Endpoint to fetch all the users.

    :return: List of all users.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

# @app.route('/users/<int:user_id>', methods=['GET'])
# def get_user_movies(user_id):
#     """
#     Endpoint to fetch a specific user's favorite movies.

#     :param user_id: The ID of the user.
#     :return: List of the user's favorite movies.
#     """
#     user = data_manager.get_user(user_id)
#     movies = []
#     for mov_id in user.watched_movies:
#         movies.append(data_manager.get_movie({'id': mov_id}))
#     return render_template('user_movies.html', movies=movies, user=user)

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
        movies = [data_manager.get_movie({'id': mov_id}) for mov_id in user.watched_movies]
        return render_template('user_movies_search.html', user=user, movies=movies)

    return render_template('user_movies_search.html', error="User not found")

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


@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Endpoint to fetch all the movies.
    :return: List of all movies
    """

    movies = data_manager.get_all_movies()
    return render_template('movies.html', movies=movies)


@app.route('/movies/watchers/search', methods=['GET', 'POST'])
def movie_watchers_search():
    """
    Endpoint to fetch a Users watching a specific movies.

    :body movie_id: The ID of the movie.
    :return: List of the users watching the movie.
    """
    if request.method == 'POST':
        movie_id = request.form.get('movieId')
        movie_name = request.form.get('movieName')
        imdb_id = request.form.get('imdbID')

        movie_search_params = {}

        if movie_id:
            movie_search_params['id'] = movie_id
        elif movie_name:
            movie_search_params['name'] = movie_name
        elif imdb_id:
            movie_search_params['imdbID'] = imdb_id

        movie = data_manager.get_movie(movie_search_params)

        if movie:
            users = [data_manager.get_user(user_id) for user_id in movie.watched_by]
            return render_template('movie_watchers_search.html', movie=movie, users=users)
    return render_template('movie_watchers_search.html')



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
    return jsonify({'status': 'Movie deleted successfully from user favorites'})


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
    app.run(debug=True)
