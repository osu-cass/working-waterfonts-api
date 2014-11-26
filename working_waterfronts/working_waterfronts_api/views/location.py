from django.http import HttpResponse
from working_waterfronts.working_waterfronts_api.models import POI
import json


def locations(request):
    """
    */locations/*

    Returns a list of city names for all pois. Useful for populating
    selection lists.
    """
    poi_list = POI.objects.all()
    cities = [poi.city for poi in poi_list]
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
