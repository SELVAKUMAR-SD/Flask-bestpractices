""" Error handlers """
from flask import current_app as app, jsonify
from sqlalchemy.orm.exc import NoResultFound


def handle_error(error):
    """ Error handler """
    app.logger.error(error)
    app.logger.debug(error, exc_info=True)

    description = ''
    if hasattr(error, 'description'):
        description = error.description

    if not description:
        description = ",\n ".join([str(x) for x in error.args])

    if isinstance(error, NoResultFound):
        status_code = 404
    elif isinstance(error, TimeoutError):
        status_code = 522
    elif hasattr(error, 'code'):
        status_code = error.code
    else:
        status_code = 400

    return jsonify(error=description,
                   error_type=error.__class__.__name__), status_code
