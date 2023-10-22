from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from schema import db

class Director(db.Model):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(String)  # Consider using DateTime instead if you have exact date/time info
