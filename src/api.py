
import requests
import os
import json

API_ENDPOINT = 'http://api.translink.ca/RTTIAPI/V1/stops/'
STOP = 53656
TOP_PATH = os.path.realpath('..')
# TOP_PATH = os.path.realpath('')
CRED_PATH = TOP_PATH + '\\credentials.json'


def get_api_key():
    api_key = ''
    try:
        with open(CRED_PATH, 'r') as json_file:
            api_json = json.load(json_file)
        api_key = api_json['api_key']
    except:
        print('credentials.json not found, please enter credentials')
        api_key = input('api_key: ')

    return api_key


class transitApi:
    headers = None
    auth = None

    def __init__(self):
        self.auth = ''
        self.headers = {'Accept': 'application/json'}
        self.api_key = get_api_key()

    def get_stop_info(self):
        res = requests.get(
            API_ENDPOINT + str(STOP) + '/estimates', headers=self.headers, params={'apiKey': self.api_key})
        return res
