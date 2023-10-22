from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from schema import db

# # Association table for the many-to-many relationship between movies and genres
# movies_genres_association = Table('movies_genres', db.metadata,
#     Column('movie_id', Integer, ForeignKey('movies.id')),
#     Column('genre_id', Integer, ForeignKey('genres.id'))
# )

class Genre(db.Model):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)
