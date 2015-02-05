from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from working_waterfronts.working_waterfronts_api.models import Category
from working_waterfronts.working_waterfronts_api.forms import CategoryForm


def list(request):
    """
    */entry/categories*

    The entry interface's categories list. This view lists all categories,
    their description, and allows you to click on them to view/edit the
    category.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Category deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Category saved successfully!"

    paginator = Paginator(Category.objects.order_by('category'),
                          settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-category'),
        'new_text': "New Item",
        'title': "Categories",
        'item_classification': "item",
        'item_list': categories,
        'edit_url': 'edit-category'
    })


def category(request, id=None):
    """
    */entry/categories/<id>*, */entry/categories/new*

    The entry interface's edit/add/delete category view. This view creates
    the edit page for a given category, or the "new category" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    categories.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        category = get_object_or_404(Category, pk=id)
        category.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        category_form = CategoryForm(post_data)
        if category_form.is_valid() and not errors:
            if id:
                category = Category.objects.get(id=id)
                category.__dict__.update(**category_form.cleaned_data)
                category.save()
            else:
                category = Category.objects.create(
                    category=category_form.cleaned_data['category'])
                category.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('entry-list-categories'))
        else:
            pass
    else:
        errors = []
        message = ''

    if id:
        category = Category.objects.get(id=id)
        title = "Edit {0}".format(category.category)
        post_url = reverse('edit-category', kwargs={'id': id})
        category_form = CategoryForm(instance=category)

        if request.GET.get('success') == 'true':
            message = "Item saved successfully!"

    elif request.method != 'POST':
        category_form = CategoryForm()
        post_url = reverse('new-category')
        title = "New Item"

    else:
        post_url = reverse('new-category')
        title = "New Item"

    return render(request, 'category.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-categories'),
             'name': 'Categories'}
        ],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': errors,
        'category_form': category_form,
    })
