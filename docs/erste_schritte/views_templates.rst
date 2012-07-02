Die ersten Views
****************

Nachdem du nun einige Datensätze mit Hilfe der Admins-Applikation angelegt
hast ist der nächste Schritt, diese auch im Frontend anzuzeigen. Dazu musst du
drei Dinge tun:

    #. URLs definieren
    #. Views schreiben
    #. Templates erstellen

..  note::

    Siehe :ref:`Grafik: Schematische Darstellung einer Request / Response
    Verarbeitung <grafik_request_response>`

URLs definieren
===============

Zuerst definieren wir die URLs, die zum Abruf der verschiedenen Views dienen
sollen. Fürs Erste wollen wir zwei URLs anlegen. Öffne dazu die Datei
:file:`urls.py` und füge am Ende der ``urlpatterns`` die folgenden beiden
Zeilen ein::

    url(r'^rezept/(?P<slug>[-\w]+)/$', 'recipes.views.detail'),
    url(r'^$', 'recipes.views.index'),

Die Datei :file:`urls.py` sieht danach so aus::

    from django.conf.urls import patterns, include, url

    # Uncomment the next two lines to enable the admin:
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'cookbook.views.home', name='home'),
        # url(r'^cookbook/', include('cookbook.foo.urls')),

        # Uncomment the admin/doc line below to enable admin documentation:
        # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'recipes.views.detail'),
        url(r'^$', 'recipes.views.index'),
    )

..  note::

    Das erste Argument der ``url`` Funktion ist ein `Raw-String
    <http://docs.python.org/reference/lexical_analysis.html#string-literals>`_,
    der einen regulären Ausdruck enthält.

    Falls du regulären Ausdrücken zum ersten Mal begegnest kannst du mehr
    darüber auf Regular-Expressions.info_ oder im Artikel von Doug Hellmann
    über das re-Modul_ erfahren. Auf RegexPlanet_ kannst du reguläre Ausdrücke
    direkt im Browser testen.

.. _Regular-Expressions.info: http://www.regular-expressions.info/
.. _re-Modul: http://www.doughellmann.com/PyMOTW/re/
.. _RegexPlanet: http://www.regexplanet.com/advanced/python/index.html

Nun startest du den Entwicklungs-Webserver:

..  code-block:: bash

    $ python manage.py runserver
    Validating models...
    0 errors found

    Django version 1.4, using settings 'cookbook.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Der Aufruf der URL http://127.0.0.1:8000/ zeigt eine ``ViewDoesNotExist``
Exception. Das ist auch richtig so, denn bis jetzt hast du ja noch keinen View
geschrieben. Es zeigt aber, dass dein URL funktioniert.

Wie wird ein Template gerendert?
================================

Bevor wir die ersten Views schreiben wollen wir uns ansehen wie Django
Templates gerendert werden.

Django Templates sind einfache Python Objekte, deren Konstruktor einen String
erwartet. Mit Hilfe eines Context Objekts werden dann die Platzhalter im
Template durch die gewünschten Werte ersetzt.

Das erste Beispiel zeigt wie man ein Dictionary als Datenstruktur nutzen
kann::

    $ python manage.py shell

.. note::

    Der Befehl :program:`shell` lädt die Einstellungen aus :file:`settings.py`
    für das aktuelle Projekt, was beim Start durch die Eingabe von
    :program:`python` nicht passieren würde.

::

    >>> from django.template import Context, Template
    >>> t = Template('Mein Name ist {{ person.first_name }}.')
    >>> d = {'person': {'first_name': 'Andi'}}
    >>> t.render(Context(d))
    u'Mein Name ist Andi.'

Im zweiten Beispiel nutzen wir ein einfaches Python Objekt als Datenstruktur::

    >>> class Person: pass
    ...
    >>> p = Person()
    >>> p.first_name = 'Klara'
    >>> c = Context({'person': p})
    >>> t.render(c)
    u'Mein Name ist Klara.'

Listen können ebenfalls genutzt werden::

    >>> t = Template('Erster Artikel: {{ articles.0 }}')
    >>> c = Context({'articles': ['Brot', 'Eier', 'Milch']})
    >>> t.render(c)
    u'Erster Artikel: Brot'

Den ersten View schreiben
=========================

