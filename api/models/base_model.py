""" `BaseModel` """
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy_utils import UUIDType

from flask_sqlalchemy_session import current_session

from api.db.base import Base


class BaseModel(Base):
    """ Base user model """
    __abstract__ = True

    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    deleted_at = Column(DateTime(timezone=True), default=None)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    @classmethod
    def query(cls):
        """ alias for `query_property()` """
        return current_session.query(cls)
