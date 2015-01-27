from django.http import (HttpResponse,
                         HttpResponseNotFound)
from django.contrib.gis.measure import D
from working_waterfronts.working_waterfronts_api.models import PointOfInterest
from working_waterfronts.working_waterfronts_api.functions import get_lat_long_prox

import json
from .serializer import ObjectSerializer


def poi_list(request):
    """
    */pointsofinterest/*

    List all pointsofinterest in the database. There is no order to this list,
    only whatever is returned by the database.
    """
    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }
    data = {}

    point, proximity, limit, error = get_lat_long_prox(request, error)

    if point:
        poi_list = PointOfInterest.objects.filter(
            location__distance_lte=(point, D(mi=proximity)))[:limit]
    else:
        poi_list = PointOfInterest.objects.all()[:limit]

    if not poi_list:
        error = {
            "status": True,
            "name": "No PointsOfInterest",
            "text": "No PointsOfInterest found",
            "level": "Information",
            "debug": ""
        }

    serializer = ObjectSerializer()

    data = {
        "pointsofinterest": json.loads(
            serializer.serialize(
                poi_list,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")
