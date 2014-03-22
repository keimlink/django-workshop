Authentifizierung & Registrierung
*********************************

.. todo:: Translate chapter

Aus verschiedenen Gründen ist eine Authentifizierung im Frontend sinnvoll. Zum
Beispiel sollen Benutzer selbst Inhalte erstellen, Lesezeichen anlegen oder
Bewertungen abgeben können.

Django stellt in ``django.contrib.auth`` eine Applikation zur
Authentifizierung zur Verfügung. Diese wird zum Beispiel auch im Admin
eingesetzt.

Eine weitere Applikation erstellen
==================================

Da ``django.contrib.auth`` etwas erweitert werden muss erstellen wir zuerst
eine eigene Applikation mit dem Namen ``userauth``:

..  code-block:: bash

    $ python manage.py startapp userauth

Projekt konfigurieren
=====================

Nun müssen wir das Projekt so konfigurieren, dass unsere neue Applikation auch
benutzt wird. Dazu erweiterst du zuerst die Datei :file:`settings.py`::

    INSTALLED_APPS = (
        ...
        'userauth',
    )

    LOGIN_URL = 'userauth_login'
    LOGOUT_URL = 'userauth_logout'
    LOGIN_REDIRECT_URL = '/'

Die drei neuen Konfigurationswerte haben folgende Aufgaben:

* ``LOGIN_URL``: Dieser URL wird aufgerufen, wenn ein Login erforderlich ist
* ``LOGOUT_URL``: Das Gegenstück zu ``LOGIN_URL``
* ``LOGIN_REDIRECT_URL``: Wenn nach einem erfolgreichen Login kein URL
  angegeben wurde wird zu diesem URL weitergeleitet

Außerdem können wir schon die URLs einbinden, die wir später für unsere neue
Applikation erzeugen werden. Dazu erweiterst du die Datei :file:`urls.py` im
Konfigurationsverzeichnis nach dem Eintrag für den Admin um folgende Zeile::

    url(r'^benutzer/', include('userauth.urls')),

Authentifizierung mit der Applikation ``userauth``
==================================================

URLConf erstellen
-----------------

Nun erstellen wir die Datei :file:`urls.py` im Verzeichnis :file:`userauth`::

    from django.conf.urls import patterns, include, url

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

Sie enthält die URLs für Login und Logout sowie zum Ändern des Passworts.
Dabei werden die Views aus ``django.contrib.auth.views`` benutzt. Sie werden
aber mit eigenen Templates gerendert.

.. _toggle_login:

Templates anlegen
-----------------

Für die Formulare werden wir die Django App `django-crispy-forms
<http://django-crispy-forms.readthedocs.org/en/latest/>`_ nutzen. Sie
kann einfach mit Hilfe von :program:`pip` installiert werden:

::

    $ pip install django-crispy-forms

Außerdem müssen wir ``crispy_forms`` zu den ``INSTALLED_APPS``
hinzufügen sowie konfigurieren, dass wir Bootstrap 3 benutzen:

::

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

Als nächstes Erstellen wir ein Template für das Login in
:file:`userauth/templates/userauth/login.html`:

