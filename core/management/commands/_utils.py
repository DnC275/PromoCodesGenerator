import os
import base64
import json

from django.conf import settings

import core
from json.decoder import JSONDecodeError


def get_codes_file_path(file_name):
    app_path = os.path.dirname(core.__file__)
    codes_file_path = os.path.join(app_path, '..', file_name)
    return codes_file_path


def generate_code(length=8):
    token = os.urandom(length)
    return base64.b64encode(token).decode()[:-1]


def read_data(path=None):
    if not path:
        path = get_codes_file_path(settings.CODES_FILE_DEFAULT_NAME)

    try:
        with open(path, 'r') as codes_file:
            codes_data = json.load(codes_file)
            return codes_data
    except (FileNotFoundError, JSONDecodeError):
        with open(path, 'w') as codes_file:
            json.dump({}, codes_file)
        return dict()


def write_data(data, path=None):
    if not path:
        path = get_codes_file_path(settings.CODES_FILE_DEFAULT_NAME)

    with open(path, 'w') as codes_file:
        json.dump(data, codes_file, indent=2)

