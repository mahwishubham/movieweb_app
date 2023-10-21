from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from schema import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    poster_url = Column(String, default="")
    imdbID = Column(String, default="")
