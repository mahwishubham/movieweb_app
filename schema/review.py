from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from schema import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    review_text = Column(String)
    rating = Column(Float)

    user = relationship("User", backref="reviews")
    movie = relationship("Movie", backref="reviews")
