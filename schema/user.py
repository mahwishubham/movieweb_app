'''
User Datamodel
'''
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class User:
    '''
        User Datamodel CLass
    '''
    id: int
    name: str
    email: str
    watched_movies: Optional[List[int]] = field(default_factory=list)

