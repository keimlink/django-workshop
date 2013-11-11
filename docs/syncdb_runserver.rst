***********************************
Database and Development Web Server
***********************************

Now we can populate the database and then call the development web
server in order to use the admin application.

Check the Models
================

First, you should check your models with the following command::

    $ python manage.py validate

Django automatically checks the models for all operations that use
models. With this command you can also perform targeted testing.

Synchronize the Database
========================

SQL queries from the models must now be produced, in order to fill the database.

With the following command you can issue the queries:

.. command-output:: python manage.py sqlall recipes
    :cwd: ../src/cookbook

To run these queries directly and create the tables and indexes you need
to run the following command. You will be asked if you would like to
create a superuser. Answer yes and fill out the fields that follow. In
the next step, you can login with these login details.

.. code-block:: text
    :emphasize-lines: 17-23

    $ python manage.py syncdb
    Creating tables ...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table recipes_category
    Creating table recipes_recipe_category
    Creating table recipes_recipe

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (leave blank to use 'vagrant'): admin
    E-mail address: admin@example.com
    Password:
    Password (again):
    Superuser created successfully.
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

Prepare Media Handling
======================

After the database is created you need to do a few additional
preparations to be able to use the web development server. This is
because we used an ``ImageField`` in our ``Recipe`` model which needs
the `Pillow <https://pypi.python.org/pypi/Pillow/2.2.1>`_ package to be
installed.

Linux and Mac OS X
------------------

To prepare for the installation of Pillow under Linux the following
packages must be installed:

- libjpeg62
- liblcms1
- python-dev

For Mac OS X you can, for example, use `Homebrew <http://brew.sh/>`_ to
install the support for the JPG format::

    $ brew install jpeg

Now Pillow can be installed::

    $ pip install Pillow

Windows
-------

Pillow for Windows must be installed as a binary package using ``easy_install``::

    > easy_install Pillow

Set up a media URL
------------------

Finally you need to setup a media URL for development. Add the following
lines at the end of :file:`cookbook/urls.py`:

.. literalinclude:: ../src/cookbook/cookbook/urls.py
    :lines: 2, 19-25

Start the Web Development Server
================================

Now you can start the development server:

.. literalinclude:: runserver.log

Using the URL http://127.0.0.1:8000/admin/ you can now access the admin
application, log in to the super user you just created and add a few
recipes.

Export and Import of Data using JSON
====================================

So you can exchange data between different systems, there are built-in
Django export and import functions. With the command :program:`dumpdata`
you can export the models of the application ``recipes``:

.. code-block:: text

    $ mkdir recipes/fixtures
    $ python manage.py dumpdata --indent 4 recipes > recipes/fixtures/initial_data.json

.. note::

    Django loads the fixtures from a fixture called
    :file:`initial_data.json` every time you execute :program:`syncdb`.
    Therefore the data you just stored will be loaded automatically
    every time you execute :program:`syncdb`.

In addition, you can load the data with the command :program:`loaddata`:

.. code-block:: text

    $ python manage.py loaddata recipes/fixtures/initial_data.json
    Installed 4 object(s) from 1 fixture(s)

.. note::

    To import data from other sources in Django :program:`loaddata` is
    only suitable to a limited extent because the fixtures always define
    the primary keys. There are other apps, such as `CSV importer
    <http://django-csv-importer.readthedocs.org/>`_, that are more
    suitable for the regular import of new data.

Further links to the Django documentation
=========================================

- :djangodocs:`django-admin.py and manage.py <ref/django-admin/>`
- :djangodocs:`Providing initial data for models <howto/initial-data/>`
