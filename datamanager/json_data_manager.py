'''
This is Json Datamanager
'''
import json
from datamanager.data_manager_interface import DataManagerInterface
from schema.movies import Movie
from schema.user import User

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
            movie.update(new_info)
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
        self.save_data()

    def create_movie(self, movie: Movie):
        '''
        Create a new Movie.

        :param movie: The Movie object to be created.
        '''
        self.movies.append(movie.__dict__)
        self.save_data()

    def get_movie(self, movie_id: int) -> Movie:
        '''
        Retrieve a Movie by ID.

        :param movie_id: The ID of the Movie to be retrieved.
        :return: The Movie object if found, None otherwise.
        '''
        movie_data = next((movie for movie in self.movies if movie['id'] == movie_id), None)
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
        self.save_data()

