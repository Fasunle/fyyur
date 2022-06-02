import babel
import dateutil.parser
from datetime import datetime


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


def get_genres(genres: str = "") -> list:
    '''
        reformat the genres data from string to a list
    '''
    result = []

    # if genres is not selected
    if not len(genres):
        return result

    # if genres is of format {Classical, "Afrobeat Pop", "Hip Hop"}
    if genres[0] is '{':

        _genres = genres[1:-1]
        genre_list = _genres.split(",")

        for x in genre_list:

            if x[0] is '"':
                result.append(x[1:-1])
            else:
                result.append(x)

        return result

    # if the genres is a single field e.g Classical
    else:
        return result.append(genres)


def past_or_upcoming_shows(shows: tuple) -> dict:
    '''
    Sort shows into past show and upcoming show.
    It uses Show Model under ther hood
    '''

    past = []
    upcoming = []
    data = {"past": past, "upcoming": upcoming}
    # fetch the shows from the database

    # type casting ensure no error since database had converted start_time to string
    current_time = datetime.now()

    for show in shows:
        if show.start_time > current_time:
            data['upcoming'].append(show)
        else:
            data['past'].append(show)
    return data
