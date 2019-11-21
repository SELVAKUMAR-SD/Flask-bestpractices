""" App Factory """
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy_session import flask_scoped_session

from api.views import BLUEPRINTS
from api.error_handlers import handle_error
from api.encoder import JSONEncoder
from api.db.session import session_factory


def create_app():
    """ Create an app instance """
    app = Flask(__name__)
    app.config.from_object('config')
    app.json_encoder = JSONEncoder
    app.db_session = flask_scoped_session(session_factory, app)

    CORS(app)

    app.register_error_handler(Exception, handle_error)
    _ = list(map(app.register_blueprint, BLUEPRINTS))

    return app
