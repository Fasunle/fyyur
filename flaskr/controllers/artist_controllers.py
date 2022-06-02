from datetime import datetime
from flask import flash, jsonify, redirect, render_template, request, url_for

from flaskr.utils import get_genres, past_or_upcoming_shows
from flaskr.models.artist_model import Artist
from flaskr.models.show_model import Show
from flaskr.models.venue_model import Venue
from flaskr.models import db
from flaskr.forms import ArtistForm, ShowForm


def artist_controllers(app):
    '''Artist Controllers'''

    @app.route('/artists')
    def artists():
        # replace with real data returned from querying the database

        data = Artist.fetch_all()

        return render_template('pages/artists.html', artists=data)

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
        name = artist.name.data.title()

        # create Artist if the form is validated -> properly submitted
        if artist.validate():
            Artist.create(artist, name)

        return render_template('pages/home.html')

    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        form = ArtistForm()

        # populate form with fields from artist with ID <artist_id>
        artist = Artist.fetch(artist_id)

        return render_template('forms/edit_artist.html', form=form, artist=artist)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        # take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes

        artist = ArtistForm(request.form)
        old_artist_data = Artist.query.get(id=artist_id)

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

        Artist.update(old_artist_data, artist_id)

        return redirect(url_for('show_artist', artist_id=artist_id))

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        # implement search on artists with partial string search. Ensure it is
        # case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".

        search_term = request.form.get('search_term', '')
        found_artists = Artist.query.filter(
            Artist.name.op("~")(search_term.lower())).all()
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
                venue = Venue.query.get(show.venue_id)

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
