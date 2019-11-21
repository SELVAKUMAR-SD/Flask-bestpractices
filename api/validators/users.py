import re

from werkzeug.exceptions import BadRequest

import config
from api import strings
from api.errors import UnauthorizedError
from api.models import User
from api.util import fetch_by_filter


def validate_credentials(user, password):
    """
    Validate email and password
    :param user: User object
    :param password: string
    """
    if not user or not User.verify_hash(password, user.password_hash):
        raise UnauthorizedError(strings.INVALID_CREDENTIAL)


def cleanup_edit_payload(payload):
    """
    Cleaning the payload for update
    :param payload: json data
    :return: json with updatable attribute
    """
    # removing password attribute if exists
    payload.pop('password', None)
    # User should not update balance in this API
    payload.pop('balance', None)

    return payload


def validate_password_terms(password):
    """
    Checking password terms
    :param password: String
    :return: Exception if error
    """
    while True:
        if len(password) < int(config.PASSWORD_LENGTH):
            raise BadRequest(strings.PASSWORD_LENGTH_ERR)
        if re.search('[0-9]', password) is None:
            raise BadRequest(strings.PASSWORD_NUMBER_ERR)
        if re.search('[A-Z]', password) is None:
            raise BadRequest(strings.PASSWORD_CAPS_ERR)
        if re.search('[a-z]', password) is None:
            raise BadRequest(strings.PASSWORD_SMALL_ERR)
        break


def validate_unique_user_by_role(phone_no, role):
    """
    Validating users phone_no with role unique together
    :param role: UserRoleEnum
    :param phone_no: String
    :return: Exception if error
    """
    if fetch_by_filter(User, dict(phone_no=str(phone_no),
                                  role=role.value)):
        raise BadRequest(strings.USER_PHONE_NUMBER_EXISTS)
