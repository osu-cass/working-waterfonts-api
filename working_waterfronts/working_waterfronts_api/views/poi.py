from django.http import (HttpResponse,
                         HttpResponseNotFound)
from django.contrib.gis.measure import D
from working_waterfronts.working_waterfronts_api.models import PointOfInterest
from working_waterfronts.working_waterfronts_api.functions import get_lat_long_prox

import json
from .serializer import FreshSerializer


def pointofinterest_list(request):
    """
    */pointofinterests/*

    List all pointofinterests in the database. There is no order to this list,
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
        pointofinterest_list = PointOfInterest.objects.filter(
            location__distance_lte=(point, D(mi=proximity)))[:limit]
    else:
        pointofinterest_list = PointOfInterest.objects.all()[:limit]

    if not pointofinterest_list:
        error = {
            "status": True,
            "name": "No PointOfInterests",
            "text": "No PointOfInterests found",
            "level": "Information",
            "debug": ""
        }

    serializer = FreshSerializer()

    data = {
        "pointofinterests": json.loads(
            serializer.serialize(
                pointofinterest_list,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def pointofinterests_products(request, id=None):
    """
    */pointofinterests/products/<id>*

    List all pointofinterests in the database that sell product <id>.
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
            pointofinterest_list = PointOfInterest.objects.filter(
                pointofinterestproduct__product_preparation__product__id__exact=id,
                location__distance_lte=(point, D(mi=proximity)))[:limit]
        else:
            pointofinterest_list = PointOfInterest.objects.filter(
                pointofinterestproduct__product_preparation__product__id__exact=id
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

    if not pointofinterest_list:
        error = {
            "status": True,
            "name": "No PointOfInterests",
            "text": "No PointOfInterests found for product %s" % id,
            "level": "Information",
            "debug": ""
        }

    serializer = FreshSerializer()

    data = {
        "pointofinterests": json.loads(
            serializer.serialize(
                pointofinterest_list,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def pointofinterest_details(request, id=None):
    """
    */pointofinterests/<id>*

    Returns the pointofinterest data for pointofinterest <id>.
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
        pointofinterest = PointOfInterest.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'PointOfInterest Not Found',
            'text': 'PointOfInterest id %s was not found.' % id,
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
            [pointofinterest],
            use_natural_foreign_keys=True
        )[1:-1]  # Serializer can only serialize lists,
        # so we have to chop off the list brackets
        # to get the serialized string without the list
    )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")
