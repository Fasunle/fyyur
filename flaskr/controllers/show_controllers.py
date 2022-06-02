from flask import flash, render_template, request

from flaskr.models.artist_model import Artist
from flaskr.models.show_model import Show
from flaskr.models.venue_model import Venue
from flaskr.models import db
from flaskr.forms import ShowForm


def show_controllers(app):
    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        shows = Show.query.all()

        eachShow = {}
        data = []

        for show in shows:
            # get artist and venue for a given Show
            artist = Artist.query.filter_by(id=show.artist_id).first()
            venue = Venue.query.filter_by(id=show.venue_id).first()
            eachShow['artist_name'] = artist.name.title()
            eachShow['venue_name'] = venue.name.title()
            eachShow['venue_id'] = venue.id
            eachShow['artist_id'] = artist.id
            eachShow['start_time'] = str(show.start_time)
            eachShow['artist_image_link'] = artist.image_link

            # push into the data list
            data.append(eachShow)
            eachShow = {}

        return render_template('pages/shows.html', shows=data)

    @app.route('/shows/create')
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # insert form data as a new Show record in the db, instead
        show = ShowForm(request.form)

        if show.validate():
            Show.create(
                Show(
                    artist_id=show.artist_id.data,
                    venue_id=show.venue_id.data,
                    start_time=show.start_time.data
                )
            )

        return render_template('pages/home.html')