Also müssen nun die Views erstellt werden. Sie sollen die Daten, die angezeigt
werden sollen, mit Hilfe des ORMs aus der Datenbank holen.

Dazu öffnest du die Datei :file:`views.py` in der Applikation ``recipes``, die
durch das Kommando :command:`startapp recipes` angelegt wurde.

Die meisten Views geben ein ``HttpResponse`` Objekt zurück. Also schreiben wir
einen ganz einfachen View, der dies tut::

    from django.http import HttpResponse


    def index(request):
        return HttpResponse('Mein erster View.')

Nachdem du den View gespeichert hast rufst du http://127.0.0.1:8000/ auf und
wirst den String sehen, den du dem ``HttpResponse`` Objekt übergeben hast. Ein
``HttpResponse`` erwartet also immer einen String.

Nun werden wir statt des Strings ein ``Template`` laden und dieses mit einem
``Context`` rendern, der ein ``Recipe`` Objekt enthält. Der ``HttpResponse``
wird dann den vom ``Template`` gerenderten String zurück geben::

    from django.http import HttpResponse
    from django.template import Context, loader

    from .models import Recipe


    def index(request):
        recipes = Recipe.objects.all()
        t = loader.get_template('recipes/index.html')
        c = Context({'object_list': recipes})
        return HttpResponse(t.render(c))

Wenn du nun http://127.0.0.1:8000/ aufrufst wird eine ``TemplateDoesNotExist``
Exception ausgelöst. Klar - du hast das geladene Template auch noch nicht
erstellt.

Templates erstellen
===================

Als erstes benötigst du ein Basis-Template für deine Website. Erstelle das
Verzeichnis :file:`templates` im Projektverzeichnis. Das ist das Verzeichnis
:file:`cookbook` mit der Datei :file:`manage.py` darin. Im neuen Verzeichnis
erstellt du die Datei :file:`base.html`:

..  code-block:: html+django

    <!doctype html>
    <head>
        <meta charset="utf-8">
    	<title>{% block title %}Kochbuch{% endblock %}</title>
    </head>
    <body>
        <h1>Kochbuch</h1>
        {% block content %}{% endblock %}
    </body>
    </html>

Sie enthält HTML und zwei **Blöcke**. Diese werden von den anderen Templates
gefüllt, die von diesem Template ableiten.

Innerhalb der Applikation musst du auch zwei Verzeichnisse für die Templates
anlegen, nämlich :file:`recipes/templates/recipes`. Darin erstellt du die
Datei :file:`index.html`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Alle Rezepte{% endblock %}

    {% block content %}
    <h2>Alle Rezepte</h2>
    <ul>
        {% for recipe in object_list %}
        <li><a href="/rezept/{{ recipe.slug }}/">{{ recipe.title }}</a></li>
        {% endfor %}
    </ul>
    {% endblock %}

Jetzt sollte deine Verzeichnisstruktur wie folgt aussehen:

..  code-block:: bash

    cookbook
    |-- cookbook
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    |-- cookbook.db
    |-- manage.py
    |-- recipes
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- fixtures
    |   |   `-- initial_data.json
    |   |-- models.py
    |   |-- templates
    |   |   `-- recipes
    |   |       `-- index.html
    |   |-- tests.py
    |   `-- views.py
    `-- templates
        `-- base.html

Nachdem du den Entwicklungs-Webserver neu gestartet hast solltest du nun eine
Liste aller Rezepte sehen, wenn du http://127.0.0.1:8000/ aufrufst.

Den zweiten View hinzufügen
===========================

Damit auch die Detailansicht der Rezepte funktioniert, muss ein zweiter View
geschrieben werden.

Als erstes muss ein zusätzlicher Import an den Beginn der Datei
:file:`views.py`::

    from django.http import Http404

An das Ende kommt eine neue Methode für den neuen View::

    def detail(request, slug):
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

    from .models import Recipe


    def index(request):
        recipes = Recipe.objects.all()
        t = loader.get_template('recipes/index.html')
        c = Context({'object_list': recipes})
        return HttpResponse(t.render(c))


    def detail(request, slug):
        try:
            recipe = Recipe.objects.get(slug=slug)
        except Recipe.DoesNotExist:
            raise Http404
        t = loader.get_template('recipes/detail.html')
        c = Context({'object': recipe})
        return HttpResponse(t.render(c))

