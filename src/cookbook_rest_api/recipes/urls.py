from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .api import RecipeResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RecipeResource())

urlpatterns = patterns('recipes.views',
    url(r'^recipe/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
    url(r'^$', 'index', name='recipes_recipe_index'),
)

urlpatterns += patterns('',
    url(r'^api/', include(v1_api.urls)),
)
