******************
RESTful Webservice
******************

Often other applications want to access the data of the Django project.
There has to be a `RESTful web service
<http://en.wikipedia.org/wiki/Representational_state_transfer>`_ to do
so. A possible way to implement such a web service is to use `Tastypie
<http://tastypieapi.org/>`_.

Installation
============

The first step is to install the Python Packages ::

    $ pip install django-tastypie

.. note::

     Tastypie needed some more Python packages, which are automatically
     installed. In order to use such features as the XML serializer,
     YAML serializer or useing a authentication APIKEY, more Python
     packages need to be manually installed.

Then you add ``tastypie`` to the ``INSTALLED_APPS``

.. literalinclude:: ../src/cookbook_rest_api/cookbook/settings.py
    :lines: 121-134
    :emphasize-lines: 13

As a last step you have to generate the necessary database structures::

    $ python manage.py migrate tastypie
    Syncing...
    Creating tables ...
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)
    Migrating...
    Running migrations for tastypie:
     - Migrating forwards to 0001_initial.
     > tastypie:0001_initial
     - Loading initial data for tastypie.
    Installed 0 object(s) from 0 fixture(s)

    Synced:
     > django.contrib.auth
     > django.contrib.contenttypes
     > django.contrib.sessions
     > django.contrib.sites
     > django.contrib.messages
     > django.contrib.staticfiles
     > django.contrib.admin
     > django.contrib.admindocs
     > debug_toolbar
     > south
     > userauth
     > addressbook

    Migrated:
     - tastypie
     - recipes
     - news

Create a resource
=================

A RESTful web service provides available resources. So you have to put
these in the shape of ``Resource`` classes. For this purpose, you create
the file :file:`recipes/api.py`

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 5-9, 21, 24-26


Now you have to bind the ``RecipeResource`` to a URL in the
:file:`cookbook / urls.py`::

    from recipes.api import RecipeResource

    recipe_resource = RecipeResource()

    # other url patterns...

    urlpatterns += patterns('',
        # Andere url Definitionen...
        url(r'^api/', include(recipe_resource.urls)),
    )

You can now access various resources:

* a list of all recipes: http://127.0.0.1:8000/api/recipe/?format=json
* a single recipe: http://127.0.0.1:8000/api/recipe/1/?format=json
* a group of recipes: http://127.0.0.1:8000/api/recipe/set/1;3/?format=json
* the pattern of the resource: http://127.0.0.1:8000/api/recipe/schema/?format=json

In order to work more easily in the browser with the API, we recommend
to the install one or more extensions:

* `JSONView <http://jsonview.com/>`_ (für Chrome und Firefox)
* `cREST Client <https://chrome.google.com/webstore/detail/crest-client/baedhhmoaooldchehjhlpppaieoglhml>`_ (für Chrome)
* `Poster <https://addons.mozilla.org/en-US/firefox/addon/poster/>`_ (für Firefox)

Of course, you also can use `cURL <http://curl.haxx.se/>`_ on the
commandline type.

Currently you have read only access to the resources (GET). Creating
(POST), updating (PUT), and deleting (DELETE) of resources is not
allowed.::

    $ curl -IX DELETE http://127.0.0.1:8000/api/recipe/1/
    HTTP/1.0 401 UNAUTHORIZED
    Date: Sat, 13 Oct 2012 11:22:43 GMT
    Server: WSGIServer/0.1 Python/2.6.6
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

As you can see, the result of a DELETE request is "401 UNAUTHORIZED ".
For security reasons, there is only read access. Write access must be
activated.

Extend authorization
====================

To perform POST / PUT / DELETE operations, you need to extend the
authorization of the resource

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 3, 5-6, 7-9, 21, 24-27


.. warning::

    Such a configured authorization allows EVERYONE to perform ALL
    OPERATIONS! Therefore, this configuration is only suitable for the
    development environment and need to be extended for production.

Change resources via PUT
========================

Now it is possible to update resource with PUT. Here I am reading a
record via GET with the cREST client. You can see that the attribute
``is_active`` has the value ``true``.

.. image:: /images/cREST_Client_GET.png


First I copy the JSON data from the response of the GET request above.
Then I set the HTTP method to PUT and copy the JSON data in the field
"Request Entity" and change ``is_active`` to ``false``. Then I activate
the HTTP headers and set the header to ``Content-Type: application /
json``. As a last step I will send a Request and so change the record.

.. image:: /images/cREST_Client_PUT.png

After I sent this request I call the record again with GET. The value of
the attribute ``is_active`` has to be changed to ``false``.

.. image:: /images/cREST_Client_GET_after_PUT.png

Adding another resource
=======================

Currently, only the recipes and not the associated user is visible. You
can change this by enabling a new resource for the user in
:file:`recipes / api.py`

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 1-3, 5-13, 19-27

Now you just have to integrate this new resource into the URLconf.

.. literalinclude:: ../src/cookbook_rest_api/cookbook/urls.py
    :lines: 1-34
    :emphasize-lines: 8-14, 33

Now there are more data available than previously and in addition we
have the API versioned:

* http://127.0.0.1:8000/api/v1/?format=json
* http://127.0.0.1:8000/api/v1/recipe/?format=json
* http://127.0.0.1:8000/api/v1/recipe/1/?format=json
* http://127.0.0.1:8000/api/v1/recipe/set/1;3/?format=json
* http://127.0.0.1:8000/api/v1/recipe/schema/?format=json
* http://127.0.0.1:8000/api/v1/user/?format=json
* http://127.0.0.1:8000/api/v1/user/1/?format=json
* http://127.0.0.1:8000/api/v1/user/schema/?format=json

However, we now have a new problem, because in the ``User`` Resource
also contain sensitive data such as passwords.

Restrict access
===============

So we have to restrict the access. There are two possibilities.

#. Exclude the unwanted fields

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 10-14

#. Only specify the fields that are allowed::

    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            fields = ['username', 'first_name', 'last_name', 'last_login']

In addition, we only want to allow read access to the ``User`` resource

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 10-15

filter ressources
=================

With some additional configuration, it is also possible to filter
resources

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :emphasize-lines: 16-18, 28-32

Now following queries are possible:

* http://127.0.0.1:8000/api/v1/recipe/?format=json&title__startswith=k
* http://127.0.0.1:8000/api/v1/recipe/?format=json&title__icontains=ei
* http://127.0.0.1:8000/api/v1/recipe/?format=json&number_of_portions__gt=3
* http://127.0.0.1:8000/api/v1/recipe/?format=json&author__username=admin

Further links to the Django documentation
=========================================

* `Tastypie Dokumentation <http://django-tastypie.readthedocs.org/>`_
