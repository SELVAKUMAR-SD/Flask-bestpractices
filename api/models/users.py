""" `User` model """
import enum

from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import (Column, String, Integer, ForeignKey, Float,
                        UniqueConstraint,
                        func)
from flask_sqlalchemy_session import current_session
import bcrypt

from .base_model import BaseModel


class UserRoleEnum(enum.Enum):
    """ Class to define user roles """

    ADMIN = 'ADMIN'
    CHILD = 'CHILD'
    PARENT = 'PARENT'
    VENDOR = 'VENDOR'
    FACULTY = 'FACULTY'


class UserStatusEnum(enum.Enum):
    """ Class to define user status """

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class User(BaseModel):
    """ User model """

    __tablename__ = 'users'

    __serialize_attributes__ = (
        'uuid', 'first_name', 'last_name', 'phone_no', 'email', 'age', 'role',
        'img_url', 'status')

    __updatable_attributes__ = (
        'first_name', 'last_name', 'phone_no', 'age', 'img_url',
        'status', 'password_hash', 'temporary_password')

    __payload_allowed_attributes__ = (
        'email', 'password', 'phone_no', 'first_name', 'last_name', 'age',
        'img_url')

    __table_args__ = (UniqueConstraint('email', 'role',
                                       name='uix_email_role'),)

    email = Column(String(256), index=True, nullable=True)
    phone_no = Column(String(12), nullable=False, index=True)
    password_hash = Column(String(256))
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    img_url = Column(String, nullable=True)
    role = Column(String(20), nullable=False)
    status = Column(String(20), nullable=True)

    @hybrid_property
    def name(self):
        """ combined name """
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def currency(self):
        """
        Getting currency from User object
        :return: currency_code - String
        """
        return self.find_currency()

    @staticmethod
    def generate_hash(password):
        """
        Getting hash of password
        :param password: string password
        :return: string hash
        """
        return bcrypt.hashpw(password.encode('utf-8'),
                             bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_hash(password, _hash):
        """
        Matching hash and password
        :param password: string
        :param _hash: string
        :return: Boolean
        """
        return bcrypt.checkpw(password.encode('utf-8'), _hash.encode('utf-8'))

    @classmethod
    def find_by_email(cls, email, role=UserRoleEnum.PARENT, session=None):
        """
        Get parent object by email
        :param role: UserRoleEnum
        :param email: string
        :return: User object
        """
        session = session if session else current_session
        return session.query(cls) \
            .filter(func.lower(User.email) == func.lower(email),
                    User.role == role.value).first()
