import forgery_py

from tests.conftest import TEST_PASSWORD, header


def test_create_user_email_missing(client, api_version):
    """
    Test create user
    :param client: Test client
    :param api_version: Integer
    :return: 201 Ok
    """
    payload = dict(email='ghtsjj@divum.in',
                   last_name='murugan',
                   img_url='www.google.com',
                   first_name='varsha',
                   age='20',
                   password='aA123456',
                   role='PARENT')
    result = client.post('api/v{v}/users/signup'.format(v=api_version),
                         json=payload)

    assert result.status_code == 400
    assert result.json
    assert 'error_type' in result.json
    assert result.json['error_type'] == 'BadRequest'


def test_create_user(client, api_version, email, phone_no, image_url, user_role, password):
    """
    Test create user
    :param password: String
    :param user_role: String
    :param image_url: String
    :param phone_no: String
    :param email: String
    :param client: Test client
    :param api_version: Integer
    :return: 201 Ok
    """
    payload = dict(email=email,
                   last_name=forgery_py.lorem_ipsum.word(),
                   phone_no=phone_no,
                   img_url=image_url,
                   first_name=forgery_py.lorem_ipsum.word(),
                   password=TEST_PASSWORD,
                   role=user_role)
    result = client.post('api/v{v}/users/signup'.format(v=api_version),
                         json=payload)

    assert result.status_code == 201
    assert result.json
    assert 'user' in result.json


def test_login_email_missing(client, api_version, user):
    """
    Test create user
    :param user: Object
    :param client: Test client
    :param api_version: Integer
    :return: 401 UnauthorizedError
    """
    payload = dict(password=TEST_PASSWORD)
    result = client.post('api/v{v}/users/login'.format(v=api_version),
                         json=payload)
    assert result.status_code == 401
    assert result.json
    assert 'error_type' in result.json
    assert result.json['error_type'] == 'UnauthorizedError'


def test_login(client, api_version, user):
    """
    Test create user
    :param user: Object
    :param client: Test client
    :param api_version: Integer
    :return: 200 ok
    """
    payload = dict(email=user.email,
                   password=TEST_PASSWORD)
    result = client.post('api/v{v}/users/login'.format(v=api_version),
                         json=payload)

    assert result.status_code
    assert result.json
    assert 'access_token' in result.json
    assert 'refresh_token' in result.json
    assert 'user' in result.json


def test_user_details_token_missing(client, api_version, user):
    """
    Test User Details
    :param client: Test client
    :param api_version: Integer
    :param user: Object
    :return: 401 UnauthorizedError
    """
    result = client.get('api/v{v}/users/{uuid}'.format(v=api_version,
                                                       uuid=user.uuid))
    assert result.status_code
    assert result.json
    assert 'error_type' in result.json
    assert result.json['error_type'] == 'UnauthorizedError'


def test_user_details(client, api_version, user):
    """
    Test User Details
    :param client: Test client
    :param api_version: Integer
    :param user: Object
    :return: 200 ok
    """
    result = client.get('api/v{v}/users/{uuid}'.format(v=api_version,
                                                       uuid=user.uuid),
                        headers=header(user))

    assert result.status_code == 200
    assert result.json
    assert 'user' in result.json
