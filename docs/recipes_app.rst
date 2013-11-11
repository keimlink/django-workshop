The first Django App
********************

Now we start with the first Django application for our project "cookbook".

This is how the data model looks like:

.. graphviz:: recipes_models.dot
    :alt: An entity–relationship model of the recipes application
    :inline:

- The name of the app is *recipes*
- It has two models: *Recipe* und *Category*
- The *id* field will be created automatically as primary key by the Django ORM
- Both models are connected by the n-m relation *category*
- *Recipe.author* is connected to the *User* model provided by Django's auth app

Create the app
==============

Because the application will manage recipes we will call it
:file:`recipes`::

    $ cd cookbook
    $ python manage.py startapp recipes

This command will create a directory :file:`recipes` containing these
four files::

    recipes
    |-- __init__.py
    |-- models.py
    |-- tests.py
    `-- views.py

Create the Models
=================

Now open the file :file:`models.py` in a text editor. It contains only a single
``import``:

.. code-block:: python

    from django.db import models

To prevent problems with the encoding add the following line before the
``import``::

    # encoding: utf-8


A Model for the categories
--------------------------

Now start with the model for the categories:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 1, 3, 5-11

The next step is to extend the class ``Category``:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 13-18

A Model for the recipes
-----------------------

Let's start with the second model for the recipes:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 21-22, 31-45

We habe to add another ``import`` for the ``User`` class:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 2

Add some constants for the ``difficulty`` field at the top of the class:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 23-30

Again we have to add a ``Meta`` class and a ``__unicode__``  method
for the ``Recipe`` class:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 47-53

Because we want to populate the date fields automatically we have to
overload the ``save`` method:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 55-59

At the end of the ``save`` method we call the `super
<http://docs.python.org/library/functions.html#super>`_ function to call
the parent method.

Finally we have to add the ``now`` function at the top of the file:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :lines: 4

..  note::

    :pep:`8`, the `Python documentation
    <http://docs.python.org/reference/simple_stmts.html#import>`_ and
    this `short article <http://effbot.org/zone/import-confusion.htm>`_
    provide more information about the ``import`` statement.

The complete file
=================

When everything is complete, the file :file:`models.py` should look as
follows:

.. literalinclude:: ../src/cookbook/recipes/models.py
    :linenos:

Activating the app
==================

Open the file :file:`settings.py` and add the name of our new
application at the end of the ``INSTALLED_APPS`` setting.

Now ``INSTALLED_APPS`` looks like this:

.. literalinclude:: ../src/cookbook/cookbook/settings.py
    :lines: 121-133

Further links to the Django documentation
=========================================

- :djangodocs:`Django Models <topics/db/models/>`
- :djangodocs:`Model field reference <ref/models/fields/>`
- :djangodocs:`Model Meta options <ref/models/options/>`
