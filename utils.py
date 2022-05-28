"""Utility file for helper functions
"""


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
