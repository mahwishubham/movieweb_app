from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schema.movies import Movie
from schema.user import User
from schema.review import Review
from schema.director import Director
from schema.genre import Genre
from api_requester import ApiRequester
import os

BASE_URL = "http://www.omdbapi.com"
API_KEY = os.getenv("API_KEY")

class SQLDataManager:
    def __init__(self):
        # Use the already defined engine from the Flask configuration
        from schema import db
        self.session = db.session

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_movies(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.watched_movies if user else None

    def delete_user_movie(self, user_id: int, movie_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            movie = self.session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                user.watched_movies.remove(movie)
                self.session.commit()
                return True
        return False

    def create_user(self, user: User):
        self.session.add(user)
        self.session.commit()

    def get_user(self, user_id: int):
        return self.session.query(User).filter_by(id=user_id).first()

    def update_user(self, user_id: int, new_info: dict):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in new_info.items():
                setattr(user, key, value)
            self.session.commit()

    def delete_user(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def create_movie(self, movie: Movie):
        self.session.add(movie)
        self.session.commit()

    def get_movie(self, movie: dict):
        search_params = ['id', 'name', 'imdbID']
        for key in search_params:
            if movie.get(key):
                return self.session.query(Movie).filter_by(**{key: movie[key]}).first()

    def get_all_movies(self):
        return self.session.query(Movie).all()

    def update_movie(self, movie_id: int, new_info: dict):
        movie = self.session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            for key, value in new_info.items():
                setattr(movie, key, value)
            self.session.commit()

    def omdb(self, title: str):
        api_requester = ApiRequester(BASE_URL, API_KEY)
        existing_movie = self.session.query(Movie).filter_by(name=title).first()
        if existing_movie:
            print(f"Movie {title} already exists!")
            return
        movie_data = api_requester.request_movie_data(title)
        if not movie_data or movie_data.get("Response") == "False":
            print(f"Error: Movie {title} not found.")
            return
        movie = Movie(**api_requester.extract_data(movie_data))
        self.create_movie(movie)
        return movie

    def create_review(self, review: Review):
        self.session.add(review)
        self.session.commit()
    

    def create_director(self, director: Director):
        self.session.add(director)
        self.session.commit()

    def get_director(self, director_id: int):
        return self.session.query(Director).filter_by(id=director_id).first()

    def create_genre(self, genre: Genre):
        self.session.add(genre)
        self.session.commit()

    def get_genre(self, genre_id: int):
        return self.session.query(Genre).filter_by(id=genre_id).first()