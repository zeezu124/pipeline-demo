import json
import unittest
import requests

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:5000/results'
        self.query = 'I hate everything lol'
        self.data = {
            'input_text': self.query
            }

    def test_results(self):
        # make a post request to your Flask app
        response = requests.post(url=self.url, json=self.data)

        # Convert the response content to JSON
        json_data = response.json()

        # Make assertions on the JSON data
        
        assert isinstance(json_data, dict) #Expected JSON response to be a dictionary
        assert "output" in json_data #Expected 'output' key to be present in JSON response
        #Expected 'key' to have value specified
        assert json_data["output"] == "The text: I hate everything lol | denotes this emotion: annoyance | with a confidence score of 0.9987181425094604"
        
    def test_results_error(self):
            # make a post request to your Flask app
            data = {'input_not_text': ''}
            response = requests.post(url=self.url, json=data)

            # Convert the response content to JSON
            json_data = response.json()

            # Make assertions on the JSON data
            print(json_data)
            assert isinstance(json_data, dict) #Expected JSON response to be a dictionary
            assert "error" in json_data #Expected 'error' key to be present in JSON response
            #Expected 'key' to have value specified
            assert json_data["error"] == "Invalid request"
        


if __name__ == '__main__':
    unittest.main()