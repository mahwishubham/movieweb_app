'''
This is Json Datamanager
'''
import json
import os
from abc import ABC

from dotenv import load_dotenv
from datamanager.data_manager_interface import DataManagerInterface
from schema.movies import Movie
from schema.user import User
from api_requester import  ApiRequester

load_dotenv()  # load environment variables from .env file
API_KEY = os.getenv("API_KEY")  # read the API key from the .env file
BASE_URL = "http://www.omdbapi.com"

class JSONDataManager(DataManagerInterface, ABC):
    """
    JSON Data Manager handles CRUD operations for both User and Movie data models.
    It interfaces with JSON files storing User and Movie data.
    """

    def __init__(self, users_filename, movies_filename):
        """
        Initialize JSONDataManager with filenames for user and movie data.

        :param user_filename: The filename of the JSON file storing user data.
        :param movie_filename: The filename of the JSON file storing movie data.
        """
        self.users_filename = users_filename
        self.movies_filename = movies_filename
        self.users = {}
        self.movies = {}
        self.load_data()

    def load_data(self):
        """
        Load user and movie data from JSON files.
        """
        with open(self.users_filename, 'r', encoding='utf-8') as file:
            self.users = json.load(file)

        with open(self.movies_filename, 'r', encoding='utf-8') as file:
            self.movies = json.load(file)

    def save_data(self):
        """
            Saving Data to Json File
        """
        with open(self.users_filename, 'w', encoding='utf-8') as file:
            json.dump(self.users, file)
        with open(self.movies_filename, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file)

    def get_all_users(self):
        """
        :return: list of users in the database
        """
        return self.users

    def get_user_movies(self, user_id: int):
        """
        This function looks for user fav movies
        :param user_id:
        :return:  user fav movies
        """
        user_data = next((user for user in self.users if user['id'] == user_id), None)
        return user_data['movies']

    def create_user(self, user: User):
        """
        Create a new User.

        :param user: The User object to be created.
        """
        self.users.append(user.__dict__)
        self.save_data()

    def get_user(self, user_id: int) -> User:
        """
        Retrieve a User by ID.

        :param user_id: The ID of the User to be retrieved.
        :return: The User object if found, None otherwise.
        """
        user_data = next((user for user in self.users if user['id'] == user_id), None)
        print(user_data)
        return User(**user_data) if user_data else None

    def update_user(self, user_id: int, new_info: dict):
        """
        Update a User by ID.

        :param user_id: The ID of the User to be updated.
        :param new_info: The dictionary containing new information to be updated.
        """
        print(new_info)
        user = next((user for user in self.users if user['id'] == user_id), None)
        if user:
            user.update(new_info)
            self.save_data()

    def delete_user(self, user_id: int):
        """
        Delete a User by ID.

        :param user_id: The ID of the User to be deleted.
        """
        self.users = [user for user in self.users if user['id'] != user_id]
        self.save_data()

    def create_movie(self, movie: Movie):
        """
        Create a new Movie.

        :param movie: The Movie object to be created.
        """
        self.movies.append(movie.__dict__)
        self.save_data()

    def get_movie(self, movie: dict) -> Movie:
        """
        Retrieve a Movie by ID.

        :param movie: search params of movie.
        :return: The Movie object if found, None otherwise.
        """
        search, key = None, None
        key_priority = ['id', 'name', 'imdbID']
        for k in key_priority:
            if movie.get(k):
                search, key = movie[k], k
                break
        movie_data = None

        for mov in self.movies:
            if mov.get(key) == search:
                movie_data = mov
                break

        return Movie(**movie_data) if movie_data else None

    def get_all_movies(self):
        """
        :return all movies in the database
        """
        return self.movies

    def update_movie(self, movie_id: int, new_info: dict):
        """
        Update a Movie by ID.

        :param movie_id: The ID of the Movie to be updated.
        :param new_info: The dictionary containing new information to be updated.
        """
        movie = next((movie for movie in self.movies if movie['id'] == movie_id), None)
        if movie:
            movie.update(new_info)
            self.save_data()

    def update_user_movie(self, movie_id: int, user_id: int, new_info: dict):
        """
        Update movie details of a User
        :param movie_id:
        :param user_id:
        :param new_info:
        :return:
        """
        user_data = next((user for user in self.users if user['id'] == user_id), None)
        if user_data:
            movies = user_data.get('movies')
            movie = movies.get(str(movie_id))
            # print("\n\n\n========================================\n\n\n")
            # print(movies, movie_id, new_info)
            # print("\n\n\n========================================\n\n\n")
            if movie:
                movie.update(new_info)
                self.save_data()
        else:
            print(f"User with ID {user_id} does not exist.")

    def delete_movie(self, movie_id: int):
        """
        Delete a Movie by ID.

        :param movie_id: The ID of the Movie to be deleted.
        """
        self.movies = [movie for movie in self.movies if movie['id'] != movie_id]
        self.save_data()

    def delete_user_movie(self, user_id: int, movie_id: int):
        """
        Delete a Movie From User Watch List.
        :param user_id:
        :param movie_id: The ID of the Movie to be deleted.
        """
        user_data = next((user for user in self.users if user['id'] == user_id), None)
        if user_data:
            movies = user_data.get('movies')
            if movies.get(str(movie_id)):
                del movies[str(movie_id)]
                print(f"Movie with ID {movie_id} has been deleted.")
                self.save_data()
            else:
                print(f"Movie with ID {movie_id} does not exist in the dictionary.")

        else:
            print(f"User with ID {user_id} does not exist.")

    def omdb(self, title: str):
        """
        Seacrh of movie on omdb and return movie data
        :param title:
        :return: movie data
        """

        api_requester = ApiRequester(BASE_URL, API_KEY)
        for movie in self.movies:
            if movie.get('name') == title:
                print(f"Movie {title} already exists!")
                return None
        movie_data = api_requester.request_movie_data(title)
        if not movie_data or movie_data.get("Response") == "False":
            print(f"Error: Movie {title} not found.")
            return None
        movie = Movie(**api_requester.extract_data(movie_data))
        self.create_movie(movie)
        return movie
