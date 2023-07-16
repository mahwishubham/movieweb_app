'''
This is Json Datamanager
'''
import json
import os
from dotenv import load_dotenv
from datamanager.data_manager_interface import DataManagerInterface
from schema.movies import Movie
from schema.user import User
from api_requester import  ApiRequester

load_dotenv()  # load environment variables from .env file
API_KEY = os.getenv("API_KEY")  # read the API key from the .env file
BASE_URL = "http://www.omdbapi.com"

class JSONDataManager(DataManagerInterface):
    '''
    JSON Data Manager handles CRUD operations for both User and Movie data models.
    It interfaces with JSON files storing User and Movie data.
    '''

    def __init__(self, users_filename, movies_filename):
        '''
        Initialize JSONDataManager with filenames for user and movie data.
        
        :param user_filename: The filename of the JSON file storing user data.
        :param movie_filename: The filename of the JSON file storing movie data.
        '''
        self.users_filename = users_filename
        self.movies_filename = movies_filename
        self.users = {}
        self.movies = {}
        self.load_data()

    def load_data(self):
        '''
        Load user and movie data from JSON files.
        '''
        with open(self.users_filename, 'r', encoding='utf-8') as file:
            self.users = json.load(file)

        with open(self.movies_filename, 'r', encoding='utf-8') as file:
            self.movies = json.load(file)

    def save_data(self):
        '''
            Saving Data to Json File
        '''
        with open(self.users_filename, 'w', encoding='utf-8') as file:
            json.dump(self.users, file)
        with open(self.movies_filename, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file)

    def get_all_users(self):
        # Return all the users
        return self.users

    def get_user_movies(self, user_id):
        '''Return all the movies for a given user'''
        # Time: O (n) -> where n number of users 
        user = next((user for user in self.users if user['id'] == user_id), None)
        if user is not None:
            movie_ids = user.get("watched_movies", []) # Time: O (1)
            # Time: O (m) -> where m number of movies 
            return [movie for movie in self.movies if movie['id'] in movie_ids]

        return None
        # Total Time Complexity Is: T(max(n + m)) which is still linear

    def update_user_movie(self, user_id: int, movie_id: int, new_info: dict):
        '''
            This method is used to updated user movies list
        '''
        # Update the details of a movie for a given user
        movie = next((movie for movie in self.movies if movie['id'] == movie_id), None)
        if movie is not None and user_id in movie['watched_by']:
            print(movie, new_info)
            movie.update(new_info)
            print(movie)
            self.save_data()
            return True
        return False

    def create_user(self, user: User):
        '''
        Create a new User.

        :param user: The User object to be created.
        '''
        self.users.append(user.__dict__)
        self.save_data()

    def get_user(self, user_id: int) -> User:
        '''
        Retrieve a User by ID.

        :param user_id: The ID of the User to be retrieved.
        :return: The User object if found, None otherwise.
        '''
        user_data = next((user for user in self.users if user['id'] == user_id), None)
        return User(**user_data) if user_data else None

    def update_user(self, user_id: int, new_info: dict):
        '''
        Update a User by ID.

        :param user_id: The ID of the User to be updated.
        :param new_info: The dictionary containing new information to be updated.
        '''
        user = next((user for user in self.users if user['id'] == user_id), None)
        if user:
            user.update(new_info)
            self.save_data()

    def delete_user(self, user_id: int):
        '''
        Delete a User by ID.

        :param user_id: The ID of the User to be deleted.
        '''
        self.users = [user for user in self.users if user['id'] != user_id]
        # Find user_id in all movies and delete them
        for movie in self.movies:
            if movie['watched_by'] is not None and user_id in movie['watched_by']:
                movie['watched_by'] = [uid for uid in movie['watched_by'] if uid != user_id]

        self.save_data()

    def create_movie(self, movie: Movie):
        '''
        Create a new Movie.

        :param movie: The Movie object to be created.
        '''
        self.movies.append(movie.__dict__)
        self.save_data()

    def get_movie(self, movie: dict) -> Movie:
        '''
        Retrieve a Movie by ID.

        :param movie: search params of movie.
        :return: The Movie object if found, None otherwise.
        '''
        search, key = None, None
        key_priority = ['id', 'name', 'imdbID']
        for k in key_priority:
            if movie.get(k):
                search, key = movie[k], k
                break
        movie_data = None

        for movie in self.movies:
            if movie.get(key) == search:
                movie_data = movie
                break

        return Movie(**movie_data) if movie_data else None

    def update_movie(self, movie_id: int, new_info: dict):
        '''
        Update a Movie by ID.

        :param movie_id: The ID of the Movie to be updated.
        :param new_info: The dictionary containing new information to be updated.
        '''
        movie = next((movie for movie in self.movies if movie['id'] == movie_id), None)
        if movie:
            movie.update(new_info)
            self.save_data()

    def delete_movie(self, movie_id: int):
        '''
        Delete a Movie by ID.

        :param movie_id: The ID of the Movie to be deleted.
        '''
        self.movies = [movie for movie in self.movies if movie['id'] != movie_id]
        # Find movie_id in all users and delete them
        for user in self.users:
            if user['watched_movies'] is not None and movie_id in user['watched_movies']:
                user['watched_movies'] = [mid for mid in user['watched_movies'] if mid != movie_id]

        self.save_data()

    def omdb(self, title: str):
        '''
        Seacrh of movie on omdb and return movie data
        :param title:
        :return: movie data
        '''

        api_requester = ApiRequester(BASE_URL, API_KEY)
        for movie in self.movies:
            if movie.get('name') == title:
                print(f"Movie {title} already exists!")
                return
        movie_data = api_requester.request_movie_data(title)
        if not movie_data or movie_data.get("Response") == "False":
            print(f"Error: Movie {title} not found.")
            return
        movie = Movie(**api_requester.extract_data(movie_data))
        self.create_movie(movie)
        return movie

