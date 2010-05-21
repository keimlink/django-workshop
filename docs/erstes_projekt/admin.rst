Der Admin
*********

Als nächstes werden wir den Admin aktivieren, damit wir Daten für unser Projekt eingeben, bearbeiten und löschen können.

Der Admin ist eine Applikation, die schon in Django enthalten ist.

Die Applikation beim Admin registrieren
=======================================

Damit der Admin mit unser Applikation benutzt werden kann, müssen wir unsere Models dem Admin bekannt machen.

Dazu muss die Datei ``admin.py`` in der Applikation angelegt werden. Danach öffnest du die Datei in deinem Editor und fügst die beiden folgenden Zeilen Code ein::

    from django.contrib import admin
    
    from recipes.models import Category, Recipe

Damit stehen dir der Admin und die Models der Applikation zur Verfügung.

Als nächstes erstellen wir eine Klasse, um das Model ``Category`` beim Admin zu registrieren::

    class CategoryAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['name']}
    
    
    admin.site.register(Category, CategoryAdmin)

Mehr ist nicht zu tun.

Das Attribut ``prepopulated_fields`` hilft im Admin dabei, dass Feld ``slug`` bei der Eingabe automatisch zu füllen.

Das gleiche tun wir jetzt für das Model ``Recipe``::

    class RecipeAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['title']}
    
    
    admin.site.register(Recipe, RecipeAdmin)

Die vollständige Datei
----------------------

Die Datei ``admin.py`` sollte nun so aussehen::

    from django.contrib import admin
    
    from recipes.models import Category, Recipe
    
    class CategoryAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['name']}


    class RecipeAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ['title']}


    admin.site.register(Category, CategoryAdmin)
    admin.site.register(Recipe, RecipeAdmin)

Den Admin aktivieren
====================

Um den Admin zu aktivieren sind zwei Schritte nötig.

Anpassen der Konfiguration
--------------------------

Entferne in der Datei ``settings.py`` in ``INSTALLED_APPS`` das Kommentarzeichen vor der Zeile ``'django.contrib.admin',``, um den Admin zu aktivieren.

URLConf anpassen
----------------

Damit der Admin auch im Browser aufgerufen werden kann müssen wir die URL des Admins ebenfalls aktivieren.

Öffne dazu die Datei ``cookbook/urls.py`` und entferne die Kommentarzeichen in den Zeilen 4, 5 und 16. Danach sieht die Datei so aus::

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
    )

Weiterführende Links zur Django Dokumentation
=============================================

    * `Informationen zum Admin <http://docs.djangoproject.com/en/1.2/ref/contrib/admin/#ref-contrib-admin>`_
