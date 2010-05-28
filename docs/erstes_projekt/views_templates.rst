Die ersten Views
****************

Nachdem du nun einige Datensätze mit Hilfe des Admins angelegt hast ist der nächste Schritt, diese auch im Frontend anzuzeigen. Dazu musst du drei Dinge tun:

    #. URLs definieren
    #. Views schreiben
    #. Templates erstellen

..  note::

    Siehe :ref:`Grafik: Schematische Darstellung einer Request / Response Verarbeitung <grafik_request_response>`

URLs definieren
===============

Zuerst definieren wir die URLs, die zum Abruf der verschiedenen Views dienen sollen. Fürs Erste wollen wir zwei URLs anlegen. Öffne dazu die Datei ``urls.py`` und füge am Ende der ``urlpatterns`` die folgenden beiden Zeilen ein::

    (r'^rezept/(?P<slug>[-\w]+)/$', 'recipes.views.detail'),
    (r'^$', 'recipes.views.index'),

Die Datei ``urls.py`` sieht danach so aus::

    from django.conf.urls.defaults import *

    # Uncomment the next two lines to enable the admin:
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        # Example:
        # (r'^cookbook/', include('cookbook.foo.urls')),

        # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
        # to INSTALLED_APPS to enable admin documentation:
        # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        (r'^admin/', include(admin.site.urls)),
        (r'^rezept/(?P<slug>[-\w]+)/$', 'recipes.views.detail'),
        (r'^$', 'recipes.views.index'),
    )

Wenn du nun den Entwicklungs-Webserver startest und den URL http://127.0.0.1:8000/ aufrufst siehst du eine ``ViewDoesNotExist`` Exception. Das ist auch richtig so, denn bis jetzt hast du ja noch keinen View geschrieben. Es zeigt aber, dass dein URL funktioniert.

Den ersten View schreiben
=========================

Also müssen nun die Views erstellt werden. Sie sollen die Daten, die angezeigt werden sollen, mit Hilfe des ORMs aus der Datenbank holen.

Dazu öffnest du die Datei ``views.py`` in der Applikation ``recipes``, die durch das Kommando ``startapp recipes`` angelegt wurde.

Der erste View sieht so aus::

    from django.http import HttpResponse
    from django.template import Context, loader

    from recipes.models import Recipe

    def index(request):
        recipes = Recipe.objects.all()
        t = loader.get_template('recipes/index.html')
        c = Context({'object_list': recipes})
        return HttpResponse(t.render(c))

Wenn du nun http://127.0.0.1:8000/ aufrufst bekommst du eine ``TemplateDoesNotExist`` Exception. Klar - du hast das Template auch noch nicht erstellt.

Templates erstellen
===================

Als erstes benötigst du ein Basis-Template für deine Website. Erstelle das Verzeichnis ``templates`` im Projektverzeichnis. Darin erstellt du die Datei ``base.html``:

..  code-block:: html+django

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
    	<title>{% block title %}Kochbuch{% endblock %}</title>
    </head>
    <body>
        <h1>Kochbuch</h1>
        {% block content %}{% endblock %}
    </body>
    </html>

Sie enthält HTML und zwei **Blöcke**. Diese werden von den anderen Templates gefüllt, die von diesem Template ableiten.

Innerhalb der Applikation musst du auch zwei Verzeichnisse für die Templates anlegen, nämlich ``recipes/templates/recipes``. Darin erstellt du die Datei ``index.html``:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Alle Rezepte{% endblock %}

    {% block content %}
    <h2>Alle Rezepte</h2>
    <ul>
        {% for recipe in object_list %}
        <li><a href="/rezept/{{ recipe.slug }}">{{ recipe.title }}</a></li>
        {% endfor %}
    </ul>
    {% endblock %}

Nun solltest du eine Liste aller Rezepte sehen, wenn du http://127.0.0.1:8000/ aufrufst.

Den zweiten View hinzufügen
===========================

Damit auch die Detailansicht der Rezepte funktioniert, muss ein zweiter View geschrieben werden.

Als erstes muss ein zusätzlicher Import an den Beginn der Datei ``views.py``::

    from django.http import Http404

An das Ende kommt eine neue Methode für den neuen View::

    def detail(render, slug):
        try:
            recipe = Recipe.objects.get(slug=slug)
        except Recipe.DoesNotExist:
            raise Http404
        t = loader.get_template('recipes/detail.html')
        c = Context({'object': recipe})
        return HttpResponse(t.render(c))

Die komplette Datei sieht dann so aus::

    from django.http import Http404, HttpResponse
    from django.template import Context, loader

    from recipes.models import Recipe

    def index(request):
        recipes = Recipe.objects.all()
        t = loader.get_template('recipes/index.html')
        c = Context({'object_list': recipes})
        return HttpResponse(t.render(c))

    def detail(render, slug):
        try:
            recipe = Recipe.objects.get(slug=slug)
        except Recipe.DoesNotExist:
            raise Http404
        t = loader.get_template('recipes/detail.html')
        c = Context({'object': recipe})
        return HttpResponse(t.render(c))

Ein zweites Template erstellen
==============================

Nun fehlt nur noch das zweite Template ``recipes/detail.html``. Lege es im gleichen Verzeichnis wie auch ``recipes/index.html`` an:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - {{ object.title }}{% endblock %}

    {% block content %}
    <h2>{{ object.title }}</h2>
    <p>Ergibt {{ object.number_of_portions }} Portionen.</p>
    <h3>Zutaten</h3>
    {{ object.ingredients|linebreaks }}
    <h3>Zubereitung</h3>
    {{ object.preparation|linebreaks }}
    <p>Zubereitungszeit: {{ object.time_for_preparation }} Minuten</p>
    {% endblock %}

Weiterführende Links zur Django Dokumentation
=============================================

    * `Der URL dispatcher <http://docs.djangoproject.com/en/1.2/topics/http/urls/#topics-http-urls>`_
    * `Views schreiben <http://docs.djangoproject.com/en/1.2/topics/http/views/#topics-http-views>`_
    * `Templates und deren Vererbung <http://docs.djangoproject.com/en/1.2/topics/templates/#topics-templates>`_
