'''
This module is used to make api request to OMDB.
'''

from abc import ABC, abstractmethod
import requests
import uuid

class IApiRequester(ABC):
    """
    Abstract base class representing an API requester.

    """

    @abstractmethod
    def request_movie_data(self, title):
        """
        Abstract method to request movie data from the API.

        Args:
            title (str): The title of the movie.

        Returns:
            dict: The movie data retrieved from the API.

        """


class ApiRequester(IApiRequester):
    """
    Class representing an API requester implementation.

    Args:
        base_url (str): The base URL of the API.
        api_key (str): The API key to access the API.

    Attributes:
        _base_url (str): The base URL of the API.
        _api_key (str): The API key to access the API.

    """

    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key

    def request_movie_data(self, title):
        """
        Request movie data from the API.

        Args:
            title (str): The title of the movie.

        Returns:
            dict: The movie data retrieved from the API.

        """
        response = requests.get(f"{self._base_url}/?t={title}&apikey={self._api_key}")
        if response.status_code != 200:
            print("Error: API is not accessible.")
            return None

        movie_data = response.json()
        if movie_data.get("Response") == "False":
            print(f"Error: Movie {title} not found.")
            return None

        return movie_data

    def extract_data(self, movie_data):
        """
        Extracts relevant movie information from the data received from the API.

        Args:
            movie_data (dict): The movie data retrieved from the API.

        Returns:
            dict: The extracted movie information.

        """
        return {
            "id": uuid.uuid1().int >> 64,
            "name": movie_data.get("Title"),
            "year": movie_data.get("Year") or 0,
            "rating": float(movie_data["imdbRating"]) if movie_data.get("imdbRating", "N/A") != "N/A" else 0.0,
            "poster_url": movie_data.get("Poster") if movie_data.get("Poster") != "N/A" else "",
            "imdbID": movie_data.get("imdbID") or "",
            "director": movie_data.get("Director") or "",
        }