import jwt
from sqlalchemy.exc import SQLAlchemyError, DataError, IntegrityError

import config
from api import strings
from api.auth import get_jwt

from api.logger import get_logger

from api.errors import (DataConflictError)
from api.models import User, UserStatusEnum, UserRoleEnum

LOGGER = get_logger(__name__)  # pylint:disable=invalid-name


def _get_user_creation_error_message(error):
    error = str(error)

    if error.__contains__('unique_phone_no'):
        return strings.PHONE_EXISTS

    if error.__contains__('ix_users_email') or \
            error.__contains__('uix_email_role'):
        return strings.EMAIL_EXISTS

    return error


#
# def _send_success_signup(first_name, last_name, email):
#     name = first_name + " " + last_name
#     html = render_template('welcome_email.html',
#                            txt=_get_email_content(name))
#     response = send_mail(email, strings.SUCCESS_SIGNUP_SUBJECT,
#                          body=None, html=html)
#     if not response:
#         LOGGER.error(strings.EMAIL_SENDING_FAILED)


def create_user(payload, role, password):
    """
    Creating User object
    Applying referral code if exists
    :param payload: JSON payload
    :param role: UserRoleEnum
    :param password: string
    :return: User object
    """
    password_hash = User.generate_hash(password)

    user = User(status=UserStatusEnum.ACTIVE.value, role=role.value,
                password_hash=password_hash,
                **payload)

    try:
        user.save()
    except (DataError, IntegrityError) as err:
        raise DataConflictError(_get_user_creation_error_message(err))

    # _send_success_signup(user.first_name, user.last_name, user.email)

    return user


def generate_jwt(user_uuid):
    """
    Generating JWT access token and refresh token
    :param user_uuid: string
    :return: dict of access token and refresh token
    """
    user_uuid = str(user_uuid)

    access_token = get_jwt(user_uuid,
                           config.JWT_ACCESS_TOKEN_TIMEOUT_MINUTES)
    refresh_token = get_jwt(user_uuid,
                            config.JWT_REFRESH_TOKEN_TIMEOUT_MINUTES)

    return dict(access_token=access_token,
                refresh_token=refresh_token)
