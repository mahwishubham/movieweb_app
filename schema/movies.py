'''
Movies Datamodel
'''
from dataclasses import dataclass

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
        """
        Converts the Movie object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'director': self.director,
            'year': self.year,
            'rating': self.rating,
            'poster_url': self.poster_url,
            'imdbID': self.imdbID
        }
