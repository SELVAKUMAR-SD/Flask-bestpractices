""" User Blueprint """

from flask import request, jsonify
from validate_email import validate_email as is_valid_email
from werkzeug.exceptions import BadRequest

from api import strings, rest as REST
from api.auth import has_access
from api.blueprint import Blueprint
from api.helpers.user import (create_user,
                              generate_jwt)
from api.models.users import User, UserRoleEnum
from api.util import (requires_json,
                      parse_payload,
                      validate_payload_fields)
from api.validators.users import (validate_credentials,
                                  validate_password_terms,
                                  cleanup_edit_payload,
                                  validate_unique_user_by_role)

user_blueprint = Blueprint('user',  # pylint: disable=invalid-name
                           __name__, api_prefix='users')

SIGNUP_REQUIRED_FIELDS = (('email', strings.EMAIL_MISSING),
                          ('password', strings.PASSWORD_MISSING),
                          ('phone_no', strings.PHONE_NO_MISSING))


@user_blueprint.route('/signup', methods=['POST'])
@requires_json
@parse_payload(User.__payload_allowed_attributes__)
@validate_payload_fields(SIGNUP_REQUIRED_FIELDS)
def signup(payload):
    """
    Signup new user
    :return: User object
    """
    payload['email'] = payload['email'].lower().strip()
    if not is_valid_email(payload['email']):
        raise BadRequest(strings.INVALID_EMAIL)

    password = payload.pop('password')
    validate_password_terms(password)
    validate_unique_user_by_role(payload['phone_no'], UserRoleEnum.PARENT)

    user = create_user(payload, UserRoleEnum.PARENT, password)

    return jsonify(user=user), 201


@user_blueprint.route('/login', methods=['POST'])
def login():
    """
    Login existing user
    :return: Access token and Refresh token
    """
    payload = request.json
    email = payload.get('email', None)
    password = payload.get('password', None)

    user = User.find_by_email(email)
    validate_credentials(user, password)

    return jsonify({**generate_jwt(user.uuid), 'user': user})


@user_blueprint.route('/<uuid:uuid>', methods=['GET'])
def details(uuid):
    """
    User details from given uuid
    :return: User object
    """
    has_access(uuid)
    return jsonify(user=request.user)


@user_blueprint.route('/<uuid:uuid>', methods=['PUT', 'PATCH'])
def edit(uuid):
    """
    Edit User details from given payload
    :param uuid: user uuid
    :return: User object
    """
    payload = request.json
    has_access(uuid)
    payload = cleanup_edit_payload(payload)

    return REST.update(User, uuid, payload, 'user', obj=request.user)


@user_blueprint.route('/<uuid:uuid>', methods=['DELETE'])
def delete(uuid):
    """
    Soft delete User for given uuid
    :return: User object
    :param uuid: User uuid
    :return: No content response
    """
    has_access(uuid)

    return REST.delete(User, uuid, obj=request.user)
