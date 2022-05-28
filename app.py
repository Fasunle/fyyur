#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
from xmlrpc.client import DateTime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from utils import get_genres, past_or_upcoming_shows
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Done: connected to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
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


# Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Artist(db.Model):
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


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(
        db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(
        db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now())


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # replace with real venues data.
    unique_city_names = []
    data = []

    venues = Venue.query.all()
    shows = Show.query.all()

    upcoming_shows = past_or_upcoming_shows(shows)["upcoming"]

    # get unique venues by the venue name
    for venue in venues:

        upcoming = 0
        # calculate the number ofshow that each venue has
        for show in upcoming_shows:

            if show.venue_id == venue.id:

                upcoming += 1

        if venue.city in unique_city_names:

            already_present_at_index = unique_city_names.index(venue.city)

            present = data[already_present_at_index]["venues"]

            present.append(
                {
                    "id": venue.id,
                    "name": venue.name.title(),
                    "num_upcoming_shows": upcoming
                }
            )
        else:
            # construct a unique list
            unique_city_names.append(venue.city)

            # format the data as this
            data.append({
                "city": venue.city,
                "state": venue.state,
                "venues": [
                    {
                        "id": venue.id,
                        "name": venue.name.title(),
                        "num_upcoming_shows": upcoming
                    }
                ]
            })

    # confirms that the sorting is correct
    assert len(data) == len(unique_city_names)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    #  implement search on artists with partial string search. Ensure it is
    # TODO: case-insensitive.
    #  seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = str(request.form.get('search_term', '')).lower()
    found_venues = Venue.query.filter(Venue.name.op("~")(search_term)).all()
    shows = Show.query.all()
    upcoming_shows = past_or_upcoming_shows(shows)["upcoming"]
    response = {"data": [], "count": len(found_venues)}

    for venue in found_venues:
        response["data"].append(
            {
                "id": venue.id,
                "name": venue.name.title(),
                "num_upcomint_shows": len(
                    [upcoming_show.venue_id is venue.id for upcoming_show in upcoming_shows]
                )
            }
        )

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # replace with real venue data from the venues table, using venue_id
    all_venues = []
    each_venue = {}

    venues = Venue.query.all()    # get all artists
    shows = Show.query.filter_by(venue_id=venue_id).all()

    # loop through all artists
    for venue in venues:
        # build the venue data

        each_venue["id"] = venue.id
        each_venue["city"] = venue.city
        each_venue["name"] = venue.name.title()
        each_venue["phone"] = venue.phone
        each_venue["state"] = venue.state
        each_venue["genres"] = get_genres(venue.genres)
        each_venue["address"] = venue.address
        each_venue["website"] = venue.website_link
        each_venue["image_link"] = venue.image_link
        each_venue["facebook_link"] = venue.facebook_link
        each_venue["seeking_talent"] = venue.seeking_talent
        each_venue["seeking_description"] = venue.seeking_description
        each_venue["past_shows"] = []
        each_venue["upcoming_shows"] = []
        each_venue["past_shows_count"] = 0
        each_venue["upcoming_shows_count"] = 0

        # loop through the show table
        for show in shows:

            # get the corresponding venue data for each show
            artist = Artist.query.get(show.artist_id)

            # add past show feilds to the artists data
            if show.start_time < datetime.now():
                each_venue["past_shows"].append(
                    {
                        "artist_id": artist.id,
                        "artist_name": artist.name.title(),
                        "artist_image_link": artist.image_link,
                        "start_time": str(show.start_time)
                    }
                )
            # add upcoming show feilds to the venue data
            else:
                each_venue["upcoming_shows"].append(
                    {
                        "artist_id": artist.id,
                        "artist_name": artist.name.title(),
                        "artist_image_link": artist.image_link,
                        "start_time": str(show.start_time)
                    }
                )
        each_venue["past_shows_count"] = len(each_venue["past_shows"])
        each_venue["upcoming_shows_count"] = len(
            each_venue["upcoming_shows"])

        # put the complete data into all_artists array
        all_venues.append(each_venue)
        each_venue = {}    # reset

    data = list(filter(lambda d: d['id'] ==
                venue_id, all_venues))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # insert form data as a new Venue record in the db, instead
    # modify data to be the data object returned from db insertion
    venue = VenueForm(request.form)
    name = venue.name.data
    error = False

    if venue.validate():
        try:
            db.session.add(
                Venue(
                    name=venue.name.data.lower(),
                    city=venue.city.data,
                    genres=venue.genres.data,
                    phone=venue.phone.data,
                    state=venue.state.data,
                    address=venue.address.data,
                    facebook_link=venue.facebook_link.data,
                    website_link=venue.website_link.data,
                    image_link=venue.image_link.data,
                    seeking_talent=venue.seeking_talent.data,
                    seeking_description=venue.seeking_description.data
                )
            )
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        data = {name}

        if error:
            # on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Venue ' +
                  data.name + ' could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    venue = Venue.query.filter_by(id=venue_id).first()
    try:
        # if Venue is linked with show, delete the show since you are deleting the venue
        # otherwise, foreign key constraint violation will be thrown
        # this also deletes the show because they are related and cascaded

        if venue != None:
            db.session.delete(venue)
        else:
            error = True

        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        flash("Could not delete Venue with id " + str(venue_id))
    else:
        flash("Venue with id " + str(venue_id) + " has been deleted")
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return {}

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # ? IMPROVEMENT: replace with real data returned from querying the database

    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # implement search on artists with partial string search. Ensure it is
    # TODO: case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = str(request.form.get('search_term', '')).lower()
    found_artists = Artist.query.filter(Artist.name.op("~")(search_term)).all()
    shows = Show.query.all()
    upcoming_shows = past_or_upcoming_shows(shows)["upcoming"]
    response = {"data": [], "count": len(found_artists)}

    for artist in found_artists:
        response["data"].append(
            {
                "id": artist.id,
                "name": artist.name.title(),
                "num_upcomint_shows": len(
                    [upcoming_show.artist_id is artist.id for upcoming_show in upcoming_shows]
                )
            }
        )

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # replace with real artist data from the artist table, using artist_id

    all_artists = []
    each_artist = {}

    artists = Artist.query.all()    # get all artists

    # loop through all artists
    for artist in artists:
        # build the artist data

        each_artist["id"] = artist.id
        each_artist["city"] = artist.city
        each_artist["name"] = artist.name.title()
        each_artist["phone"] = artist.phone
        each_artist["state"] = artist.state
        each_artist["genres"] = get_genres(artist.genres)
        each_artist["website"] = artist.website_link
        each_artist["image_link"] = artist.image_link
        each_artist["facebook_link"] = artist.facebook_link
        each_artist["seeking_venue"] = artist.seeking_venue
        each_artist["seeking_description"] = artist.seeking_description
        each_artist["past_shows"] = []
        each_artist["upcoming_shows"] = []
        each_artist["past_shows_count"] = 0
        each_artist["upcoming_shows_count"] = 0

        if artist_id is not artist.id:
            continue

        shows = Show.query.filter_by(artist_id=artist_id).all()
        # loop through the show table
        for show in shows:

            # get the corresponding venue data for each show
            venue = Venue.query.get(id=show.venue_id)

            # add past show feilds to the artists data
            if show.start_time < datetime.now():
                each_artist["past_shows"].append(
                    {
                        "venue_id": venue.id,
                        "venue_name": venue.name.title(),
                        "venue_image_link": venue.image_link,
                        "start_time": show.start_time
                    }
                )
            # add upcoming show feilds to the artists data
            else:
                each_artist["upcoming_shows"].append(
                    {
                        "venue_id": venue.id,
                        "venue_name": venue.name.title(),
                        "venue_image_link": venue.image_link,
                        "start_time": str(show.start_time)
                    }
                )
        each_artist["past_shows_count"] = len(each_artist["past_shows"])
        each_artist["upcoming_shows_count"] = len(
            each_artist["upcoming_shows"])

        # put the complete data into all_artists array
        all_artists.append(each_artist)
        each_artist = {}    # reset

    data = list(filter(lambda d: d['id'] ==
                artist_id, all_artists))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    # populate form with fields from artist with ID <artist_id>
    artist = Artist.query.filter_by(id=artist_id).first()
    artist.name.title()

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    artist = ArtistForm(request.form)
    error = False

    try:
        old_artist_data = Artist.query.filter_by(id=artist_id).first()

        # update the data with form data (artist)
        old_artist_data.name = artist.name.data.lower()
        old_artist_data.city = artist.city.data
        old_artist_data.phone = artist.phone.data
        old_artist_data.state = artist.state.data
        old_artist_data.genres = artist.genres.data
        old_artist_data.image_link = artist.image_link.data
        old_artist_data.facebook_link = artist.facebook_link.data
        old_artist_data.seeking_venue = artist.seeking_venue.data
        old_artist_data.seeking_description = artist.seeking_description.data

        db.session.add(old_artist_data)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        flash("Unable to edit the artist with id " + str(artist_id))
    else:
        flash("Editted the artist with id " + str(artist_id) + " successfully")

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    # populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    venue = VenueForm(request.form)
    error = False

    try:
        old_venue_data = Venue.query.filter_by(id=venue_id).first()

        # update the data with form data (venue)
        old_venue_data.name = venue.name.data.lower()
        old_venue_data.city = venue.city.data
        old_venue_data.phone = venue.phone.data
        old_venue_data.state = venue.state.data
        old_venue_data.genres = venue.genres.data
        old_venue_data.image_link = venue.image_link.data
        old_venue_data.facebook_link = venue.facebook_link.data
        old_venue_data.seeking_talent = venue.seeking_talent.data
        old_venue_data.seeking_description = venue.seeking_description.data

        db.session.add(old_venue_data)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        flash("Unable to edit the artist with id " + str(venue_id))
    else:
        flash("Editted the artist with id " + str(venue_id) + " successfully")

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # insert form data as a new Artist record in the db, instead
    #
    # Get the submitted form
    artist = ArtistForm(request.form)
    error = False
    name = artist.name.data.title()

    # create Artist if the form is validated -> properly submitted
    if artist.validate():
        try:
            db.session.add(
                Artist(
                    name=artist.name.data.lower(),
                    city=artist.city.data,
                    genres=artist.genres.data,
                    phone=artist.phone.data,
                    state=artist.state.data,
                    facebook_link=artist.facebook_link.data,
                    website_link=artist.website_link.data,
                    image_link=artist.image_link.data,
                    seeking_venue=artist.seeking_venue.data,
                    seeking_description=artist.seeking_description.data
                )
            )
            # persist the change
            db.session.commit()
        except:
            # error occured
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        # modify data to be the data object returned from db insertion
        data = {name}

        if error:
            # on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Artist ' +
                  data.name + ' could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

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
        error = False
        try:
            db.session.add(
                Show(
                    artist_id=show.artist_id.data,
                    venue_id=show.venue_id.data,
                )
            )
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        # on unsuccessful db insert, flash an error instead.
        if error:
            flash('An error occurred. Show could not be listed.')

        # on successful db insert, flash success
        else:
            flash('Show was successfully listed!')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
