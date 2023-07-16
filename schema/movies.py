'''
Movies Datamodel
'''
from ast import List
from dataclasses import dataclass

@dataclass
class Movie:
    '''
    Movies Datamodel Class
    '''
    id: int
    name: str
    director: str
    year: int
    rating: float
    watched_by: List[int]
