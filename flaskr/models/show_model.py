from datetime import datetime
from flask import flash, jsonify

from flaskr.models import db


class Show(db.Model):
    """This links both the Artist Model and Venue model via their primary keys. This, it has a relatioship with the both.

    Args:
        db (Model): Base class which enables us to use SQLAlchemy API on our class 'Show'
    """

    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(
        db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(
        db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now())

    def create(self):
        """
        Create a show from Artist id and Venue id, and optionally, 
        specify the start_time
        """

        error = False
        message = ""

        try:
            db.session.add(self)
            db.session.commit()
            message = 'Show was successfully listed!'
        except:
            error = True
            message = 'An error occurred. Show could not be listed.'
            db.session.rollback()
        finally:
            db.session.close()

        if error:
            # on unsuccessful db insert, flash an error instead.
            flash(message)
        else:
            # on successful db insert, flash success
            flash(message)

        return jsonify({
            "success": not error,
            "message": message
        })

    def fetch(id):
        '''Fetches a single show'''

        show = Show.query.get(id)

        return {
            "artist_id": show.artist_id,
            "venue_id": show.venue_id,
            "start_time": show.start_time
        }

    def fetch_all():
        shows = Show.query.all()

        return [
            {
                "artist_id": show.artist_id,
                "venue_id": show.venue_id,
                "start_time": show.start_time
            }

            for show in shows
        ]
