""" JSON encoder """
import datetime
import enum
from decimal import Decimal
from flask.json import JSONEncoder as FlaskJSONEncoder


class JSONEncoder(FlaskJSONEncoder):
    """ Custom JSON encoder """

    def default(self, obj):  # pylint: disable=method-hidden,arguments-differ
        """ Encode an object to JSON """

        if isinstance(obj, datetime.datetime):
            return obj.isoformat(timespec='milliseconds')

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, enum.Enum):
            return obj.value

        from api.db.base import Base
        if isinstance(obj, Base):
            return obj.serialize()

        return super(JSONEncoder, self).default(obj)
