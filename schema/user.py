'''
User Datamodel
'''
from ast import List
from dataclasses import dataclass

@dataclass
class User:
    '''
        User Datamodel CLass
    '''
    id: int
    name: str
    email: str
    watched_movies: List[int]
