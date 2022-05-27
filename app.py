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


def past_or_upcoming_shows():
    '''
    Sort shows into past show and upcoming show.

    It uses Show Model under ther hood
    '''

    past = []
    upcoming = []
    data = {"past": past, "upcoming": upcoming}
    # fetch the shows from the database
    shows = Show.query.all()

    # type casting ensure no error since database had converted start_time to string
    current_time = datetime.now()

    for show in shows:
        if show.start_time > current_time:
            data['upcoming'].append(show)
        else:
            data['past'].append(show)
    return data

#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # replace with real venues data.
    unique_city_names = []
    data = []

    venues = Venue.query.all()

    upcoming_shows = past_or_upcoming_shows()["upcoming"]

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
                    "name": venue.name,
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
                        "name": venue.name,
                        "num_upcoming_shows": upcoming
                    }
                ]
            })

    # confirms that the sorting is correct
    assert len(data) == len(unique_city_names)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data1 = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": [{
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "genres": ["Classical", "R&B", "Hip-Hop"],
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "website": "https://www.theduelingpianos.com",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "past_shows": [{
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [{
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 1,
        "upcoming_shows_count": 1,
    }
    data = list(filter(lambda d: d['id'] ==
                venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=data)

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
                    name=venue.name.data,
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
        # print(sys.exc_info())
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
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # replace with real artist data from the artist table, using artist_id

    # Todo: handle the genres to display if it is multi-field

    all_artists = []
    each_artist = {}

    artists = Artist.query.all()    # get all artists

    # loop through all artists
    for artist in artists:
        # build the artist data

        each_artist["id"] = artist.id
        each_artist["city"] = artist.city
        each_artist["name"] = artist.name
        each_artist["phone"] = artist.phone
        each_artist["state"] = artist.state
        each_artist["genres"] = artist.genres
        each_artist["website"] = artist.website_link
        each_artist["image_link"] = artist.image_link
        each_artist["facebook_link"] = artist.facebook_link
        each_artist["seeking_venue"] = artist.seeking_venue
        each_artist["seeking_description"] = artist.seeking_description
        each_artist["past_shows"] = []
        each_artist["upcoming_shows"] = []
        each_artist["past_shows_count"] = 0
        each_artist["upcoming_shows_count"] = 0

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
                        "venue_name": venue.name,
                        "venue_image_link": venue.image_link,
                        "start_time": show.start_time
                    }
                )
            # add upcoming show feilds to the artists data
            else:
                each_artist["upcoming_shows"].append(
                    {
                        "venue_id": venue.id,
                        "venue_name": venue.name,
                        "venue_image_link": venue.image_link,
                        "start_time": show.start_time
                    }
                )
        each_artist["past_shows_count"] = len(each_artist["past_shows"])
        each_artist["upcoming_shows_count"] = len(
            each_artist["upcoming_shows"])

        # put the complete data into all_artists array
        all_artists.append(each_artist)
        each_artist = {}    # reset

    # print("\n", all_artists, "\n")

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
        old_artist_data.name = artist.name.data
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
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
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
    name = artist.name.data

    # create Artist if the form is validated -> properly submitted
    if artist.validate():
        try:
            db.session.add(
                Artist(
                    name=artist.name.data,
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
        eachShow['artist_name'] = artist.name
        eachShow['venue_name'] = venue.name
        eachShow['venue_id'] = venue.name
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

    # print('\n----------------\n')
    # print(show.artist_id.data)
    # print('\n----------------\n')

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
