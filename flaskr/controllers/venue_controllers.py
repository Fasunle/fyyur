from datetime import datetime
from flask import flash, render_template, request

from flaskr.utils import get_genres, past_or_upcoming_shows
from flaskr.models.artist_model import Artist
from flaskr.models.show_model import Show
from flaskr.models.venue_model import Venue
from flaskr.models import db
from flaskr.forms import VenueForm, ArtistForm, ShowForm


def venue_controllers(app):
    '''Venue controllers'''

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
        # case-insensitive.
        #  seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        search_term = request.form.get('search_term', '')
        found_venues = Venue.query.filter(
            Venue.name.op("~")(search_term.lower())).all()
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

        if venue.validate():
            Venue.create(Venue(
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
            ), name)

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
                flash("Editted the artist with id " +
                      str(venue_id) + " successfully")

            return redirect(url_for('show_venue', venue_id=venue_id))
