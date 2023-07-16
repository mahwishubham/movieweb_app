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
    year: int
    rating: float
    poster_url: str = ""
    imdbID: str = ""
    watched_by: Optional[List[int]] = field(default_factory=list)
