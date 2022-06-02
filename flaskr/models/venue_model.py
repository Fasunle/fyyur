from flask import flash, jsonify
from flaskr.models import db


class Venue(db.Model):
    """
    Venue model inherit from a base class and thus, we can manipulate the class using  

    Args:
        db (Model): Base class which enables us to use SQLAlchemy API on our class 'Venue'
    """

    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(120), nullable=False)
    show = db.relationship("Show", cascade="all, delete-orphan")

    def create(self, name: str):
        """
            Create a new Venue

            Args:
                name (string): Name of the venue. It is just used for flash message

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
            message = 'Venue ' + name + ' was successfully listed!'
        except:
            error = True
            message = 'An error occurred. Venue ' + name + ' could not be listed.'
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

    def delete(id):
        """
            Delete an venue with a specific id

            returns: 
                {
                    "success": not error,
                    "message": message
                }

        """

        venue = Venue.query.get(id)
        error = False
        message = ""

        try:
            db.session.delete(venue)
            # db.session.commit()
            message = f"Venue with {id} was deleted!"
        except:
            message = f"Unable to delete Venue with {id}"
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

    def fetch(id: int):
        '''Fetch and format venue with a given id'''

        venue = Venue.query.filter_by(id=id).first()
        return {
            "id": venue.id,
            "address": venue.address,
            "city": venue.city,
            "name": venue.name,
            "phone": venue.phone,
            "state": venue.state,
            "genres": venue.genres,
            "website_link": venue.website_link,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description
        }

    def fetch_all() -> list:
        '''Fetcl all artists and return json format'''

        artists = Venue.query.all()

        formated_artists = [
            {
                "id": venue.id,
                "address": venue.address,
                "city": venue.city,
                "name": venue.name,
                "phone": venue.phone,
                "state": venue.state,
                "genres": venue.genres,
                "website_link": venue.website_link,
                "facebook_link": venue.facebook_link,
                "seeking_venue": venue.seeking_venue,
                "seeking_description": venue.seeking_description
            }

            for venue in artists
        ]

        return formated_artists

    def update(self, id):
        """
            Update an Venue

            Args:
                name (string): Name of the venue. It is just used for flash message

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
            message = "Editted the venue with id " + str(id) + " successfully"
        except:
            error = True
            message = "Unable to edit the venue with id " + str(id)
            db.session.rollback()
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
