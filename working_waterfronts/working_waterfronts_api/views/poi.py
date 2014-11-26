from django.http import (HttpResponse,
                         HttpResponseNotFound)
from django.contrib.gis.measure import D
from whats_fresh.whats_fresh_api.models import POI
from whats_fresh.whats_fresh_api.functions import get_lat_long_prox

import json
from .serializer import FreshSerializer


def poi_list(request):
    """
    */pois/*

    List all pois in the database. There is no order to this list,
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
        poi_list = POI.objects.filter(
            location__distance_lte=(point, D(mi=proximity)))[:limit]
    else:
        poi_list = POI.objects.all()[:limit]

    if not poi_list:
        error = {
            "status": True,
            "name": "No POIs",
            "text": "No POIs found",
            "level": "Information",
            "debug": ""
        }

    serializer = FreshSerializer()

    data = {
        "pois": json.loads(
            serializer.serialize(
                poi_list,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def pois_products(request, id=None):
    """
    */pois/products/<id>*

    List all pois in the database that sell product <id>.
    There is no order to this list, only whatever is returned by the database.
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
    try:
        if point:
            poi_list = POI.objects.filter(
                poiproduct__product_preparation__product__id__exact=id,
                location__distance_lte=(point, D(mi=proximity)))[:limit]
        else:
            poi_list = POI.objects.filter(
                poiproduct__product_preparation__product__id__exact=id
            )[:limit]

    except Exception as e:
        error = {
            'status': True,
            'name': 'Invalid product',
            'text': 'Product id is invalid',
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    if not poi_list:
        error = {
            "status": True,
            "name": "No POIs",
            "text": "No POIs found for product %s" % id,
            "level": "Information",
            "debug": ""
        }

    serializer = FreshSerializer()

    data = {
        "pois": json.loads(
            serializer.serialize(
                poi_list,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def poi_details(request, id=None):
    """
    */pois/<id>*

    Returns the poi data for poi <id>.
    """
    data = {}

    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }

    try:
        poi = POI.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'POI Not Found',
            'text': 'POI id %s was not found.' % id,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    serializer = FreshSerializer()

    data = json.loads(
        serializer.serialize(
            [poi],
            use_natural_foreign_keys=True
        )[1:-1]  # Serializer can only serialize lists,
        # so we have to chop off the list brackets
        # to get the serialized string without the list
    )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")
