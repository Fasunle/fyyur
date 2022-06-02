
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup_db(app):
    '''Setup database with its configuration. It uses flask_migrate as schema migration tool'''

    db.init_app(app)

    # uses Alembic under the hood
    # https://flask-migrate.readthedocs.io/en/latest/
    Migrate(app, db)
