Authentifizierung & Registrierung
*********************************

Eine weitere Applikation erstellen
==================================

..  code-block:: bash

    $ python manage.py startapp userauth

Projekt konfigurieren
=====================

settings.py::

    INSTALLED_APPS = (
        ...
        'userauth'
    )
    
    LOGIN_URL = '/benutzer/anmelden/'
    LOGOUT_URL = '/benutzer/abmelden/'
    LOGIN_REDIRECT_URL = '/'

urls.py::

    (r'^benutzer/', include('userauth.urls')),

Applikation ``recipes`` erweitern
=================================

recipes/views.py::

    from django.template import RequestContext

``render_to_response`` erweitern.

recipes/views.py::

    from django.template import RequestContext
    from django.shortcuts import get_object_or_404, render_to_response

    from recipes.models import Recipe

    def index(request):
        recipes = Recipe.objects.all()
        return render_to_response('recipes/index.html', {'object_list': recipes},
            context_instance=RequestContext(request))

    def detail(request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        return render_to_response('recipes/detail.html', {'object': recipe},
            context_instance=RequestContext(request))

Authentifizierung mit der Applikation ``userauth``
==================================================

URLConf erstellen
-----------------

userauth/urls.py::

    from django.conf.urls.defaults import *

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

Templates anlegen
-----------------

userauth/templates/userauth/login.html:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Login{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
        <form action="{% url userauth_login %}" method="post" accept-charset="utf-8">
            {{ form.as_p }}
            {% csrf_token %}
            <input type="hidden" name="next" value="{{ next }}" />
            <input type="submit" value="Login"/>
        </form>
    {% endblock %}

userauth/templates/userauth/password_change_form.html:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Passwort ändern{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <form action="{% url userauth_password_change %}" method="post" accept-charset="utf-8">
        {{ form.as_p }}
        {% csrf_token %}
        <input type="submit" value="Passwort ändern"/>
    </form>
    {% endblock %}

userauth/templates/userauth/password_change_done.html:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Passwort erfolgreich geändert{% endblock %}

    {% block content %}
    <p>Dein Passwort wurde erfolgreich geändert.</p>
    <a href="{% url recipes_recipe_index %}">zurück zur Übersicht</a>
    {% endblock %}

userauth/templates/userauth/toggle_login.html:

..  code-block:: html+django

    {% if user.is_authenticated %}
        <p>Hallo {{ user.username }}!
        <a href="{% url userauth_password_change %}">Passwort ändern</a>
        <a href="{% url userauth_logout %}">Logout</a></p>
    {% else %}
        <p><a href="{% url userauth_login %}">Login</a>
    {% endif %}

Das Basis-Template erweitern
----------------------------

templates/base.html:

..  code-block:: html+django

    {% block toggle_login %}
        {% include "auth/toggle_login.html" %}
    {% endblock %}

Authentifizierung testen
------------------------

Test: http://127.0.0.1:8000/

Registrierung mit der Applikation ``userauth``
==============================================

URLConf erweitern
-----------------

userauth/urls.py::

    urlpatterns += patterns('',
        url(r'^registrieren/$', 'userauth.views.register',
            {'next_page_name': 'userauth_register_done'},
            name='userauth_register'),
        url(r'^willkommen/', 'django.views.generic.simple.direct_to_template',
            {'template': 'userauth/register_done.html'},
            name='userauth_register_done')
    )

Ein View für das Formular
-------------------------

userauth/views.py::

    from django.contrib.auth.forms import UserCreationForm
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response
    from django.template import RequestContext

    def register(request, template_name='userauth/register.html', next_page_name=None):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                if next_page_name is None:
                    next_page = '/'
                else:
                    next_page = reverse(next_page_name)
                return HttpResponseRedirect(next_page)
        else:
            form = UserCreationForm()
        return render_to_response(template_name, {'form': form},
            context_instance=RequestContext(request))

Templates anlegen und erweitern
-------------------------------

userauth/templates/userauth/register.html:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Registrieren{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <form action="{% url userauth_register %}" method="post" accept-charset="utf-8">
        {{ form.as_p }}
        {% csrf_token %}
        <input type="submit" value="registrieren"/>
    </form>
    {% endblock %}

userauth/templates/userauth/register_done.html:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Erfolgreich registriert{% endblock %}

    {% block content %}
    <p>Du hast dich registriert. Viel Spass mit dem Kochbuch!</p>
    <a href="{% url recipes_recipe_index %}">zurück zur Übersicht</a>
    {% endblock %}

userauth/templates/userauth/toggle_login.html:

..  code-block:: html+django

    {% if user.is_authenticated %}
        <p>Hallo {{ user.username }}!
        <a href="{% url userauth_password_change %}">Passwort ändern</a>
        <a href="{% url userauth_logout %}">Logout</a></p>
    {% else %}
        <p><a href="{% url userauth_login %}">Login</a>
        <a href="{% url userauth_register %}">Registrieren</a></p>
    {% endif %}

Registrieren testen
-------------------

Test: http://127.0.0.1:8000/

Weiterführende Links zur Django Dokumentation
=============================================

TBD