Ein zweites Template erstellen
==============================

Nun fehlt nur noch das zweite Template :file:`recipes/detail.html`. Lege es im
gleichen Verzeichnis wie auch :file:`recipes/index.html` an:

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

Jetzt kannst du auch alle Rezepte ansehen, indem du auf die Links auf der
Startseite klickst.

Warum versteckt die Template Engine Variablen, die nicht existieren?
====================================================================

Wenn eine Variable nicht als Schlüssel im Context definiert wurde, wird diese
im Template von der Django Template Engine ignoriert. Dies ist vor allem im
Produktivbetrieb sinnvoll, da so die Seite trotz einer fehlenden Variable noch
gerendert werden kann.

Um trotzdem zu sehen, ob eine Variable nicht gerendert wurde, kann man in der
Konfiguration :file:`settings.py` eine Zeichenkette definieren, die in diesem
Fall ausgegeben wird::

    TEMPLATE_STRING_IF_INVALID = 'TEMPLATE NAME ERROR'

Diese Einstellung sollte im Produktivbetrieb aber wieder deaktiviert werden.

Maskierung von HTML und JavaScript
==================================

Aus Sicherheitsgründen maskiert die Django Template Engine alles HTML und
JavaScript, dass sich im Context befindet. Nehmen wir an, ein Benutzer schreibt in das
Feld "Zubereitung" seines Rezepts folgenden Text::

    <script>alert('Das beste Rezept der Welt!')</script>
    Das Wasser im Topf auf 100°C erhitzen.

Dann würde dieses HTML erzeugt::

    <p>&lt;script&gt;alert(&#39;Das beste Rezept der <Welt!&#39;)&lt;/script&gt;</p>
    <p>Das Wasser im Topf auf 100°C erhitzen.</p>

Der JavaScript Code würde also nicht ausgeführt werden.

Es ist auch möglch, HTML Tags komplett zu entfernen. Dazu müsstest du im
Template zusätzlich den ``striptags`` Filter einsetzen:

..  code-block:: html+django

    {% block content %}
    <h2>{{ object.title }}</h2>
    <p>Ergibt {{ object.number_of_portions }} Portionen.</p>
    <h3>Zutaten</h3>
    {{ object.ingredients|linebreaks }}
    <h3>Zubereitung</h3>
    {{ object.preparation|striptags|linebreaks }}
    <p>Zubereitungszeit: {{ object.time_for_preparation }} Minuten</p>
    {% endblock %}

Jetzt sieht das HTML so aus::

    <p>alert(&#39;Das beste Rezept der Welt!&#39;)</p>
    <p>Das Wasser im Topf auf 100°C erhitzen.</p>

Bist du dir dagegen sicher, dass HTML oder JavaScript gerendet und ggf.
ausgeführt werden soll, kannst du den ``safe`` Filter benutzen, um dies
explizit zu erlauben:

..  code-block:: html+django

    {% block content %}
    <h2>{{ object.title }}</h2>
    <p>Ergibt {{ object.number_of_portions }} Portionen.</p>
    <h3>Zutaten</h3>
    {{ object.ingredients|linebreaks }}
    <h3>Zubereitung</h3>
    {{ object.preparation|safe|linebreaks }}
    <p>Zubereitungszeit: {{ object.time_for_preparation }} Minuten</p>
    {% endblock %}

Jetzt wird tatsächlich das JavaScript wie vom Benutzer gewüscht ausgeführt::

    <p><script>alert('Das beste Rezept der Welt!')</script></p>
    <p>Das Wasser im Topf auf 100°C erhitzen.</p>

.. note::

    Dies ermögicht natürlich XSS-Angriffe_ und sollte deshalb mit größter
    Vorsicht eingesetzt werden.

.. _XSS-Angriffe: https://de.wikipedia.org/wiki/Cross-Site-Scripting

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Der URL dispatcher <topics/http/urls/#topics-http-urls>`
* :djangodocs:`Views schreiben <topics/http/views/#topics-http-views>`
* :djangodocs:`Templates und deren Vererbung <topics/templates/#topics-templates>`
* :djangodocs:`Automatische Maskierung von HTML und JavaScript <topics/templates/#automatic-html-escaping>`
* :djangodocs:`Django Templates für Python Programmierer <ref/templates/api/>`
