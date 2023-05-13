import json
import requests

# Set the URL for the Flask application
url = 'http://localhost:5000/'

# Define the search query
query = 'example query'

# Define the data for the POST request
data = {'search_query': query}

# Set the headers for the POST request
headers = {'Content-type': 'application/json'}

# Send the POST request to the Flask application
response = requests.post(url=url, data=json.dumps(data), headers=headers)

# Print the response from the Flask application
print("I am todd hewitt")
print(response)
print(response.content.decode('utf-8'))
