.. _simplify_urls:

**************************************
Simplifying and decoupling the URLconf
**************************************

At the moment, all URLs are defined in :file:`urls.py` in the
configuration directory of the project. This is confusing in the long
run and also violates the :ref:`dry` principle. Each application should
determine their own URLs.

An URLconf for the ``recipes`` application
==========================================

So we put an empty file named :file:`urls.py` inside the application
:file:`recipes`. It should include the URLs of the recipes:

.. code-block:: python

    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^recipe/(?P<slug>[-\w]+)/$', 'recipes.views.detail'),
        url(r'^$', 'recipes.views.index'),
    ]

The two URLs we take from the URLconf of the project.

Simplifing the URLconf of the project
=====================================

Therefore we can now remove the two URLs for the :file:`recipes`
application from the URLconf of the project. Instead, we need to assign
the new URLconf of the application to an URL:

.. literalinclude:: ../src/cookbook_improved/cookbook/urls.py
    :lines: 6-13
    :emphasize-lines: 7
    :language: python

You can now test this configuration, the frontend should work as usual.

Define URLs centrally
=====================

Now the URLs have been moved from the URLconf of the project to the
application, which has led to more clarity. But there are still parts of
the application that define their own URLs.

In the template :file:`recipes/templates/recipes/index.html` the link to
the recipe is defined manually. So it may happen that an URL in the
template does not match with that in the URLconf of the application. We
will change that.

Expand the URLconf of the application
-------------------------------------

First, we give the URLs in the URLconf of the application a name:

.. literalinclude:: ../src/cookbook_improved/recipes/urls.py
    :lines: 3-7

The function ``url`` accepts an argument ``name`` to specify the name of
an URL. Normally, the name is constructed after the APPLICATION_MODEL_VIEW
scheme - this way a name can not occur twice.

A new method for the model
--------------------------

Next the model ``Recipe`` gets a new method to ensure that each instance
can create their own URL. For this is the method ``get_absolute_url``
reserved:

.. literalinclude:: ../src/cookbook_improved/recipes/models.py
    :lines: 62-63

Also the import for ``reverse`` must be added at the top:

.. literalinclude:: ../src/cookbook_improved/recipes/models.py
    :lines: 3

Customize templates
-------------------

Finally, the templates must be adapted to the new method. In the
template :file:`recipes/templates/recipes/index.html` the old call:

.. literalinclude:: ../src/cookbook/recipes/templates/recipes/index.html
    :lines: 9
    :language: html+django

gets replaced by a new one:

.. literalinclude:: ../src/cookbook_improved/recipes/templates/recipes/index.html
    :lines: 9
    :language: html+django

In the template :file:`recipes/templates/recipes/detail.html` we add a
link to the overview:

.. literalinclude:: ../src/cookbook_improved/recipes/templates/recipes/detail.html
    :lines: 12-14
    :emphasize-lines: 2
    :language: html+django

So all URLs can be managed centrally in the URLconf.

Further links to the Django documentation
=========================================

- :djangodocs:`Model.get_absolute_url() <ref/models/instances/#get-absolute-url>`
- :djangodocs:`Naming URL patterns <topics/http/urls/#naming-url-patterns>`
