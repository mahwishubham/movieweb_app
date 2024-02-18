'''
User Datamodel
'''

from dataclasses import dataclass, field

@dataclass
class User:
    '''
        User Datamodel CLass
    '''
    id: int
    name: str
    email: str
    movies: dict