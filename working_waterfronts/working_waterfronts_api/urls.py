from django.conf.urls import patterns
from django.conf.urls import url

url_base = 'working_waterfronts.working_waterfronts_api'

urlpatterns = patterns(
    '',

    url(r'^entry/hazards/new/?$',
        url_base + '.views.entry.hazards.hazard',
        name='new-hazard'),

    url(r'^entry/hazards/(?P<id>\d+)/?$',
        url_base + '.views.entry.hazards.hazard',
        name='edit-hazard'),

    url(r'^entry/hazards/?$',
        url_base + '.views.entry.hazards.list',
        name='entry-list-hazards'),

    url(r'^entry/?$',
        url_base + '.views.entry.home.home',
        name='home'),

    url(r'^entry/categories/(?P<id>\d+)/?$',
        url_base + '.views.entry.categories.category',
        name='edit-category'),

    url(r'^entry/categories/new/?$',
        url_base + '.views.entry.categories.category',
        name='new-category'),

    url(r'^entry/categories/?$',
        url_base + '.views.entry.categories.list',
        name='entry-list-categories'),

    url(r'^entry/images/(?P<id>\d+)/?$',
        url_base + '.views.entry.images.image',
        name='edit-image'),

    url(r'^entry/images/new/?$',
        url_base + '.views.entry.images.image',
        name='new-image'),

    url(r'^entry/images/?$',
        url_base + '.views.entry.images.image_list',
        name='entry-list-images'),

    url(r'^1/pois/?$',
        url_base + '.views.pointsofinterest.poi_list',
        name='pois-list'),
)
