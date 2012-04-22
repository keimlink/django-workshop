Die Admin-Applikation
*********************

Als nächstes werden wir die Admin-Applikation aktivieren, damit wir Daten für
unser Projekt eingeben, bearbeiten und löschen können.

Diese Applikation ist schon in Django enthalten.

Die eigene Applikation beim Admin registrieren
==============================================

Damit der Admin mit unser Applikation benutzt werden kann, müssen wir unsere
Models dem Admin bekannt machen.

Dazu muss die Datei :file:`admin.py` in der Applikation angelegt werden. Das
Projekt sieht danach folgendermassen aus:

..  code-block:: bash

    cookbook
    |-- cookbook
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    |-- manage.py
    `-- recipes
        |-- admin.py
        |-- __init__.py
        |-- models.py
        |-- tests.py
        `-- views.py

Danach öffnest du die Datei in deinem Editor und fügst die beiden folgenden
Zeilen Code ein::

    from django.contrib import admin

    from .models import Category, Recipe

Damit stehen dir der Admin und die Models der Applikation zur Verfügung.

Der zweite ``import`` ist ein relativer import. Diese wurden in :pep:`328`
definiert und sind ab Python 2.6 direkt verfügbar. In Python 2.5 müssen sie mit
dem folgenden Code geladen werden::

    from __future__ import absolute_import

Als nächstes erstellen wir eine Klasse, um das Model ``Category`` beim Admin
zu registrieren::

    class CategoryAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['name']}


    admin.site.register(Category, CategoryAdmin)

Mehr ist nicht zu tun.

Das Attribut ``prepopulated_fields`` hilft in der Admin-Applikation dabei,
dass Feld ``slug`` bei der Eingabe automatisch zu füllen. In diesem Fall mit
dem Attribut ``name`` des Models.

Das gleiche tun wir jetzt für das Model ``Recipe``::

    class RecipeAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['title']}


    admin.site.register(Recipe, RecipeAdmin)

Die vollständige Datei
----------------------

Die Datei :file:`admin.py` sollte nun so aussehen::

    from django.contrib import admin

    from .models import Category, Recipe


    class CategoryAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['name']}


    class RecipeAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['title']}


    admin.site.register(Category, CategoryAdmin)
    admin.site.register(Recipe, RecipeAdmin)

Die Admin-Applikation aktivieren
================================

Um die Admin-Applikation zu aktivieren sind zwei Schritte nötig.

Anpassen der Konfiguration
--------------------------

Entferne in der Datei :file:`settings.py` in ``INSTALLED_APPS`` das
Kommentarzeichen vor der Zeile ``'django.contrib.admin',``, um die
Admin-Applikation zu aktivieren.

URLConf anpassen
----------------

Damit die Admin-Applikation auch im Browser aufgerufen werden kann müssen wir
die URL des Admins ebenfalls aktivieren.

Öffne dazu die Datei :file:`cookbook/urls.py` und entferne die
Kommentarzeichen in den Zeilen 4, 5 und 16. Danach sieht die Datei so aus::

    from django.conf.urls.defaults import patterns, include, url

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
    )

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Informationen zur Admin-Applikation <ref/contrib/admin/#ref-contrib-admin>`
