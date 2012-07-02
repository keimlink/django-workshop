Eine Suche mit AJAX
*******************

Die Wikipedia_ erklärt AJAX wie folgt:

    "Ajax ist ein Apronym für die Wortfolge „Asynchronous JavaScript and
    XML“. Es bezeichnet ein Konzept der asynchronen Datenübertragung
    zwischen einem Browser und dem Server."

Moderne Web Applikationen nutzen oft AJAX, um den Benutzern eine bessere
User Experience zu bieten. Denn AJAX ermöglicht es einzelne Teile des
DOMs der Seite auszutauschen, ohne dabei die Seite komplett neu zu
laden.

Da bei der Implementierung die Eigenarten der verschiedenen Browser
berücksichtigt werden müssen ist es sinnvoll ein JavaScript-Framework
wie zum Beispiel jQuery_ einzusetzen, dass sich um diese Unterschiede
kümmert. Das :ref:`HTML5 Boilerplate <html5_boilerplate>` enthält
bereits jQuery, wir müssen diese Bibliothek also nicht mehr
installieren.

.. _Wikipedia: https://de.wikipedia.org/wiki/Ajax_(Programmierung)
.. _jQuery: http://jquery.com/

Ein View, der JSON generiert
============================

Wir wollen in diesem Kapitel eine kleine Suche bauen. Es soll ein
Eingabefeld geben, in das man den Suchbegriff eintippt. Dabei sollen,
nachdem der zweite Buchstabe eingegeben wurde, Rezept-Titel vom Server
gelesen und unterhalb des Eingabefelds ausgegeben werden. Dazu benötigen
wir zuerst einen View, der das JSON erzeugt, dass im Browser als Liste
der Vorschläge dienen soll.

Der Pfad der URLs, die an den Server gesendet werden, um eine Liste von
Rezept-Titeln zu holen, sieht so aus::

    /autocomplete/?term=ko

Zuerst fügen wir also eine entsprechende neue URL für den View
`autocomplete` in :file:`recipes/urls.py` ein::

    urlpatterns = patterns('recipes.views',
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
        url(r'^autocomplete/$', 'autocomplete', name='recipes_recipe_autocomplete'),
        url(r'^$', 'index', name='recipes_recipe_index'),
    )

Dann schreiben wir den passenden View in :file:`recipes/views.py`, der
den GET Parameter `term` zur Suche benutzt::

    def autocomplete(request):
        term = request.GET.get('term', '')
        recipes = Recipe.objects.filter(title__startswith=term).order_by('title')
        titles = []
        for recipe in recipes:
            titles.append(recipe.title)
        json = simplejson.dumps(titles, ensure_ascii=False)
        return HttpResponse(json, mimetype='application/json')

Ein zweiter View für die Suche
==============================

Außerdem benötigen wir noch einen zweiten View, der die Suche dann
durchführt und die Ergebnisse anzeigt. Dieser soll folgenden URL-Pfad
benutzen::

    /suche/?begriff=ko

Der URL für den View `search` in :file:`recipes/urls.py`::

    urlpatterns = patterns('recipes.views',
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
        url(r'^autocomplete/$', 'autocomplete', name='recipes_recipe_autocomplete'),
        url(r'^suche/$', 'search', name='recipes_recipe_search'),
        url(r'^$', 'index', name='recipes_recipe_index'),
    )

Und der entsprechende View::

    def search(request):
        query = request.GET.get('begriff', '')
        results = Recipe.objects.filter(title__startswith=query).order_by('title')
        return render(request, 'recipes/search.html', {'results': results})

Da dieser View ein Template rendert, benötigt er auch eine
Template-Datei, nämlich :file:`recipes/templates/recipes/search.html`:

.. code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Suche{% endblock %}

    {% block content %}
    <h2>Suchergebnisse</h2>
    <ul>
        {% for recipe in results %}
          <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
        {% empty %}
          <li>Keine Rezepte gefunden.</li>
        {% endfor %}
    </ul>
    {% endblock %}

jQuery im Frontend einsetzen
============================

Allerdings benötigen wir für die Darstellung im Browser auch jQueryUI_,
das wir noch installieren müssen. Dazu die Version 1.8.x auf der
`jQueryUI Website herunterladen`_. Das "x" in der Version ist immer
durch die letzte Nummer des aktuellen Release zu ersetzen.

.. note::

    Wenn du jQueryUI klein halten möchtest, reicht es nur die
    Komponenten *Core*, *Widget*, *Position* und *Autocomplete*
    für den Download auszuwählen.

Nachdem du das Zip-Archiv herunterladen hast entpackst du es. Danach
hast du ein Verzeichnis das :file:`jquery-ui-1.8.x.custom` oder
:file:`jquery-ui-1.8.x` heißt, je nachdem ob du jQueryUI vor dem
Download angepasst hast oder nicht. Dann kopierst du die nötigen
Dateien in das Verzeichnis :file:`cookbook/static`:

- das Verzeichnis :file:`ui-lightness` aus dem Verzeichnis :file:`jquery-ui-1.8.x.custom/css` in das Verzeichnis :file:`static/css`
- die Datei :file:`jquery-ui-1.8.x.custom.min` aus dem Verzeichnis :file:`jquery-ui-1.8.x.custom/js` in das Verzeichnis :file:`static/js/libs`

Alle weiteren Arbeiten werden am Template :file:`base.html` durchgeführt.

Zuerst binden wir das neue CSS und JavaScript von jQueryUI im Template ein:

.. code-block:: html+django

    <head>
    ...
      <link rel="stylesheet" href="{{ STATIC_URL }}css/ui-lightness/jquery-ui-1.8.x.custom.css">
    ...
    </head>

.. code-block:: html+django

      </footer>
      <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
      <script>window.jQuery || document.write('<script src="{{ STATIC_URL }}js/libs/jquery-1.7.1.min.js"><\/script>')</script>
      <script src="{{ STATIC_URL }}js/libs/jquery-ui-1.8.21.custom.min.js"></script>
      ...
    </body>

Dann folgt das Suchformular:

.. code-block:: html+django

      <div role="main">
        <form action="{% url recipes_recipe_search %}">
          <div class="ui-widget">
            <label for="search">Suche: </label>
            <input id="search" name="begriff" />
          </div>
        </form>
        {% block content %}{% endblock %}
      </div>

Als letztes erstellen wir den JavaScript-Code, der die Anfrage zur
Autovervollständigung an den Server senden wird:

.. code-block:: html+django

      ...
      <script>
        $(function() {
          $("#search").autocomplete({
            source: "/autocomplete/",
            minLength: 2
          });
        });
      </script>
    </body>

.. _jQueryUI: http://jqueryui.com/
.. _jQueryUI Website herunterladen: http://jqueryui.com/download

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Django Objekte serialisieren <topics/serialization/>`
* :djangodocs:`Das HttpResponse Objekt <ref/request-response/#django.http.HttpResponse>`
