""" REST Operations """
from datetime import datetime

from flask import jsonify
from flask_sqlalchemy_session import current_session as session

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from api import strings
from api.db.util import fetch, fetch_all, fetch_all_by_filter, save_all
from api.util import no_content_response
from api.logger import get_logger

logger = get_logger(__name__)  # pylint:disable=invalid-name


def _serialize(json_key, obj, status_code=200):
    return jsonify(**{json_key: obj}), status_code


def create(cls, payload, json_key):
    """ Create a new resource """
    obj = cls(**payload)
    obj.save()
    return _serialize(json_key, obj, 201)


def create_multiple(cls, payload, json_key=None, validation_func=None):
    """ Create multiple instances of `cls` """
    json_key = json_key if json_key else 'result'

    objs = []
    if validation_func:
        for item in payload:
            validation_func(**item)
            objs.append(cls(**item))
    else:
        objs = [cls(**item) for item in payload]

    try:
        save_all(objs)
    except IntegrityError as err:
        logger.error('Error: %s', err)
        return jsonify(**{json_key: False, 'error': 'Integrity Error'})

    return jsonify(**{json_key: True}), 201


def update(cls, uuid, payload, json_key, obj=None):
    """ Update a resource """
    if not obj:
        obj = fetch(cls, uuid)

    obj.update(payload)
    obj.save()

    return _serialize(json_key, obj)


def get(cls, uuid, json_key):
    """ Fetch a resource """
    return _serialize(json_key, fetch(cls, uuid))


def delete(cls, uuid, obj=None):
    """ Delete a resource """
    if not obj:
        obj = fetch(cls, uuid)

    obj.delete()
    return no_content_response()


def delete_bulk(cls, uuids):
    """ Delete multiple resources """

    query = session.query(cls) \
        .filter(cls.uuid.in_(uuids), cls.deleted_at.is_(None))

    if query.count() != len(uuids):
        raise BadRequest(strings.INVALID_UUID_LIST.format(cls.__tablename__))

    query.update({cls.deleted_at: datetime.utcnow()},
                 synchronize_session=False)
    session.commit()

    return no_content_response()


def get_list(cls, json_key, order_by=None):
    """ get a list of objects """
    return _serialize(json_key, fetch_all(cls, order_by=order_by))


def get_list_by_filter(cls, filter_params, json_key, order_by=None):
    """ get a list of objects by filter"""
    return _serialize(json_key, fetch_all_by_filter(cls, filter_params,
                                                    order_by=order_by))
