import json
import os
import webbrowser

import requests


api_url = 'https://dummyjson.com/products'

def use_requests(api_url, post):

    response = requests.post(api_url, post)
    json_response = json.loads(response.text)
    print(json_response)
    return
