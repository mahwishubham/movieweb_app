'''
Movies Datamodel
'''
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Movie:
    '''
    Movies Datamodel Class
    '''
    id: int
    name: str
    director: str
    year: str
    rating: float
    poster_url: str = ""
    imdbID: str = ""

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'director': self.director,
            'year': self.year,
            'rating': self.rating,
            'poster_url': self.poster_url,
            'imdbID': self.imdbID
        }