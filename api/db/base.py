""" base model """
from datetime import datetime

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy_session import current_session

from .commit import commit


class Base:
    """ Base class """
    __serialize_attributes__ = ()
    __updatable_attributes__ = ()

    def save(self, session=None):
        """ Save an object to the database """
        session = session if session else current_session
        session.add(self)
        commit(session)

    def serialize(self):
        """ Return a JSON-serializable version of the object """
        return {c: getattr(self, c) for c in self.__serialize_attributes__}

    def as_dict(self):
        """ Return all attributes as JSON object """
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def update(self, attributes):
        """ Update object with attributes list """
        for key, value in attributes.items():
            if key not in self.__updatable_attributes__:
                continue
            setattr(self, key, value)

    def delete(self, session=None):
        """ Delete the object from the database """
        session = session if session else current_session
        setattr(self, 'deleted_at', datetime.utcnow())
        commit(session)

    def force_delete(self, session=None):
        """ Delete the object permanently from the database """
        session = session if session else current_session
        session.delete(self)
        commit(session)


Base = declarative_base(cls=Base)  # pylint: disable=invalid-name
