from django.conf.urls.defaults import *

urlpatterns = patterns('recipes.views',
    url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
    url(r'^erstellen/$', 'add', name='recipes_recipe_add'),
    url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),
    url(r'^$', 'index', name='recipes_recipe_index'),
)
