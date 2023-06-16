# Import necessary python packages
import requests

# Import config
from Config.conf import *

# Create function that connect and fetch data from Github API 
def get_github_repositories(query):

    # Define headers
    headers = {
        "Authorization": ACCESS_TOKEN
    }

    # Define parameters
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 100,
        'fork': False
    }

    # Create a request
    response = requests.get(URL, headers=headers, params=params)

    # Retrieve data in json format
    data = response.json()

    # Implementing pagination logic
    while 'next' in response.links:
        response = requests.get(response.links['next']['url'], headers=headers)
        response_data =  response.json()

        # When items doesn't exist then return the response and false
        if 'items' not in response_data:
            return {'data': False, 'request': response}
        else:
            # Extend new results to the existed data
            data['items'].extend(response_data['items'])
            
    # Return data['items'] that contains repo's informations if it exists
    return {'data': data.get('items', []), 'request': response}