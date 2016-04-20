import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.gis.geos import fromstr
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from working_waterfronts.working_waterfronts_api.models import (
    PointOfInterest, Image, Video, Category, Hazard)
from working_waterfronts.working_waterfronts_api.functions import (
    coordinates_from_address, BadAddressException)
from working_waterfronts.working_waterfronts_api.forms import (
    PointOfInterestForm)


@login_required
def list(request):
    """
    */entry/pois*

    The entry interface's pois list. This view lists all pois,
    their description, and allows you to click on them to view/edit the
    poi.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Point Of Interest deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Point Of Interest saved successfully!"

    paginator = Paginator(PointOfInterest.objects.order_by('name'),
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
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-poi'),
        'new_text': "New Item",
        'title': "Points Of Interest",
        'item_classification': "item",
        'item_list': pois,
        'edit_url': 'edit-poi'
    })


@login_required
def poi(request, id=None):
    """
    */entry/pois/<id>*, */entry/pois/new*

    The entry interface's edit/add/delete poi view. This view creates
    the edit page for a given poi, or the "new poi" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    pois.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        poi = get_object_or_404(PointOfInterest, pk=id)
        poi.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        try:
            try:
                post_data['location'] = fromstr(
                    'POINT(%s %s)' % (post_data['longitude'],
                                      post_data['latitude']), srid=4326)

            except:
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
            categories = [Category.objects.get(
                pk=int(c)) for c in post_data.get(
                    'category_ids', None).split(',')]
        except:
            errors.append("You must choose at least one category.")

        poi_form = PointOfInterestForm(post_data)
        if poi_form.is_valid() and not errors:
            image_keys = post_data.get('image_ids', None)
            images = []
            if image_keys:
                images = [Image.objects.get(
                    pk=int(i)) for i in image_keys.split(',')]

            video_keys = post_data.get('video_ids', None)
            videos = []
            if video_keys:
                videos = [Video.objects.get(
                    pk=int(v)) for v in video_keys.split(',')]

            hazard_keys = post_data.get('hazard_ids', None)
            hazards = []
            if hazard_keys:
                hazards = [Hazard.objects.get(
                    pk=int(h)) for h in hazard_keys.split(',')]
            if id:
                poi = PointOfInterest.objects.get(id=id)
                # process images
                existing_images = poi.images.all()
                for image in existing_images:
                    if image not in images:
                        poi.images.remove(image)
                for image in images:
                    if image not in existing_images:
                        poi.images.add(image)
                # process videos
                existing_videos = poi.videos.all()
                for video in existing_videos:
                    if video not in videos:
                        poi.videos.remove(video)
                for video in videos:
                    if video not in existing_videos:
                        poi.videos.add(video)
                # process hazards
                existing_hazards = poi.hazards.all()
                for hazard in existing_hazards:
                    if hazard not in hazards:
                        poi.hazards.remove(hazard)
                for hazard in hazards:
                    if hazard not in existing_hazards:
                        poi.hazards.add(hazard)
                # process categories
                existing_categories = poi.categories.all()
                for category in existing_categories:
                    if category not in categories:
                        poi.categories.remove(category)
                for category in categories:
                    if category not in existing_categories:
                        poi.categories.add(category)
                poi.__dict__.update(**poi_form.cleaned_data)
                poi.save()
            else:
                poi = poi_form.save()
                for image in images:
                    poi.images.add(image)
                for video in videos:
                    poi.videos.add(video)
                for hazard in hazards:
                    poi.hazards.add(hazard)
                for category in categories:
                    poi.categories.add(category)
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('entry-list-pois'))
        else:
            pass
    else:
        errors = []
        message = ''

    if id:
        poi = PointOfInterest.objects.get(id=id)
        poi.latitude = poi.location[1]
        poi.longitude = poi.location[0]
        title = "Edit {0}".format(poi.name)
        post_url = reverse('edit-poi', kwargs={'id': id})
        poi_form = PointOfInterestForm(
            instance=poi,
            initial={'latitude': poi.latitude, 'longitude': poi.longitude})

        existing_images = poi.images.all()
        existing_videos = poi.videos.all()
        existing_categories = poi.categories.all()
        existing_hazards = poi.hazards.all()

        if request.GET.get('success') == 'true':
            message = "Item saved successfully!"

    elif request.method != 'POST':
        poi_form = PointOfInterestForm()
        post_url = reverse('new-poi')
        title = "New Item"
        existing_images = []
        existing_videos = []
        existing_categories = []
        existing_hazards = []

    else:
        post_url = reverse('new-poi')
        title = "New Item"
        existing_images = []
        existing_videos = []
        existing_categories = []
        existing_hazards = []

    data = {'images': [], 'videos': [], 'categories': [], 'hazards': []}

    for image in Image.objects.all():
        data['images'].append({
            'id': image.id,
            'name': image.name
        })

    for video in Video.objects.all():
        data['videos'].append({
            'id': video.id,
            'name': video.name
        })

    for hazard in Hazard.objects.all():
        data['hazards'].append({
            'id': hazard.id,
            'name': hazard.name
        })

    for category in Category.objects.all():
        data['categories'].append({
            'id': category.id,
            'category': category.category
        })

    return render(request, 'poi.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-pois'),
             'name': 'Points OfInterest'}
        ],
        'existing_images': existing_images,
        'existing_videos': existing_videos,
        'existing_hazards': existing_hazards,
        'existing_categories': existing_categories,
        'data_json': json.dumps(data),
        'data_dict': data,
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': errors,
        'poi_form': poi_form,
    })
