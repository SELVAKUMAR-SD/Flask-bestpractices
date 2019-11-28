import os

from alembic.command import upgrade, revision
from alembic.config import Config


# TODO Need to support specific revision version
# TODO Downgrade option
# TODO Empty migrations file generation should be ignored

def run_migrations(script_location: str, dsn: str) -> None:
    print('Running DB migrations in %r on %r', script_location, dsn)

    migrations_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(migrations_dir, "alembic.ini")

    config = Config(file_=config_file)
    config.set_main_option("script_location", script_location)
    revision(config, autogenerate=True, message="Creating migrations")
    upgrade(config, "head")
