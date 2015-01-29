import json
from os import path


def get_test_data(file_name):
    return json.load(
        open(path.join(path.dirname(__file__), 'data', file_name)))['data']
