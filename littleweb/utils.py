import json
from json.decoder import JSONDecodeError


def str2int(value, default=None):
    try:
        return int(value)
    except ValueError as e:
        print(e)
        return default


def str2json(value, default=None):
    try:
        return json.loads(value)
    except JSONDecodeError as e:
        print(e)
        return default
    except ValueError as e:
        print(e)
        return default


def str2bool(value, default=False):
    if value:
        return value is True or value == 'true' or value == 'True'
    else:
        return default
