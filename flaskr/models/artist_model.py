from flask import flash, jsonify
from flaskr.models import db


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

    def delete(id):
        """
            Delete an artist with a specific id

            returns: 
                {
                    "success": not error,
                    "message": message
                }

        """

        artist = Artist.query.get(id)
        error = False
        message = ""

        try:
            db.session.delete(artist)
            # db.session.commit()
            message = f"Artist with {id} was deleted!"
        except:
            message = f"Unable to delete Artist with {id}"
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            flash(message)
        else:
            flash(message)

        return jsonify({
            "success": not error,
            "message": message
        })

    def create(self, name: str):
        """
            Create a new Artist

            Args:
                name (string): Name of the artist. It is just used for flash message

            Returns:
                {
                    "success": error,
                    "message": message
                }
        """
        error = False
        message = ""

        try:
            db.session.add(self)
            db.session.commit()
            message = 'Artist ' + name + ' was successfully listed!'
        except:
            error = True
            message = 'An error occurred. Artist ' + name + ' could not be listed.'
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
