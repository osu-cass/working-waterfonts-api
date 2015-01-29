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

    url(r'^1/pois/?$',
        'working_waterfronts.working_waterfronts_api.views.pointsofinterest.poi_list',
        name='pois-list'),
    url(r'^1/poi/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.poi.poi_details',
        name='poi-details'),
)
