from __future__ import absolute_import
import requests

def get_page(url):
    print(url)
    response = requests.get(url)
    return response.text
