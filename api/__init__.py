""" API module """
from flask import request

import config

from api import strings
from api.auth import decode_auth_token

from .factory import create_app

app = create_app()


@app.before_request
def extra_logs():
    """ before request hook """
    if app.debug:
        # pylint:disable=no-member
        app.logger.info('Endpoint: %s', request.endpoint)
        app.logger.info('Origin: %s', request.headers.get('Origin'))


@app.before_request
def check_auth():
    """ check auth token """
    environ = request.environ
    path = str(environ['PATH_INFO'])
    token = environ.get('HTTP_AUTHORIZATION', None)

    # whitelisted non-users APIs
    if not config.ENABLE_AUTH or environ['REQUEST_METHOD'] == 'OPTIONS':
        if app.debug:
            # pylint:disable=no-member
            app.logger.debug("authentication skipped")
        return

    if any(word in path for word in config.JWT_BLACKLIST_TOKEN_CHECKS):
        if app.debug:
            # pylint:disable=no-member
            app.logger.debug("authentication skipped")
        return

    decode_auth_token(token)
