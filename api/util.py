import datetime
from functools import wraps

from flask import request
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from api.errors import NotFoundError


def fetch(cls, uuid, session=None):
    """ Fetches an item from the database

    Args:
        cls (Base): Model class
        uuid (UUID|string): the uuid value of the item to fetch

    Returns:
        (cls): object of the specified class

    Raises:
        (NotFoundError)
    """
    session = session if session else current_session

    try:
        return session.query(cls).filter_by(uuid=uuid, deleted_at=None).one()
    except NoResultFound:
        raise NotFoundError('{} not found'.format(cls.__name__))


def fetch_all(cls, session=None, order_by=None):
    """ Fetches all items from the database

    Args:
        cls (Base): Model class

    Returns:
        (cls): object list of the specified class
    """
    return fetch_all_by_filter(cls, dict(), session=session, order_by=order_by)


def fetch_by_filter(cls, args, session=None):
    """
     Fetches the first filtered item from the database
    :param cls: (Base) Model class
    :param args: dict of filters
    :return: object of the specified class
    """
    session = session if session else current_session
    return session.query(cls).filter_by(**args, deleted_at=None).first()


def fetch_all_by_filter(cls, args, session=None, order_by=None):
    """
     Fetches all filtered items from the database
    :param cls: (Base) Model class
    :param args: dict of filters
    :return: object list of the specified class
    """
    query = get_query_by_filter(cls, args, session=session, order_by=order_by)
    return query.all()


def get_query_by_filter(cls, args, session=None, order_by=None):
    """ Get a query for a filter """
    session = session if session else current_session
    query = session.query(cls).filter_by(**args, deleted_at=None)

    if order_by:
        query = query.order_by(order_by)

    return query


def no_content_response():
    """
    Common response for delete API
    :return: HTTP response
    """
    return '', 204, {'content-type': 'application/json'}


def get_auth_exp(timeout_in_minutes):
    """
    Generating expiry timestamp
    :param timeout_in_minutes: Integer
    :return: timestamp value
    """
    _timestamp = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout_in_minutes)
    return _timestamp


def validate_fields(payload, fields):
    """ Validate existence of fields in the payload """
    for field, error_message in fields:
        if not payload.get(field):
            raise BadRequest(error_message)


def requires_json(func):
    """ requests that require a json body """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        """ raise an error if json body is empty """
        if not request.json:
            raise BadRequest('Missing json data')
        return func(*args, **kwargs)

    return decorated_function


def parse_payload(keys):
    """ parses the request payload according to the "keys" provided """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            """ raise an error if json body is empty """
            payload = request.json
            payload = dict((k, payload.get(k, None)) for k in keys)
            return func(payload, *args, **kwargs)

        return decorated_function

    return decorator


def allow_query_params(keys):
    """ parses the request query params according to the "keys" provided """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            """ raise an error if json body is empty """
            params = {key: request.args[key] for key in keys if key in request.args}
            return func(params, *args, **kwargs)

        return decorated_function

    return decorator


def validate_payload_fields(fields):
    """ Validate existence of fields in the payload """

    def decorator(func):
        @wraps(func)
        def decorated_function(payload, *args, **kwargs):
            """ raise an error payload is missing any of the fields """
            validate_fields(payload, fields)
            return func(payload, *args, **kwargs)

        return decorated_function

    return decorator
