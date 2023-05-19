import json
import unittest
import requests

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:5000'
        self.query = 'example query'
        self.data = {
            'search_query': self.query
            }

    def test_search(self):
        # make a post request to your Flask app
        data = self.data
        response = requests.post(url=self.url, data=json.dumps(data))

        # Print the response from the Flask application
        print(response.content.decode('utf-8'))

        # assert that the response is of type object
        self.assertIsInstance(response, object)

if __name__ == '__main__':
    unittest.main()