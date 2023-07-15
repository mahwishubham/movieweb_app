from flask import Flask, render_template, request, redirect
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', movies=movies, user_id=user_id)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        data_manager.add_user(username)
        return redirect('/users')
    return render_template('add_user.html')

@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        data_manager.add_movie(user_id, movie_title)
        return redirect(f'/users/{user_id}')
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        updated_movie_info = request.form.to_dict()  # Assuming the form contains all the necessary movie information
        data_manager.update_movie(user_id, movie_id, updated_movie_info)
        return redirect(f'/users/{user_id}')
    movie = data_manager.get_movie(user_id, movie_id)
    return render_template('update_movie.html', movie=movie, user_id=user_id, movie_id=movie_id)

@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(f'/users/{user_id}')

if __name__ == '__main__':
    app.run(debug=True)