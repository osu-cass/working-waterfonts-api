from django.http import (HttpResponse, HttpResponseRedirect)
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.gis.geos import fromstr
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings

from working_waterfronts.working_waterfronts_api.models import (PointOfInterest, Product,
                                                ProductPreparation,
                                                PointOfInterestProduct)
from working_waterfronts.working_waterfronts_api.forms import PointOfInterestForm
from working_waterfronts.working_waterfronts_api.functions import (group_required,
                                                   coordinates_from_address,
                                                   BadAddressException)

import json


@login_required
@group_required('Administration Users', 'Data Entry Users')
def pointofinterest(request, id=None):
    """
    */entry/pointofinterests/<id>*, */entry/pointofinterests/new*

    The entry interface's edit/add/delete pointofinterest view. This view creates the
    edit page for a given pointofinterest, or the "new pointofinterest" page if it is not passed
    an ID. It also accepts POST requests to create or edit pointofinterests, and DELETE
    requests to delete the pointofinterest.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        pointofinterest = get_object_or_404(PointOfInterest, pk=id)
        pointofinterest.delete()
        return HttpResponse()

    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        try:
            coordinates = coordinates_from_address(
                post_data['street'], post_data['city'], post_data['state'],
                post_data['zip'])

            post_data['location'] = fromstr(
                'PointOfInterestNT(%s %s)' % (coordinates[1], coordinates[0]),
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

        pointofinterest_form = PointOfInterestForm(post_data)
        if pointofinterest_form.is_valid() and not errors:
            del pointofinterest_form.cleaned_data['products_preparations']
            if id:
                pointofinterest = PointOfInterest.objects.get(id=id)

                # For all of the current pointofinterest products,
                for pointofinterest_product in pointofinterest.pointofinterestproduct_set.all():
                    # Delete any that aren't in the returned list
                    if pointofinterest_product.product_preparation.id not in prod_preps:
                        pointofinterest_product.delete()
                    # And ignore any that are in both the existing and the
                    # returned list
                    elif pointofinterest_product.product_preparation.id in prod_preps:
                        prod_preps.remove(
                            pointofinterest_product.product_preparation.id)
                # Then, create all of the new ones
                for product_preparation in prod_preps:
                    pointofinterest_product = PointOfInterestProduct.objects.create(
                        pointofinterest=pointofinterest,
                        product_preparation=ProductPreparation.objects.get(
                            id=product_preparation))
                pointofinterest.__dict__.update(**pointofinterest_form.cleaned_data)
                pointofinterest.save()
            else:
                pointofinterest = PointOfInterest.objects.create(**pointofinterest_form.cleaned_data)
                for product_preparation in prod_preps:
                    pointofinterest_product = PointOfInterestProduct.objects.create(
                        pointofinterest=pointofinterest,
                        product_preparation=ProductPreparation.objects.get(
                            id=product_preparation))
                pointofinterest.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('list-pointofinterests-edit'))

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
        pointofinterest = PointOfInterest.objects.get(id=id)
        pointofinterest_form = PointOfInterestForm(instance=pointofinterest)
        title = "Edit %s" % pointofinterest.name
        message = ""
        post_url = reverse('edit-pointofinterest', kwargs={'id': id})
        # If the list already has items, we're coming back to it from above
        # And have already filled the list with the product preparations POSTed
        if not existing_prod_preps:
            for pointofinterest_product in pointofinterest.pointofinterestproduct_set.all():
                existing_prod_preps.append({
                    'id': pointofinterest_product.product_preparation.id,
                    'preparation_text':
                        pointofinterest_product.product_preparation.preparation.name,
                    'product': pointofinterest_product.product_preparation.product.name
                })
    elif request.method != 'POST':
        title = "Add a PointOfInterest"
        post_url = reverse('new-pointofinterest')
        message = "* = Required field"
        pointofinterest_form = PointOfInterestForm()
    else:
        title = "Add aPointOfInterest"
        message = "* = Required field"
        post_url = reverse('new-pointofinterest')

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

    return render(request, 'pointofinterest.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('list-pointofinterests-edit'), 'name': 'PointOfInterests'}],
        'title': title,
        'message': message,
        'post_url': post_url,
        'existing_product_preparations': existing_prod_preps,
        'errors': errors,
        'pointofinterest_form': pointofinterest_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def pointofinterest_list(request):
    """
    */entry/pointofinterests*

    The entry interface's pointofinterests list. This view lists all pointofinterests,
    their description, and allows you to click on them to view/edit the
    pointofinterest.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "PointOfInterest deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "PointOfInterest saved successfully!"

    paginator = Paginator(PointOfInterest.objects.order_by('name'),
                          settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        pointofinterests = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pointofinterests = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pointofinterests = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'message': message,
        'new_url': reverse('new-pointofinterest'),
        'new_text': "New PointOfInterest",
        'title': "All PointOfInterests",
        'item_classification': "pointofinterest",
        'item_list': pointofinterests,
        'edit_url': 'edit-pointofinterest'
    })
