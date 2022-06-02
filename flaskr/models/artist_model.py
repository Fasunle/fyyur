import sys
from flask import jsonify, request
from flaskr.models import db
from flaskr.models.show_model import Show
from flaskr.models.venue_model import Venue
from flaskr.utils import past_or_upcoming_shows


class Artist(db.Model):
    """
    Artist model inherit from a base class and thus, we can manipulate the class using  
    Args:
        db (BaseModel): BaseModel is an SQLAlchemy base class 

        you could check this: 

        https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/#model-class
    """
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(120), nullable=False)
    show = db.relationship("Show", cascade="all, delete-orphan")

    def fetch_all() -> list:
        '''Fetcl all artists and return json format'''

        artists = Artist.query.all()

        formated_artists = [
            jsonify({
                "id": artist.id,
                "city": artist.city,
                "name": artist.name,
                "phone": artist.phone,
                "state": artist.state,
                "genres": artist.genres,
                "website_link": artist.website_link,
                "facebook_link": artist.facebook_link,
                "seeking_venue": artist.seeking_venue,
                "seeking_description": artist.seeking_description
            })

            for artist in artists
        ]

        return formated_artists

    def fetch(id: int):
        '''Fetch and format artist with a given id'''

        artist = Artist.query.filter_by(id=id).first()
        return jsonify({
            "id": artist.id,
            "city": artist.city,
            "name": artist.name,
            "phone": artist.phone,
            "state": artist.state,
            "genres": artist.genres,
            "website_link": artist.website_link,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description
        })
