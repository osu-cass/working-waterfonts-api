from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from working_waterfronts.working_waterfronts_api.models import Hazard
from working_waterfronts.working_waterfronts_api.forms import HazardForm
from working_waterfronts.working_waterfronts_api.functions import group_required


def list(request):
    """
    */entry/hazards*

    The entry interface's hazards list. This view lists all hazards,
    their description, and allows you to click on them to view/edit the
    hazard.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Hazard deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Hazard saved successfully!"

    paginator = Paginator(Hazard.objects.order_by('name'),
                          settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        hazards = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hazards = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hazards = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-hazard'),
        'new_text': "New Item",
        'title': "Hazards",
        'item_classification': "item",
        'item_list': hazards,
        'edit_url': 'edit-hazard'
    })


def hazard(request, id=None):
    """
    */entry/hazards/<id>*, */entry/hazards/new*

    The entry interface's edit/add/delete hazard view. This view creates
    the edit page for a given hazard, or the "new hazard" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    hazards.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        hazard = get_object_or_404(Hazard, pk=id)
        hazard.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        hazard_form = HazardForm(post_data)
        if hazard_form.is_valid() and not errors:
            if id:
                hazard = Hazard.objects.get(id=id)
                hazard.__dict__.update(**hazard_form.cleaned_data)
                hazard.save()
            else:
                hazard = Hazard.objects.create(
                    **hazard_form.cleaned_data)
                hazard.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('entry-list-hazards'))
        else:
            pass
    else:
        errors = []
        message = ''

    if id:
        hazard = Hazard.objects.get(id=id)
        title = "Edit {0}".format(hazard.name)
        post_url = reverse('edit-hazard', kwargs={'id': id})
        hazard_form = HazardForm(instance=hazard)

        if request.GET.get('success') == 'true':
            message = "Item saved successfully!"

    elif request.method != 'POST':
        hazard_form = HazardForm()
        post_url = reverse('new-hazard')
        title = "New Item"

    else:
        post_url = reverse('new-hazard')
        title = "New Item"

    return render(request, 'hazard.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-hazards'),
             'name': 'Hazards'}
        ],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': errors,
        'hazard_form': hazard_form,
    })
