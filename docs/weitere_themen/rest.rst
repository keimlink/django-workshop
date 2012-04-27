RESTful Webservice
******************

Oft möchten auch andere Applikationen auf die Daten des Django-Projekts
zugreifen. Dafür bietet es sich an, einen `RESTful Webservice`_ zu nutzen. Eine
Möglichkeit einen solchen Webservice zu implementieren bietet Tastypie_.

.. _RESTful Webservice: https://de.wikipedia.org/wiki/Representational_State_Transfer
.. _Tastypie: http://tastypieapi.org/

Installation
============

Der erste Schritt ist die Installation des Python Packages::

    $ pip install django-tastypie

.. note::

    Tastypie benötigt einige weitere Python Pakete, die es automatisch mit
    installiert. Um Features wie den XML Serializer, YAML Serializer oder die
    ApiKey Authentifizierung zu nutzen müssen weitere Python Pakete manuell
    installiert werden.

Danach fügst du ``tastypie`` zu den ``INSTALLED_APPS`` hinzu::

    INSTALLED_APPS = (
        # Andere Apps...
        'tastypie',
    )

Als letzten Schritt erzeugst du die nötigen Datenbankstrukturen::

    $ python manage.py syncdb
    Creating tables ...
    Creating table tastypie_apiaccess
    Creating table tastypie_apikey
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

Eine Ressource erstellen
========================

Ein RESTful Webservice stellt Ressourcen zur Verfügung. Also legst du diese in
Form von ``Resource`` Klassen an. Dazu erstellst du die Datei
:file:`recipes/api.py`::

    from tastypie.resources import ModelResource

    from .models import Recipe


    class RecipeResource(ModelResource):
        class Meta:
            queryset = Recipe.objects.all()
            resource_name = 'recipe'

Jetzt musst du die ``RecipeResource`` in :file:`recipes/urls.py` an einen URL
binden::

    from django.conf.urls.defaults import patterns, include, url
    # weitere Importe...

    from .api import RecipeResource

    recipe_resource = RecipeResource()

    # Andere urlpatterns...

    urlpatterns += patterns('',
        # Andere url Definitionen...
        url(r'^api/', include(recipe_resource.urls)),
    )

Du kannst nun verschiedene Ressourcen aufrufen:

* eine Liste aller Rezepte: http://127.0.0.1:8000/api/recipe/?format=json
* ein einzelnes Rezept: http://127.0.0.1:8000/api/recipe/1/?format=json
* eine Gruppe von Rezepten: http://127.0.0.1:8000/api/recipe/set/1;3/?format=json
* das Schema der Ressource: http://127.0.0.1:8000/api/recipe/schema/?format=json

Momentan sind nur GET Operationen und keine POST/PUT/DELETE Operationen
erlaubt. Diese enden alle mit einem “401 Unauthorized” Fehler, da aus
Sicherheitsgründen nur lesender Zugriff möglich ist. Schreibende Zugriffe
müssen erst aktiviert werden.

Autorisierung erweitern
=======================

Damit du auch POST/PUT/DELETE Operationen ausführen kannst musst die
Autorisierung der Ressource erweitern::

    from tastypie.authorization import Authorization
    from tastypie.resources import ModelResource

    from .models import Recipe


    class RecipeResource(ModelResource):
        class Meta:
            queryset = Recipe.objects.all()
            resource_name = 'recipe'
            authorization = Authorization()

.. warning::

    Diese Autorisierung erlaubt JEDEM ALLE OPERATIONEN auszuführen. Daher
    eignet sich diese Konfiguration auch nur für die Entwicklungsumgebung und
    muss für den produktiven Betrieb erweitert werden.

Eine weitere Ressource hinzufügen
=================================

Aktuell sind nur die Rezepte und nicht die damit verknüpften Benutzer sichtbar.
Dies änderst du, indem du eine neue Ressource für die Benutzer in
:file:`recipes/api.py` anlegst::

    from django.contrib.auth.models import User
    from tastypie import fields
    from tastypie.authorization import Authorization
    from tastypie.resources import ModelResource

    from .models import Recipe


    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'


    class RecipeResource(ModelResource):
        author = fields.ForeignKey(UserResource, 'author')

        class Meta:
            queryset = Recipe.objects.all()
            resource_name = 'recipe'
            authorization = Authorization()

Jetzt musst du diese neue Ressource noch in der URLConf einbinden::

    from django.conf.urls.defaults import patterns, include, url
    # weitere Importe...
    from tastypie.api import Api

    from .api import RecipeResource, UserResource

    v1_api = Api(api_name='v1')
    v1_api.register(UserResource())
    v1_api.register(RecipeResource())

    # Andere urlpatterns...

    urlpatterns += patterns('',
        # Andere url Definitionen...
        url(r'^api/', include(v1_api.urls)),
    )

Jetzt stehen mehr Daten als vorher zu Verfügung und wir haben die API
zusätzlich versioniert:

* http://127.0.0.1:8000/api/v1/?format=json
* http://127.0.0.1:8000/api/v1/recipe/?format=json
* http://127.0.0.1:8000/api/v1/recipe/1/?format=json
* http://127.0.0.1:8000/api/v1/recipe/set/1;3/?format=json
* http://127.0.0.1:8000/api/v1/recipe/schema/?format=json
* http://127.0.0.1:8000/api/v1/user/?format=json
* http://127.0.0.1:8000/api/v1/user/1/?format=json
* http://127.0.0.1:8000/api/v1/user/schema/?format=json

Allerdings haben wir jetzt ein neues Problem, denn im der ``UserResource``
werden auch sensitive Daten wie Passwörter ausgegeben.

Zugriff beschränken
===================

Also müssen wir den Zugriff beschränken. Dafür gibt es zwei Möglichkeiten.

#. Die nicht erwünschten Felder ausschliessen::

    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']

#. Nur die Felder angeben, die erlaubt sind::

    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            fields = ['username', 'first_name', 'last_name', 'last_login']

Außerdem wollen wir nur einen lesenden Zugriff auf ``UserResource`` erlauben::

    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
            allowed_methods = ['get']

Ressourcen filtern
==================

Mit etwas zusätzlicher Konfiguration ist es auch möglich Ressourcen zu filtern::

    from django.contrib.auth.models import User
    from tastypie import fields
    from tastypie.authorization import Authorization
    from tastypie.constants import ALL, ALL_WITH_RELATIONS
    from tastypie.resources import ModelResource

    from .models import Recipe


    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
            allowed_methods = ['get']
            filtering = {
                'username': ALL,
            }


    class RecipeResource(ModelResource):
        author = fields.ForeignKey(UserResource, 'author')

        class Meta:
            queryset = Recipe.objects.all()
            resource_name = 'recipe'
            authorization = Authorization()
            filtering = {
                'title': ('exact', 'startswith', 'icontains', 'contains'),
                'number_of_portions': ALL,
                'author': ALL_WITH_RELATIONS,
            }

Jetzt sind folgende Abfragen möglich:

* http://127.0.0.1:8000/api/v1/recipe/?format=json&title__startswith=k
* http://127.0.0.1:8000/api/v1/recipe/?format=json&title__icontains=ei
* http://127.0.0.1:8000/api/v1/recipe/?format=json&number_of_portions__gt=3
* http://127.0.0.1:8000/api/v1/recipe/?format=json&author__username=admin

Weiterführende Links zur Tastypie Dokumentation
===============================================

* `Tastypie Dokumentation <http://django-tastypie.readthedocs.org/>`_
