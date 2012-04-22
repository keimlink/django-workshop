from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^anmelden/$', 'login', {'template_name': 'userauth/login.html'},
        name='userauth_login'),
    url(r'^abmelden/$', 'logout', {'next_page': '/'},
        name='userauth_logout'),
    url(r'^passwort-aendern/$', 'password_change',
        {'template_name': 'userauth/password_change_form.html'},
        name='userauth_password_change'),
    url(r'^passwort-geaendert/$', 'password_change_done',
        {'template_name': 'userauth/password_change_done.html'},
        name='userauth_password_change_done')
)
