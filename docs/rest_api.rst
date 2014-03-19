*******************
RESTful Web Service
*******************

Often other applications want to access the data of a Django project.
Therefore it makes sense to use a `RESTful web service
<http://en.wikipedia.org/wiki/Representational_state_transfer>`_. One
way to implement such a web service offers `Tastypie
<http://tastypieapi.org/>`_.

Installation
============

The first step is to install the Python package::

    $ pip install django-tastypie

.. note::

     Tastypie requires some more Python packages, which are
     automatically installed. To take advantage of features such as the
     XML serializer, YAML serializer or the ApiKey authentication,
     additional Python packages must be installed manually.

After that you add ``tastypie`` to the ``INSTALLED_APPS``:

.. literalinclude:: ../src/cookbook_rest_api/cookbook/settings.py
    :lines: 121-134
    :emphasize-lines: 13

As a last step you have to generate the necessary database structures:

::

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

Creating a resource
===================

A RESTful web service publishes resources. So you put them in the form
of ``Resource`` classes. For this purpose, you create the file
:file:`recipes/api.py`:

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 5-9, 21, 24-26

.. todo:: Add :file:`recipes/urls.py`

Now you have to bind the ``RecipeResource`` to a URL in
:file:`cookbook/urls.py`:

::

    from recipes.api import RecipeResource

    recipe_resource = RecipeResource()

    # other urlpatterns...

    urlpatterns += patterns('',
        # other urls...
        url(r'^api/', include(recipe_resource.urls)),
    )

You can now access various resources:

* a list of all recipes: http://127.0.0.1:8000/api/recipe/?format=json
* a single recipe: http://127.0.0.1:8000/api/recipe/1/?format=json
* a group of recipes: http://127.0.0.1:8000/api/recipe/set/1;3/?format=json
* the schema of the resource: http://127.0.0.1:8000/api/recipe/schema/?format=json

In order to work more easily in the browser with the API, the
installation of one or more extensions is recommended:

* `JSONView <http://jsonview.com/>`_ (für Chrome und Firefox)
* `cREST Client <https://chrome.google.com/webstore/detail/crest-client/baedhhmoaooldchehjhlpppaieoglhml>`_ (für Chrome)
* `Poster <https://addons.mozilla.org/en-US/firefox/addon/poster/>`_ (für Firefox)

Of course, you can also use `cURL <http://curl.haxx.se/>`_ on the
commandline.

Currently you have read only access to the resources (GET). Creating
(POST), updating (PUT) and deleting (DELETE) of resources is not
allowed:

::

    $ curl -IX DELETE http://127.0.0.1:8000/api/recipe/1/
    HTTP/1.0 401 UNAUTHORIZED
    Date: Sat, 13 Oct 2012 11:22:43 GMT
    Server: WSGIServer/0.1 Python/2.6.6
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

As you can see, the result of a DELETE request is "401 UNAUTHORIZED".
For security reasons only read access is allowed. Write access must be
activated.

Extend authorization
====================

To perform POST/PUT/DELETE operations, you need to extend the
authorization of the resource:

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 3, 5-6, 7-9, 21, 24-27

.. warning::

    An authorization that is configured this way allows EVERYONE to
    perform ALL OPERATIONS! Therefore, this configuration is only
    suitable for the development environment and needs to be extended
    for production.

Change resources via PUT
========================

Now it is possible to update resource with PUT. Here a record is read
via GET using the cREST client. You can see that the attribute
``is_active`` has the value ``true``.

.. image:: /images/cREST_Client_GET.png

First the JSON data is copied from the response of the GET request
above. Then the HTTP method is set to PUT and the JSON data is copied in
the field "Request Entity" and ``is_active`` is changed to ``false``.
Then the HTTP headers are activated and the header is set to ``Content-
Type: application/json``. As a last step the request is sent to change
the record.

.. image:: /images/cREST_Client_PUT.png

After this request is sent the record is loaded again using GET and the
value of the attribute ``is_active`` has been changed to ``false``.

.. image:: /images/cREST_Client_GET_after_PUT.png

Adding another resource
=======================

Currently, only the recipes and not the associated user is visible. You
can change this by enabling a new resource for the user in
:file:`recipes/api.py`:

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 1-3, 5-13, 19-27

Now you just have to integrate this new resource into the URLconf:

.. literalinclude:: ../src/cookbook_rest_api/cookbook/urls.py
    :lines: 1-34
    :emphasize-lines: 8-14, 33

Afterwards there is more data available than previously and in addition
we have the API versioned:

* http://127.0.0.1:8000/api/v1/?format=json
* http://127.0.0.1:8000/api/v1/recipe/?format=json
* http://127.0.0.1:8000/api/v1/recipe/1/?format=json
* http://127.0.0.1:8000/api/v1/recipe/set/1;3/?format=json
* http://127.0.0.1:8000/api/v1/recipe/schema/?format=json
* http://127.0.0.1:8000/api/v1/user/?format=json
* http://127.0.0.1:8000/api/v1/user/1/?format=json
* http://127.0.0.1:8000/api/v1/user/schema/?format=json

However, we now have a new problem, because in the ``User`` resource
also contains sensitive data such as the password.

Restrict access
===============

So we have to restrict the access. There are two possibilities:

1. Exclude the unwanted fields

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 10-14

2. Only specify the fields that are allowed::

    class UserResource(ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            fields = ['username', 'first_name', 'last_name', 'last_login']

In addition, we only want to allow read access to the ``User`` resource:

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :lines: 10-15

Filter ressources
=================

With some additional configuration, it is also possible to filter
resources:

.. literalinclude:: ../src/cookbook_rest_api/recipes/api.py
    :emphasize-lines: 16-18, 28-32

Now following queries are possible:

* http://127.0.0.1:8000/api/v1/recipe/?format=json&title__startswith=k
* http://127.0.0.1:8000/api/v1/recipe/?format=json&title__icontains=ei
* http://127.0.0.1:8000/api/v1/recipe/?format=json&number_of_portions__gt=3
* http://127.0.0.1:8000/api/v1/recipe/?format=json&author__username=admin

Further links
=============

* `Tastypie Documentation <http://django-tastypie.readthedocs.org/>`_
