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

)
