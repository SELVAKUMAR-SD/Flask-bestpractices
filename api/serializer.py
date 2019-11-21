""" Custom JSON serializer """
import json
from .encoder import JSONEncoder


def encode(value):
    """ Custom JSON encoder """
    return json.dumps(value, cls=JSONEncoder)


def decode(value):
    """ Custom JSON decoder """
    return json.loads(value)
