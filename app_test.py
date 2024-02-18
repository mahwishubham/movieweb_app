import requests
import json

# Common variables
BASE_URL = 'http://localhost:5000'
USERNAME = 'Jason2'
EMAIL = 'Jason2@gmail.com'
MOVIE_NAME = 'Inception'
headers = {
    'Accept': 'application/json'
}

def test_add_user():
    payload = {
        'name': USERNAME,
        'email': EMAIL,
        'movies': {}
    }
    r = requests.post(f'{BASE_URL}/add_user', json=payload)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'User added successfully'

def test_add_movie_to_user_watch_list():
    payload = {
        'name': MOVIE_NAME
    }
    users = requests.get(f'{BASE_URL}/users', headers=headers)
    data = users.json()
    user = data[-1]
    r = requests.post(f"{BASE_URL}/users/{user.get('id')}/add_movie", json=payload)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie added successfully to user favorites'

def test_new_movie():
    payload = {
        'title': MOVIE_NAME
    }
    # Sending POST request to add_movie endpoint
    r = requests.post(f'{BASE_URL}/add_movie', json=payload)

    # Asserting the HTTP status code
    assert r.status_code == 200, f"Expected status code 200, got {r.status_code}"

    # Parsing the response and asserting the operation status
    response_data = json.loads(r.text)
    assert 'status' in response_data, "Response does not contain status field"


def test_update_movie():
    payload = {
        'rating': 5.8
    }
    users = requests.get(f'{BASE_URL}/users', headers=headers)
    data = users.json()
    user = data[-1]

    movies = requests.get(f'{BASE_URL}/movies', headers=headers)
    data = movies.json()
    movie = data[-1]
    r = requests.put(f"{BASE_URL}/users/{user.get('id')}/update_movie/{movie.get('id')}", json=payload)
    print(r.text)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie updated successfully'



def test_delete_movie():
    users = requests.get(f'{BASE_URL}/users', headers=headers)
    data = users.json()
    user = data[-1]

    movies = requests.get(f'{BASE_URL}/movies', headers=headers)
    data = movies.json()
    movie = data[-1]
    r = requests.delete(f"{BASE_URL}/users/{user.get('id')}/delete_movie/{movie.get('id')}")
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie deleted successfully from user favorites'

def test_delete_user():
    users = requests.get(f'{BASE_URL}/users', headers=headers)
    data = users.json()
    user = data[-1]
    r = requests.delete(f"{BASE_URL}/users/{user.get('id')}")

    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'User Deleted'


def test_list_users():
    r = requests.get(f'{BASE_URL}/users')
    assert r.status_code == 200

def test_home_page():
    r = requests.get(f'{BASE_URL}/')
    assert r.status_code == 200
