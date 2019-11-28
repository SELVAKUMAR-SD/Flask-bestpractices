import random
import uuid
from random import choice

import pytest
import forgery_py
import string

from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from api import app as _app
from api.auth import get_jwt
from api.db.base import Base
from api.db.session import engine_options
from api.models import User, UserRoleEnum

TEST_PASSWORD = 'aA123456'


@pytest.fixture(scope='session')
def app():
    """Get a test app config """
    _app.config['TESTING'] = True
    _app.config['WTF_CSRF_ENABLED'] = False
    _app.config['DEBUG'] = True
    return _app


@pytest.fixture(scope='session')
def client(app, engine, tables):
    """
    Get a test client for your Flask app
    :param app: Test FlaskApp
    :param engine: sqlalchemy engine
    :param tables: creating all tables ## DON'T REMOVE FROM HERE
    :return: test client
    """
    session_factory = sessionmaker(bind=engine)
    app.db_session = flask_scoped_session(session_factory, app)
    with app.app_context():
        yield app.test_client()


@pytest.fixture(scope='session')
def engine():
    """ Get flask engine with test database """
    return create_engine(config.TEST_DB_URL, **engine_options)


@pytest.yield_fixture(scope='session')
def tables(engine):
    """ Create/Drop tables in test database """
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def session(app):
    """Get a test session for your Flask app"""
    yield app.db_session


def random_string(size=6):
    """ generates a random string of `size` """
    return ''.join(choice(string.ascii_uppercase) for i in range(size))


def header(user):
    """
    Creating header with JWT token Authorization
    :param user: User object
    :return: dict - header
    """
    return dict(Authorization=get_access_token(user))


def get_access_token(user):
    """ JWT Token for given user """
    return get_jwt(user.uuid.__str__(),
                   config.JWT_ACCESS_TOKEN_TIMEOUT_MINUTES)


@pytest.fixture
def api_version():
    yield 1


@pytest.fixture
def email():
    """ email """
    return forgery_py.internet.email_address()


@pytest.fixture
def phone_no(size=10):
    """ generates a random phone_no of `size` """
    return ''.join(["%s" % random.randint(0, 9) for num in range(0, size)])


@pytest.fixture
def name():
    """ test username """
    return forgery_py.name.full_name()


@pytest.fixture
def password():
    """ email """
    return '{}aA1'.format(random_string(5))


@pytest.fixture
def image_url():
    return "https://fakeimg.pl/350x200/?text={}" \
        .format(forgery_py.lorem_ipsum.word())


@pytest.fixture
def user(session, email, phone_no, image_url, user_role):
    """ return user if exists else create """
    _user = session.query(User) \
        .filter(User.deleted_at.is_(None)) \
        .first()
    yield _user if user else _create_user(session, email, phone_no, image_url, role=UserRoleEnum.PARENT.value)


@pytest.fixture
def admin(session, email, phone_no, image_url, user_role, password):
    """ return user if exists else create """
    _admin = session.query(User) \
        .filter(User.deleted_at.is_(None)) \
        .filter(User.role == UserRoleEnum.ADMIN.value) \
        .first()
    yield _admin if _admin else _create_admin(session, email, phone_no, image_url)


@pytest.fixture
def user_role():
    """ return random user role """
    yield random.choice(list(UserRoleEnum.__members__))


@pytest.fixture
def random_uuid():
    """ return random uuid"""
    yield uuid.uuid1()


def _create_user(session, email, phone_no, image_url):
    """ create a user """
    _user = User(email=email,
                 last_name=forgery_py.lorem_ipsum.word(),
                 phone_no=phone_no,
                 img_url=image_url,
                 first_name=forgery_py.lorem_ipsum.word(),
                 password_hash=User.generate_hash(TEST_PASSWORD),
                 role=UserRoleEnum.PARENT.value)
    _user.save(session)
    return user


def _create_admin(session, email, phone_no, image_url):
    """ create a admin user """
    _admin = User(email=email,
                  last_name=forgery_py.lorem_ipsum.word(),
                  phone_no=phone_no,
                  img_url=image_url,
                  first_name=forgery_py.lorem_ipsum.word(),
                  password_hash=User.generate_hash(TEST_PASSWORD),
                  role=UserRoleEnum.ADMIN.value)
    _admin.save(session)
    return _admin
