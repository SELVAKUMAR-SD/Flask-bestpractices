""" Session Manager """
# pylint: disable=invalid-name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL, DB_POOL_SIZE, DB_MAX_OVERFLOW

from api import serializer

engine_options = dict(pool_size=DB_POOL_SIZE, max_overflow=DB_MAX_OVERFLOW,
                      json_serializer=serializer.encode,
                      json_deserializer=serializer.decode)

engine = create_engine(DB_URL, **engine_options)
session_factory = sessionmaker(bind=engine)
