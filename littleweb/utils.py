import json
from json.decoder import JSONDecodeError

__all__ = ['str2int', 'str2json', 'str2bool', 'STATUS_CODE_MAP', 'get_status_text']


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


STATUS_CODE_MAP = {
    # 1xx Informational
    100: 'Continue',
    101: 'Switching Protocols',

    # 2xx Success
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',

    # 3xx Redirection
    302: 'Found',

    # 4xx Client Error
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    411: 'Length Required',

    # 5xx Server Error
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    505: 'HTTP Version Not Supported',

}


def get_status_text(status_code=200, default=""):
    return STATUS_CODE_MAP.get(status_code, default)
