import json
import requests


def get_response(url, params=None, headers=None):
    response = requests.post(url, data=params, headers=headers)
    if response.status_code != 200:
        raise Exception('return status code is {}'.format(response.status_code))
    return json.loads(response.text)