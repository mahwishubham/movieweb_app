'''
User Datamodel
'''

from dataclasses import dataclass

@dataclass
class User:
    """
    User Data model Class
    """
    id: int
    name: str
    email: str
    movies: dict
