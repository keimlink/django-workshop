from django.conf.urls import patterns, include, url


urlpatterns = patterns('recipes.views',
    url(r'^recipe/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
    url(r'^add/$', 'add', name='recipes_recipe_add'),
    url(r'^edit/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),
    url(r'^$', 'index', name='recipes_recipe_index'),
)