..  code-block:: html+django

    {% extends "base.html" %}
    {% load crispy_forms_tags %}

    {% block title %}{{ block.super }} - Login{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
        <form action="{% url 'userauth_login' %}" method="post" accept-charset="utf-8">
            {{ form|crispy }}
            {% csrf_token %}
            <input type="hidden" name="next" value="{{ next }}" />
            <input type="submit" value="Login"/>
        </form>
    {% endblock %}

Neu ist hier das Formular. Für Formulare in Django muss man die ``<form>``
Tags und den Button zum Abschicken selbst definieren.

Der View ``django.contrib.auth.views.login`` liefert ein Formular als
``form``. Dieses kann man dann mit ``form.as_p`` rendern. Zusätzlich muss der
Token zum Schutz gegen einen `Cross-Site Request Forgery (CRSF)
<http://de.wikipedia.org/wiki/Cross-Site_Request_Forgery>`_ eingebunden
werden.

Im versteckten Feld ``next`` kann man einen URL angeben, der nach dem
erfolgreichen Login aufgerufen wird.

Das zweite Template :file:`password_change_form.html` dient dem Ändern das
Passwortes. Erstelle es ebenfalls im Verzeichnis
:file:`userauth/templates/userauth/`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Passwort ändern{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <form action="{% url 'userauth_password_change' %}" method="post" accept-charset="utf-8">
        {{ form.as_p }}
        {% csrf_token %}
        <input type="submit" value="Passwort ändern"/>
    </form>
    {% endblock %}

Das dritte Template wird nach dem erfolgreichen Ändern des Passworts
angezeigt. Wie in der URLConf angegeben ist sein Name
:file:`password_change_done.html`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Passwort erfolgreich geändert{% endblock %}

    {% block content %}
    <p>Dein Passwort wurde erfolgreich geändert.</p>
    {% endblock %}

Außerdem erstellen wir noch ein Template, um überall Login vzw. Logout
anzuzeigen. Dieses Template erstellst du in
:file:`userauth/templates/userauth/toggle_login.html`:

..  code-block:: html+django

    {% if user.is_authenticated %}
    <ul class="nav pull-right">
        <li class="dropdown">
            <a class="dropdown-toggle" id="dropuser" data-toggle="dropdown" href="#">{{ user.username }}</a>
            <ul class="dropdown-menu" role="menu" aria-labelledby="dropuser">
                <li><a href="{% url "userauth_password_change" %}">Passwort ändern</a></li>
                <li><a href="{% url "userauth_logout" %}">Logout</a></li>
            </ul>
        </li>
    </ul>
    {% else %}
    <form class="navbar-form pull-right" action="{% url "userauth_login" %}" method="post" accept-charset="utf-8">
        <input class="span2" type="text" placeholder="Username" name="username">
        <input class="span2" type="password" placeholder="Password" name="password">
        {% csrf_token %}
        <button type="submit" class="btn">Login</button>
    </form>
    {% endif %}

Das Basis-Template erweitern
----------------------------

Im Template :file:`cookbook/templates/base.html` ist in der Navigation
ursprünglich das folgende Login Formular enthalten:

.. code-block:: html

    <form class="navbar-form pull-right">
        <input class="span2" type="text" placeholder="Email">
        <input class="span2" type="password" placeholder="Password">
        <button type="submit" class="btn">Sign in</button>
    </form>

Dieses ersetzt du mit einem Block, in dem mit Hilfe des ``include`` Tags
das eben erstellte Template :file:`userauth/templates/userauth/toggle_login.html`
geladen wird:

..  code-block:: html+django

    {% block toggle_login %}
        {% include "userauth/toggle_login.html" %}
    {% endblock %}

.. _request_context_vorstellung:

``RequestContext`` auch hier nötig
----------------------------------

Damit im Kontext des Response-Objekts auch die nötigen Informationen wie das
User Objekt oder der ``csrf_token`` zur Verfügung stehen, muss der
``RequestContext`` an die Rendering-Funktion übergeben werden. Dies haben wir
schon beim der :ref:`staticfiles` gemacht. Also ist hier nichts weiter zu tun.

Authentifizierung testen
========================

Das war der erste Teil. Du solltest nun die Authentifizierung im Frontend
benutzen können.

Registrierung mit der Applikation ``userauth``
==============================================

Natürlich sollen die Besucher im Frontend auch neue Benutzer erstellen können.
Deshalb fügen wir jetzt noch eine Registrierung hinzu.

URLConf erweitern
-----------------

Zuerst wird die URLConf in :file:`userauth/urls.py` um zwei URLs erweitert::

    from django.views.generic import TemplateView

    urlpatterns += patterns('',
        url(r'^registrieren/$', 'userauth.views.register',
            {'next_page_name': 'userauth_register_done'},
            name='userauth_register'),
        url(r'^willkommen/$',
            TemplateView.as_view(template_name='userauth/register_done.html'),
            name='userauth_register_done')
    )

Der zweite URL ``userauth_register_done`` benutzt den generischen View
``django.views.generic.TemplateView`` (:djangodocs:`Dokumentation
<topics/class-based-views/#simple-usage-in-your-urlconf>`), da wir hier einfach
nur das Template ohne weitere Daten rendern wollen.

Ein View für das Formular
-------------------------

Jetzt muss der View für den ersten URL ``userauth_register`` geschrieben
werden. Dazu öffnest du die Datei :file:`userauth/views.py` und erstellst die
folgende Funktion::

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

``django.contrib.auth.forms`` stellt das Formular ``UserCreationForm`` zur
Verfügung, das wir benutzen, um einen neuen Benutzer zu erstellen. Der View
regelt nur noch die Verarbeitung der Daten. Das Argument ``next_page`` bietet
die Möglichkeit nach dem Anlegen des Benutzer zu einer beliebigen Seite
weiterzuleiten.

Templates anlegen und erweitern
-------------------------------

Natürlich brauchen beide URLs noch ein Template.

Zuerst erstellst du in :file:`userauth/templates/userauth/register.html` ein
Template für das Formular:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Registrieren{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <form action="{% url 'userauth_register' %}" method="post" accept-charset="utf-8">
        {{ form.as_p }}
        {% csrf_token %}
        <input type="submit" value="registrieren"/>
    </form>
    {% endblock %}

Da wir auf der Registrierungsseite kein Login anzeigen möchten überschreiben
wir den Block ``toggle_login`` einfach mit einem leeren Block.

Außerdem benötigen wir noch das Template, das nach dem erfolgreichen Erstellen
des Benutzers angezeigt wird (:file:`register_done.html`):

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Erfolgreich registriert{% endblock %}

    {% block content %}
    <p>Du hast dich registriert. Viel Spass mit dem Kochbuch!</p>
    {% endblock %}

Damit es auch einen Link zum Registrierungsformular gibt fügen wir noch eine
Zeile mit dem Link zum Registrierungsformular in das Template
:file:`toggle_login.html` ein:

..  code-block:: html+django

    {% if user.is_authenticated %}
        ...
    {% else %}
        <p><a href="{% url 'userauth_login' %}">Login</a>
        <a href="{% url 'userauth_register' %}">Registrieren</a></p>
    {% endif %}

Registrieren testen
-------------------

Nun kannst du auch die Registrierung im Frontend testen.

Django Apps für Authentifizierung und Registrierung
===================================================

Natürlich gibt es auch Open Source Django Apps, die Lösungen für
Authentifizierung und Registrierung anbieten. Die bekannteste und
wahrscheinlich meist genutzte ist django-registration_. Eine neuere, aber sehr
interessante App ist django-userena_.

.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/wiki/Home
.. _django-userena: http://docs.django-userena.org/

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Authentifizierung mit Django <topics/auth/>`
