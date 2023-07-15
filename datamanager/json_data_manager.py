class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.load_data()

    def load_data(self):
        with open(self.filename, 'r') as f:
            self.data = json.load(f)

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def get_all_users(self):
        # Return all the users
        return self.data

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        user = self.data.get(str(user_id), None)
        if user is not None:
            return user.get("movies", None)
        else:
            return None

    def update_user_movie(self, user_id, movie_id, new_info):
        # Update the details of a movie for a given user
        user = self.data.get(str(user_id), None)
        if user is not None:
            movies = user.get("movies", None)
            if movies is not None and str(movie_id) in movies:
                movies[str(movie_id)].update(new_info)
                self.save_data()
                return True
        return False