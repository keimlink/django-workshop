from django.conf.urls import patterns, include, url

urlpatterns = patterns('recipes.views',
    url(r'^recipe/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
    url(r'^$', 'index', name='recipes_recipe_index'),
)
