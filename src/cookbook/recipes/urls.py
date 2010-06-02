from django.conf.urls.defaults import *

urlpatterns = patterns('recipes.views',
    url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
    url(r'^$', 'index', name='recipes_recipe_index'),
)
