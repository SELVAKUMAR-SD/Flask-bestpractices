''' Create db tables '''
import config
from api.db.session import engine
from api.db.base import Base
from run_migration import run_migrations
import api.models # pylint:disable=unused-import


def create_all():
    ''' Create all database tables '''
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all()
    # run_migrations(config.PATH_TO_MIGRATIONS, config.DB_URL)
