from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^login/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.login.login_user',
        name='login'),

    url(r'^1/poi/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.poi.poi_details',
        name='poi-details'),
)
