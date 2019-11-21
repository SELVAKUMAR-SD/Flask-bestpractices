from uuid import UUID

import jwt
from flask import request
from werkzeug.exceptions import Forbidden

import config
from api.errors import UnauthorizedError
from api import strings
from api.models import User, UserRoleEnum
from api.util import get_auth_exp, fetch_by_filter


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|error respons
    """
    if not auth_token:
        raise UnauthorizedError(strings.TOKEN_MISSING)

    try:
        payload = get_jwt_payload(auth_token)
    except jwt.InvalidTokenError as err:
        raise UnauthorizedError(str(err))

    user = fetch_by_filter(User, dict(uuid=payload['identity']))
    if not user:
        raise UnauthorizedError(strings.INVALID_CREDENTIAL)

    request.user = user
    return payload


def get_jwt_payload(token):
    """
    Creating JWT token using identity
    :param token: JWT - String
    :return: identity - dict
    """
    return jwt.decode(token,
                      config.SECRET_KEY,
                      algorithms=[config.JWT_ALGORITHM])


def get_jwt(identity, exp_time_limit):
    """
    Creating JWT token using identity
    :param exp_time_limit: int - In Minutes
    :param identity: dict
    :return: JWT - String
    """
    identity = dict(identity=identity, exp=get_auth_exp(exp_time_limit))
    return jwt.encode(identity,
                      config.SECRET_KEY,
                      config.JWT_ALGORITHM).decode("utf-8")


def has_access(field):
    """
    Validates that the user is authorized to access/edit a resource based on
    the `field` provided
    :param field: string
    :return: bool
    """
    user = request.user

    if not isinstance(field, UUID):
        field = UUID(field)

    if not user or (user.uuid != field and
                    user.role != UserRoleEnum.ADMIN.value):
        raise Forbidden(strings.FORBIDDEN)
