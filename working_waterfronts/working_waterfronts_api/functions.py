import requests
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test
from django.contrib.gis.geos import fromstr


class BadAddressException(Exception):

    """
    The exception thrown if the address passed in invalid.
    """


def coordinates_from_address(street, city, state, zip):
    """
    This function returns a list of the coordinates from the address
    passed using the Google Geocoding API. If the address given does not
    return an exact coordinates (for instance, if the address can only be
    located down to the city), a BadAddressException is thrown.

    TODO: this should probably return a tuple, rather than a list.
    """
    try:
        full_address = street + ", " + city + ", " + state + " " + zip
        base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="

        response = requests.get(base_url + full_address)
        location_data = response.json()

        if location_data['results'][0][
                'geometry']['location_type'] == 'APPROXIMATE':
            raise BadAddressException("Address %s not found" % full_address)

        lat = float(location_data['results'][0]['geometry']['location']['lat'])
        long = float(
            location_data['results'][0]['geometry']['location']['lng'])

        return [lat, long]
    except:
        raise BadAddressException("Address %s not found" % full_address)


def get_lat_long_prox(request, error=None):
    """
    Parse the latitude, longitude, proximity, and limit for the Vendor
    list functions.

    If the parsing results in an error, the error block is updated to reflect
    that error.
    """
    limit, error = get_limit(request, error)

    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    proximity = request.GET.get('proximity', None)

    point = None

    if lat or lng:
        if proximity:
            try:
                proximity = int(proximity)
            except Exception as e:
                error = {
                    "level": "Warning",
                    "status": True,
                    "name": "Bad proximity",
                    "text": "There was an error finding PointsOfInterest "
                            "within {0} miles".format(proximity),
                    'debug': "{0}: {1}".format(type(e).__name__, str(e))
                }
                proximity = settings.DEFAULT_PROXIMITY
        else:
            proximity = settings.DEFAULT_PROXIMITY

        try:
            point = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)
        except Exception as e:
            error = {
                "level": "Warning",
                "status": True,
                "name": "Bad location",
                "text": "There was an error with the given "
                        "coordinates {0}, {1}".format(lat, lng),
                'debug': "{0}: {1}".format(type(e).__name__, str(e))
            }

    return [point, proximity, limit, error]


def get_limit(request, error=None):
    """
    Return the limit requested by the user.

    If the limit results in an error, the error block is updated to reflect
    that error.
    """
    limit = request.GET.get('limit', None)
    if limit is None:
        return [limit, error]
    try:
        return [int(limit), error]
    except Exception as e:
        error = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Warning',
            'text': 'Invalid limit. Returning all results.',
            'name': 'Bad Limit'
        }
        return [None, error]
