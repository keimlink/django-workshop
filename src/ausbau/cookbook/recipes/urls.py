from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('recipes.views',
    url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
    url(r'^$', 'index', name='recipes_recipe_index'),
)

urlpatterns += patterns('',
    url(r'^registrieren/$', 'userauth.views.register',
        {'next_page_name': 'userauth_register_done'},
        name='userauth_register'),
    url(r'^willkommen/$',
        TemplateView.as_view(template_name='userauth/register_done.html'),
        name='userauth_register_done')
)
