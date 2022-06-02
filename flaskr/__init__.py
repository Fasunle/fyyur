from flask import Flask
from flask_moment import Moment


from flaskr.controllers import controllers
from flaskr.models import setup_db
from flaskr.utils import format_datetime


def create_app():
    app = Flask(__name__)

    # CONFIGURATIONS
    app.config.from_pyfile("config.py")
    app.jinja_env.filters['datetime'] = format_datetime
    Moment(app)
    setup_db(app)
    # controllers
    controllers(app)

    return app
