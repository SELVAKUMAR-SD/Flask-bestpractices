""" Serialize Class"""
from api.models import BaseModel


class Serialize:
    """ Serialize class for all serializing methods """

    @staticmethod
    def serialize_list(object_list):
        """
        Return a list of JSON-serializable version of the object
        :param object_list: Model object list
        :return: JSON
        """
        return [item.serialize() for item in object_list]

    @staticmethod
    def serialize_nested(_object):
        """
        - Serialises the model object to JSON
        - This will work only if the model is extended from BaseModel
        :param _object: Model object
        :return: JSON
        """
        result = dict()
        for item in _object:
            if isinstance(_object[item], BaseModel):
                result[item] = _object[item].serialize()
            else:
                result[item] = _object[item]
        return result
