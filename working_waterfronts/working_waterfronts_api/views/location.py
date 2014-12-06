from django.http import HttpResponse
from working_waterfronts.working_waterfronts_api.models import PointOfInterest
import json


def locations(request):
    """
    */locations/*

    Returns a list of city names for all pointofinterests. Useful for populating
    selection lists.
    """
    pointofinterest_list = PointOfInterest.objects.all()
    cities = [pointofinterest.city for pointofinterest in pointofinterest_list]
    unique_cities = [
        {'location': city[0], 'name': city[1]}
        for city in enumerate(set(cities))]

    data = {
        'locations': unique_cities,
        'error': {
            'status': False,
            'name': None,
            'text': None,
            'level': None,
            'debug': None
        }
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
