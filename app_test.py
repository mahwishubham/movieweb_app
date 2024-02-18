import requests
import json

def test_add_user():
    payload = {
        'name': 'Jason',
        'email': 'Jason@gmail.com'
    }
    r = requests.post('http://localhost:5000/add_user', json=payload)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'User added successfully'


def test_add_movie_to_user_watch_list():
    user_id = "11754101226508521966" # The actual user id needs to be used here
    payload = {
        'name': 'Spiderman'
    }
    r = requests.post(f'http://localhost:5000/users/{user_id}/add_movie', json=payload)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie added successfully to user favorites'


def test_update_movie():
    movie_id = "1472740360802865646" # The actual movie id needs to be used here
    payload = {
        'rating': 5.8
    }
    r = requests.put(f'http://localhost:5000/movies/update_movie/{movie_id}', json=payload)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie updated successfully'


def test_delete_movie():
    movie_id = "14958777144405266926" # The actual movie id needs to be used here
    r = requests.delete(f'http://localhost:5000/movies/delete_movie/{movie_id}')
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie deleted successfully from user favorites'


def test_add_movie():
    payload = {
        'title': 'The Shawshank Redemption'
    }
    r = requests.post('http://localhost:5000/add_movie', json=payload)
    assert r.status_code == 200
    assert json.loads(r.text)['status'] == 'Movie Added'


def test_list_users():
    r = requests.get('http://localhost:5000/users')
    assert r.status_code == 200


def test_list_user_watch_list():
    user_id = "3112570009830756846" # The actual user id needs to be used here
    r = requests.get(f'http://localhost:5000/users/{user_id}')
    assert r.status_code == 200


def test_home_page():
    r = requests.get('http://localhost:5000/')
    assert r.status_code == 200