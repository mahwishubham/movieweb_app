import unittest
from app import app, data_manager
from flask import json

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True

    def test_users_route(self):
        response = self.client.get('/users')
        data = json.loads(response.get_data())
        expected_data = data_manager.list_all_users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()