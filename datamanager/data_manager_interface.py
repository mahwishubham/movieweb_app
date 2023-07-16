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
        ''' Create a new User '''

    @abstractmethod
    def get_all_users(self) -> List[User]:
        ''' Get all Users '''

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        ''' Get a User by ID '''

    @abstractmethod
    def update_user(self, user_id: int, new_info: dict):
        ''' Update a User by ID '''

    @abstractmethod
    def delete_user(self, user_id: int):
        ''' Delete a User by ID '''

    @abstractmethod
    def create_movie(self, movie: Movie):
        ''' Create a new Movie '''

    @abstractmethod
    def get_movie(self, movie_id: int) -> Movie:
        ''' Get a Movie by ID '''

    @abstractmethod
    def update_movie(self, movie_id: int, new_info: dict):
        ''' Update a Movie by ID '''

    @abstractmethod
    def delete_movie(self, movie_id: int):
        ''' Delete a Movie by ID '''