
from flask import Flask, render_template

from flaskr.controllers.artist_controllers import artist_controllers
from flaskr.controllers.error_handlers import error_handlers
from flaskr.controllers.show_controllers import show_controllers
from flaskr.controllers.venue_controllers import venue_controllers


def controllers(app: Flask) -> None:
    """
    Controller function wrap all controller functions including error handler and some       
    general controllers
    """

    artist_controllers(app)
    venue_controllers(app)
    show_controllers(app)

    @app.route('/')
    def index():
        return render_template('pages/home.html')

    error_handlers(app)  # Error handling controller
