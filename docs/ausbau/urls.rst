Vereinfachen und Entkoppeln der URLConf
***************************************

Im Moment werden alle URLs in der :file:`urls.py` im Hauptverzeichnis des
Projekts definiert. Das wird auf Dauer unübersichtlich und verletzt außerdem
das :ref:`dry`-Prinzip. Jede Applikation sollte seine URLs selbst bestimmen.

Eine URLConf für die ``recipes`` Applikation
============================================

Also legen wir in der Applikation :file:`recipes` eine leere Datei
:file:`urls.py` an. Sie soll die URLs der Rezepte aufnehmen::

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('recipes.views',
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail'),
        url(r'^$', 'index'),
    )

Das erste Argument der Funktion ``patterns``, dass bis jetzt nur ein leerer
String war, können wir nun verwenden. Es ist ein Prefix für alle Views, die in
diesem Funktionsaufruf definiert werden. Deshalb müssen wir nur noch den
eigentlichen Namen der View-Funktion angeben.

Die beiden URLs übernehmen wir ansonsten aus der URLConf des Projekts.

Die URLConf des Projekts vereinfachen
=====================================

Wir können also nun die beiden URLs für die :file:`recipes` Applikation aus
der URLConf des Projekts entfernen. Statt dessen müssen wir die neue URLConf
der Applikation einem URL zuweisen::

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
        url(r'^', include('recipes.urls')),
    )

Diese Konfiguration kannst du jetzt testen. Das Frontend sollte wie gewohnt
funktionieren.

URLs zentral definieren
=======================

Nun sind die URLs aus der URLConf des Projekts in die Applikation verschoben
worden, was zu mehr Übersichtlichkeit geführt hat. Aber es gibt immer noch
Teile der Applikation, die ihre URLs selbst definieren.

Im Template :file:`recipes/templates/recipes/index.html` wird der Link zum
Rezept manuell definiert. Es kann also passieren, dass URL im Template nicht
mit dem in der URLConf der Applikation übereinstimmt. Das werden wir ändern.

URLConf der Applikation erweitern
---------------------------------

Als erstes geben wir den URLs in der URLConf der Applikation Namen::

    urlpatterns = patterns('recipes.views',
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
        url(r'^$', 'index', name='recipes_recipe_index'),
    )

Die Funktion ``url`` akzeptiert ein Argument ``name``, um dem URL einen Namen
zu geben. Im Regelfall wird dieser nach dem Schema APPLIKATION_MODEL_VIEW
vergeben. So kann ein Name nicht doppelt auftreten.

Eine neue Methode für das Model
-------------------------------

Das Model ``Recipe`` bekommt als nächstes eine neue Methode, damit jede
Instanz ihren URL selbst erzeugen kann. Dafür ist die Methode
``get_absolute_url`` reserviert::

    @models.permalink
    def get_absolute_url(self):
        return ('recipes_recipe_detail', (), {'slug': self.slug})

Der Dekorator ``models.permalink`` erwartet einen Tupel mit drei Werten:

* Name der URL
* Argumente (Variablen im regulären Ausdruck des URL, die keinen Namen
  bekommen haben)
* Schlüsselwort-Argumente (Variablen im regulären Ausdruck des URL mit Namen)

Der Dekorator erstellt dann den URL und gibt diesen als String zurück.

..  note::

    Mehr zum Thema Dekoratoren kannst du im :pep:`318` nachlesen.

Templates anpassen
------------------

Zuletzt müssen die Templates an die neue Methode angepasst werden. Im Template
:file:`recipes/templates/recipes/index.html` wird der alte Aufruf

..  code-block:: html+django

    <li><a href="/rezept/{{ recipe.slug }}">{{ recipe.title }}</a></li>

durch einen neuen ersetzt

..  code-block:: html+django

    <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>

Im Template :file:`recipes/templates/recipes/detail.html` fügen wir einen Link
zur Übersicht ein:

..  code-block:: html+django

    <a href="{% url recipes_recipe_index %}">zurück zur Übersicht</a>

So können alle URLs zentral in der URLConf verwaltet werden.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`permalink() Dokumentation <ref/models/instances/#django.db.models.permalink>`
* :djangodocs:`URLs mit Namen versehen <topics/http/urls/#id2>`
