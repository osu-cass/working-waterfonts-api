from django.http import (HttpResponse, HttpResponseRedirect)
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.gis.geos import fromstr
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings

from whats_fresh.whats_fresh_api.models import (POI, Product,
                                                ProductPreparation,
                                                POIProduct)
from whats_fresh.whats_fresh_api.forms import POIForm
from whats_fresh.whats_fresh_api.functions import (group_required,
                                                   coordinates_from_address,
                                                   BadAddressException)

import json


@login_required
@group_required('Administration Users', 'Data Entry Users')
def poi(request, id=None):
    """
    */entry/pois/<id>*, */entry/pois/new*

    The entry interface's edit/add/delete poi view. This view creates the
    edit page for a given poi, or the "new poi" page if it is not passed
    an ID. It also accepts POST requests to create or edit pois, and DELETE
    requests to delete the poi.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        poi = get_object_or_404(POI, pk=id)
        poi.delete()
        return HttpResponse()

    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        try:
            coordinates = coordinates_from_address(
                post_data['street'], post_data['city'], post_data['state'],
                post_data['zip'])

            post_data['location'] = fromstr(
                'POINT(%s %s)' % (coordinates[1], coordinates[0]),
                srid=4326)
        # Bad Address will be thrown if Google does not return coordinates for
        # the address, and MultiValueDictKeyError will be thrown if the POST
        # data being passed in is empty.
        except (MultiValueDictKeyError, BadAddressException):
            errors.append("Full address is required.")

        try:
            if not post_data['preparation_ids']:
                errors.append("You must choose at least one product.")
                prod_preps = []
            else:
                prod_preps = list(
                    set(post_data['preparation_ids'].split(',')))
                # TODO: Find better way to do form validation
                # Needed for form validation to pass
                post_data['products_preparations'] = prod_preps[0]

        except MultiValueDictKeyError:
            errors.append("You must choose at least one product.")
            prod_preps = []

        poi_form = POIForm(post_data)
        if poi_form.is_valid() and not errors:
            del poi_form.cleaned_data['products_preparations']
            if id:
                poi = POI.objects.get(id=id)

                # For all of the current poi products,
                for poi_product in poi.poiproduct_set.all():
                    # Delete any that aren't in the returned list
                    if poi_product.product_preparation.id not in prod_preps:
                        poi_product.delete()
                    # And ignore any that are in both the existing and the
                    # returned list
                    elif poi_product.product_preparation.id in prod_preps:
                        prod_preps.remove(
                            poi_product.product_preparation.id)
                # Then, create all of the new ones
                for product_preparation in prod_preps:
                    poi_product = POIProduct.objects.create(
                        poi=poi,
                        product_preparation=ProductPreparation.objects.get(
                            id=product_preparation))
                poi.__dict__.update(**poi_form.cleaned_data)
                poi.save()
            else:
                poi = POI.objects.create(**poi_form.cleaned_data)
                for product_preparation in prod_preps:
                    poi_product = POIProduct.objects.create(
                        poi=poi,
                        product_preparation=ProductPreparation.objects.get(
                            id=product_preparation))
                poi.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('list-pois-edit'))

        existing_prod_preps = []
        for preparation_id in prod_preps:
            product_preparation_object = ProductPreparation.objects.get(
                id=preparation_id)
            existing_prod_preps.append({
                'id': preparation_id,
                'preparation_text':
                    product_preparation_object.preparation.name,
                'product': product_preparation_object.product.name
            })
    else:
        existing_prod_preps = []
        errors = []

    if id:
        poi = POI.objects.get(id=id)
        poi_form = POIForm(instance=poi)
        title = "Edit %s" % poi.name
        message = ""
        post_url = reverse('edit-poi', kwargs={'id': id})
        # If the list already has items, we're coming back to it from above
        # And have already filled the list with the product preparations POSTed
        if not existing_prod_preps:
            for poi_product in poi.poiproduct_set.all():
                existing_prod_preps.append({
                    'id': poi_product.product_preparation.id,
                    'preparation_text':
                        poi_product.product_preparation.preparation.name,
                    'product': poi_product.product_preparation.product.name
                })
    elif request.method != 'POST':
        title = "Add a POI"
        post_url = reverse('new-poi')
        message = "* = Required field"
        poi_form = POIForm()
    else:
        title = "Add aPOI"
        message = "* = Required field"
        post_url = reverse('new-poi')

    data = {}
    product_list = []

    for product in Product.objects.all():
        product_list.append(product.name)
        data[str(product.name)] = []
        for preparation in product.productpreparation_set.all():
            data[str(product.name)].append({
                "value": preparation.id,
                "name": preparation.preparation.name
            })

    json_preparations = json.dumps(data)

    return render(request, 'poi.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('list-pois-edit'), 'name': 'POIs'}],
        'title': title,
        'message': message,
        'post_url': post_url,
        'existing_product_preparations': existing_prod_preps,
        'errors': errors,
        'poi_form': poi_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def poi_list(request):
    """
    */entry/pois*

    The entry interface's pois list. This view lists all pois,
    their description, and allows you to click on them to view/edit the
    poi.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "POI deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "POI saved successfully!"

    paginator = Paginator(POI.objects.order_by('name'),
                          settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        pois = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pois = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pois = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'message': message,
        'new_url': reverse('new-poi'),
        'new_text': "New POI",
        'title': "All POIs",
        'item_classification': "poi",
        'item_list': pois,
        'edit_url': 'edit-poi'
    })
