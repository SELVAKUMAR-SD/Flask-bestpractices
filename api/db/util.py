""" Utils """

from sqlalchemy import text, func
from sqlalchemy.sql import ClauseElement
from sqlalchemy.orm.exc import NoResultFound

from flask_sqlalchemy_session import current_session

import config
from api.errors import NotFoundError, APIError
from api.logger import get_logger

from .commit import commit

logger = get_logger(__name__)  # pylint:disable=invalid-name


def get_sort_params(sort=None, cls=None):
    """
    Getting ordering, order_by values from combined sort by string
    :param cls: String
    :param sort: String
    :return: Sting:(ordering + order_by)
    """
    order_by = sort if sort else '+created_at'
    ordering = order_by[:1]
    order_by = order_by[1:]
    ordering = ' ASC ' if ordering == '+' else ' DESC '

    if (cls and order_by == 'created_at') or cls:
        order_by = "{}.{}".format(cls.__tablename__, order_by)

    return order_by + ordering


def fetch(cls, uuid, session=None):
    """ Fetches an item from the database

    Args:
        cls (Base): Model class
        uuid (UUID|string): the uuid value of the item to fetch

    Returns:
        (cls): object of the specified class

    Raises:
        (NotFoundError)
    """
    session = session if session else current_session

    try:
        return session.query(cls).filter_by(uuid=uuid, deleted_at=None).one()
    except NoResultFound:
        raise NotFoundError('{} not found'.format(cls.__name__))


def fetch_all(cls, session=None, order_by=None):
    """ Fetches all items from the database

    Args:
        cls (Base): Model class

    Returns:
        (cls): object list of the specified class
    """
    return fetch_all_by_filter(cls, dict(), session=session, order_by=order_by)


def fetch_by_filter(cls, args, session=None):
    """
     Fetches the first filtered item from the database
    :param cls: (Base) Model class
    :param args: dict of filters
    :return: object of the specified class
    """
    session = session if session else current_session
    return session.query(cls).filter_by(**args, deleted_at=None).first()


def get_query_by_filter(cls, args, session=None, order_by=None):
    """ Get a query for a filter """
    session = session if session else current_session
    query = session.query(cls).filter_by(**args, deleted_at=None)

    if order_by:
        query = query.order_by(order_by)

    return query


def fetch_all_by_filter(cls, args, session=None, order_by=None):
    """
     Fetches all filtered items from the database
    :param cls: (Base) Model class
    :param args: dict of filters
    :return: object list of the specified class
    """
    query = get_query_by_filter(cls, args, session=session, order_by=order_by)
    return query.all()


def fetch_by_ids(cls, uuids, session=None):
    """
     Fetches all items from given id list
    :param cls: (Base) Model class
    :param uuids: list of ids
    :return: object list of the specified class
    """
    session = session if session else current_session
    return session.query(cls).filter(cls.uuid.in_(uuids),
                                     cls.deleted_at.is_(None)).all()


def add_all(objects, session=None):
    """
    Bulk insert operation
    :param objects: list of Models
    :return: Exception if error
    """
    session = session if session else current_session
    session.add_all(objects)
    commit(session)


def save_all(objects, session=None):
    """
    Bulk save operation
    :param objects: list of Models
    :return: Exception if error
    """
    session = session if session else current_session
    session.bulk_save_objects(objects)
    commit(session)


def query_select(sql, session=None):
    """
    Executing RAW SQL Query
    :param session: SQLAlchemy session
    :param sql: sql string
    :return: list of rows [JSON]
    """
    result = query_execution(sql, session)
    result = [dict(row) for row in result]
    logger.debug("Executed Query - %s", sql)
    return result


def pagination_select(sql, count_query, limit=config.DEFAULT_PAGINATION_LIMIT, page=0, sort=None):
    """
    Executing RAW SQL Query
    :param sql: sql string
    :param count_query: sql string
    :param limit: Integer
    :param page: Integer
    :param sort: Query param
    :return: list of rows [JSON]
    """
    page = int(page)
    limit = int(limit)

    sql += 'ORDER BY {}'.format(get_sort_params(sort))

    if page:
        sql += ' LIMIT {} OFFSET {} '.format(limit, (page - 1) * limit)

    result = query_execution(sql)
    result = [dict(row) for row in result]
    logger.debug("Executed Query - %s", sql)
    return result, query_count(count_query)


def query_execution(sql, session=None):
    """
    Getting list from SQL query
    :param sql: sql string
    :return: QuerySet list
    """
    session = session if session else current_session

    try:
        result = session.execute(text(sql).execution_options(autocommit=True))
        return result
    except Exception as err:
        logger.error("query_execution %s", str(err))
        raise APIError(str(err))


def query_count(sql, session=None):
    """
    Getting row count for a query
    :param sql: sql string
    :return: Integer
    """
    session = session if session else current_session
    result = session.execute(sql)
    one_row = result.fetchone()
    return one_row[0]


def get_or_create(cls, kwargs, session=None):
    """
    Common function for get or creating model
    :param cls: extended from BaseModel
    :param kwargs: dict - args
    :return: instance of given model
    """
    session = session if session else current_session

    instance = fetch_by_filter(cls, kwargs, session)
    if instance:
        return instance, False

    params = dict((k, v) for k, v in kwargs.items()
                  if not isinstance(v, ClauseElement))

    instance = cls(**params)
    instance.save(session)

    return instance, True


def paginate_query_results(query, page=None, limit=None, sort=None, cls=None):
    """
    Paginate a query result
    :param cls: String - Model name
    :param query: Query object
    :param page: int
    :param limit: int
    :param sort: str
    :return: list
    """
    if sort:
        order_by = get_sort_params(sort, cls)
        query = query.order_by(text(order_by))

    if page and limit:
        offset = (page - 1) * limit
        query = query.limit(limit).offset(offset)

    return query.all()


def search_by_filter(cls, field, value, order_by=None, limit=None):
    """ Search by filter """
    query = get_query_by_filter(cls, {}, order_by=order_by)

    if value:
        query = query.filter(
            func.lower(field)
                .contains(value.lower())
        )

    if limit:
        query = query.limit(limit)

    return query.all()
