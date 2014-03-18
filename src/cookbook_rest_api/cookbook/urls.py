from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from recipes.api import RecipeResource, UserResource

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RecipeResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cookbook.views.home', name='home'),
    # url(r'^cookbook/', include('cookbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recipe/(?P<slug>[-\w]+)/$', 'recipes.views.detail'),
    url(r'^$', 'recipes.views.index'),
)


urlpatterns += patterns('',
    url(r'^api/', include(v1_api.urls)),
)

if settings.DEBUG:
    # for development only: serve media files
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
