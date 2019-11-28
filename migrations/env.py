""" Modified alembic env.py """
import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
# '..' It can change based on the placement from root directory
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

from logging.config import fileConfig

from alembic import context
import sqlalchemy_utils

from config import DB_URL

from api.db.session import engine
from api.db.base import Base

# access to the values within the .ini file in use.
config = context.config

# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == 'type' and isinstance(obj, sqlalchemy_utils.types.uuid.UUIDType):
        # add import for this type
        autogen_context.imports.add("import sqlalchemy_utils")
        autogen_context.imports.add("import uuid")
        return "sqlalchemy_utils.types.uuid.UUIDType(), default=uuid.uuid4"

    # default rendering for other objects
    return False


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DB_URL
    context.configure(url=url,
                      target_metadata=target_metadata,
                      literal_binds=True,
                      compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            compare_type=True
        )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
