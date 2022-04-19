import os
import json
from collections import defaultdict


def get_input(input_file_name):
    assert os.path.isfile(input_file_name)
    with open(input_file_name) as json_data:
        return json.load(json_data)


