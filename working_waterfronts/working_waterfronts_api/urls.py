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

    url(r'^entry/pois/(?P<id>\d+)/?$',
        url_base + '.views.entry.pois.poi',
        name='edit-poi'),

    url(r'^entry/pois/new/?$',
        url_base + '.views.entry.pois.poi',
        name='new-poi'),

    url(r'^entry/pois/?$',
        url_base + '.views.entry.pois.list',
        name='entry-list-pois'),

    url(r'^1/pois/?$',
        url_base + '.views.pointsofinterest.poi_list',
        name='pois-list'),

    url(r'^1/pois/(?P<id>\d+)/?$',
        url_base + '.views.pointsofinterest.poi_details',
        name='poi-details'),

    url(r'^entry/pois/?$',
        url_base + '.views.pointsofinterest.poi_list',
        name='entry-list-pois'),

    url(r'^entry/videos/(?P<id>\d+)/?$',
        url_base + '.views.entry.videos.video',
        name='edit-video'),

    url(r'^entry/videos/?$',
        url_base + '.views.entry.videos.video_list',
        name='entry-list-videos'),

    url(r'^entry/videos/new/?$',
        url_base + '.views.entry.videos.video',
        name='new-video'),

    url(r'^1/pois/categories/(?P<id>\d+)/?$',
        url_base + '.views.pointsofinterest.poi_categories',
        name='pois-categories'),
    url(r'^login/?$',
        url_base + '.views.entry.login.login_user',
        name='login'),

    url(r'^logout/?$',
        url_base + '.views.entry.login.logout_user',
        name='logout'),

    url(r'^/?$',
        url_base + '.views.entry.login.root',
        name='root'),

    url(r'^entry/categories/?$',
        url_base + '.views.entry.categories.category_list',
        name='entry-list-categories'),
)
