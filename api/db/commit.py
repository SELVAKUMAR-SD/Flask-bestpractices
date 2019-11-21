""" commit function """
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError


def commit(session):
    """ Commit the session or rollback and raise the error """
    try:
        session.commit()
    except (IntegrityError, StatementError, SQLAlchemyError) as error:
        session.rollback()
        raise error  # this should be handled in the view
