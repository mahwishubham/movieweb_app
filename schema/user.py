from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from schema import db

# Association table for the many-to-many relationship
watched_movies_association = Table('watched_movies', db.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    
    # Define the many-to-many relationship using the association table
    watched_movies = relationship('Movie', secondary=watched_movies_association, backref='watchers')
