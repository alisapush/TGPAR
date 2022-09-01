import json
import os
import webbrowser

import requests


api_url = 'https://dummyjson.com/products'

def use_requests(api_url):

    response = requests.get(api_url)
    json_response = json.loads(response.text)
    print(json_response)
    return
