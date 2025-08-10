import os
from pathlib import Path

from alembic import command
from alembic.config import Config


def check_migration(database_uri: str):
    dir_uri = os.path.dirname(__file__)
    alembic = Path(dir_uri) / ".." / ".." / "alembic.ini"
    migrations = Path(dir_uri) / ".." / "alembic"
    alembic_cfg = Config(alembic)
    alembic_cfg.set_main_option('script_location', str(migrations))
    alembic_cfg.set_main_option('sqlalchemy.url', database_uri)
    command.upgrade(alembic_cfg, 'head')
