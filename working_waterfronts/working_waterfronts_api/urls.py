from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    '',

    url(r'^entry/hazards/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.hazards.hazard',
        name='new-hazard'),

    url(r'^entry/hazards/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.hazards.hazard',
        name='edit-hazard'),

    url(r'^entry/hazards/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.hazards.list',
        name='entry-list-hazards'),

    url(r'^entry/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.home.home',
        name='home'),

    url(r'^entry/images/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.images.image',
        name='edit-image'),

    url(r'^entry/images/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.images.image',
        name='new-image'),

    url(r'^entry/images/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.images.image_list',
        name='entry-list-images'),

    url(r'^1/pois/?$',
        'working_waterfronts.working_waterfronts_api.views.pointsofinterest.poi_list',
        name='pois-list'),
)
