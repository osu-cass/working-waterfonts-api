from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    '',
    url(r'^1/stories/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.story.story_details',
        name='story-details'),

    url(r'^1/products/?$',
        'working_waterfronts.working_waterfronts_api.views.product.product_list',
        name='products-list'),
    url(r'^1/products/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.product.product_details',
        name='product-details'),
    url(r'^1/products/pois/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.product.product_poi',
        name='product-poi'),

    url(r'^1/pois/?$',
        'working_waterfronts.working_waterfronts_api.views.poi.poi_list',
        name='pois-list'),
    url(r'^1/pois/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.poi.poi_details',
        name='poi-details'),
    url(r'^1/pois/products/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.poi.pois_products',
        name='pois-products'),

    url(r'^1/preparations/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.preparation.preparation_details',
        name='preparation-details'),

    url(r'^1/locations/?$',
        'working_waterfronts.working_waterfronts_api.views.location.locations',
        name='locations'),

    url(r'^entry/pois/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.pois.poi',
        name='new-poi'),

    url(r'^entry/pois/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.pois.poi',
        name='edit-poi'),

    url(r'^entry/pois/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.pois.poi_list',
        name='list-pois-edit'),

    url(r'^entry/products/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.products.product',
        name='edit-product'),

    url(r'^entry/products/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.products.product',
        name='new-product'),

    url(r'^entry/products/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.products.product_list',
        name='entry-list-products'),

    url(r'^entry/stories/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.stories.story',
        name='edit-story'),

    url(r'^entry/stories/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.stories.story',
        name='new-story'),

    url(r'^entry/stories/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.stories.story_list',
        name='entry-list-stories'),

    url(r'^entry/preparations/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.preparations.preparation',
        name='new-preparation'),

    url(r'^entry/preparations/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.preparations.preparation',
        name='edit-preparation'),

    url(r'^entry/preparations/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.preparations.prep_list',
        name='entry-list-preparations'),

    url(r'^entry/images/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.images.image',
        name='edit-image'),

    url(r'^entry/images/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.images.image_list',
        name='entry-list-images'),

    url(r'^entry/images/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.images.image',
        name='new-image'),

    url(r'^entry/videos/(?P<id>\d+)/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.videos.video',
        name='edit-video'),

    url(r'^entry/videos/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.videos.video_list',
        name='entry-list-videos'),

    url(r'^entry/videos/new/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.videos.video',
        name='new-video'),

    url(r'^login/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.login.login_user',
        name='login'),

    url(r'^logout/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.login.logout_user',
        name='logout'),

    url(r'^/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.login.root',
        name='root'),

    url(r'^entry/?$',
        'working_waterfronts.working_waterfronts_api.views.entry.home.home',
        name='home'),

)
