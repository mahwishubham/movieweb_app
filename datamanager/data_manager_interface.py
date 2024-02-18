'''
Datamanager Interface
'''
from abc import ABC, abstractmethod
from typing import List
from schema.movies import Movie
from schema.user import User

class DataManagerInterface(ABC):
    """
    DataManager Interface
    """

    @abstractmethod
    def create_user(self, user: User):
        """ Create a new User """

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """ Get all Users """

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        """ Get a User by ID """

    @abstractmethod
    def update_user(self, user_id: int, new_info: dict):
        """ Update a User by ID """

    @abstractmethod
    def delete_user(self, user_id: int):
        """ Delete a User by ID """

    @abstractmethod
    def create_movie(self, movie: Movie):
        """ Create a new Movie """

    @abstractmethod
    def get_movie(self, movie: dict) -> Movie:
        """ Get a Movie by ID """

    @abstractmethod
    def update_user_movie(self, movie_id: int, user_id: int, new_info: dict):
        """ Update Users Movie from this movie list"""

    @abstractmethod
    def update_movie(self, movie_id: int, new_info: dict):
        """ Update a Movie by ID """

    @abstractmethod
    def delete_movie(self, movie_id: int):
        """ Delete a Movie by ID """

    @abstractmethod
    def delete_user_movie(self, user_id: int, movie_id: int):
        ''' Delete Movie By User Id and Movie Id'''

    @abstractmethod
    def get_user_movies(self, user_id: int):
        """ Get All Movies By User Id and Movie Id"""
