***********************************
Database and Development Web Server
***********************************

Now we can populate the database and then call the development web
server in order to use the admin application.

Check the Models
================

First, you should check your models with the following command:

::

    $ python manage.py check
    SystemCheckError: System check identified some issues:

    ERRORS:
    recipes.Recipe.photo: (fields.E210) Cannot use ImageField because Pillow is not installed.
      HINT: Get Pillow at https://pypi.python.org/pypi/Pillow or run command "pip install Pillow".

    System check identified 1 issue (0 silenced).

The :command:`check` command does not only validate the models of all installed
apps but it also performs a lot of others checks on the project. The only error
message you should see explains you that you are using an ``ImageField`` in the
``recipes.Recipe`` model which requires you to install the Pillow package. We
will do this right in the next section.

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
    :lines: 1-11, 14
    :emphasize-lines: 1, 3, 12

Perform another check
---------------------

If you run the :command:`check` command again not errors should occur:

::

    $ python manage.py check
    System check identified no issues (0 silenced).

Migrate the Database
====================

Before you can migrate the database you first have to create the necessary
migration using the :command:`migrate` command:

::

    $ python manage.py makemigrations recipes
    Migrations for 'recipes':
      0001_initial.py:
        - Create model Category
        - Create model Recipe

This will create the file :file:`recipes/migrations/0001_initial.py`. It will
be used to produce the SQL queries from the models, in order to fill the
database. With the following command you can issue the queries:

.. command-output:: python manage.py sqlmigrate recipes 0001
    :cwd: ../src/cookbook

To run these queries directly and create the tables and indexes you need to run
the following command.

::

    $ python manage.py migrate
    Operations to perform:
      Synchronize unmigrated apps: staticfiles, messages
      Apply all migrations: admin, contenttypes, recipes, auth, sessions
    Synchronizing apps without migrations:
      Creating tables...
        Running deferred SQL...
      Installing custom SQL...
    Running migrations:
      Rendering model states... DONE
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying recipes.0001_initial... OK
      Applying sessions.0001_initial... OK

The next command creates a new superuser. Fill out username and password as you
like, the email address is optional. Make sure you remmeber username and
password because in the next step you can login with these details.

::

    $ python manage.py createsuperuser
    Username (leave blank to use 'keimlink'): admin
    Email address:
    Password:
    Password (again):
    Superuser created successfully.

Start the Web Development Server
================================

Now you can start the development server:

.. literalinclude:: runserver.log

Using the URL http://127.0.0.1:8000/admin/ you can now access the admin
application, log in to the superuser you just created and add a few recipes.

Export and Import of Data using JSON
====================================

So you can exchange data between different systems, there are built-in
Django export and import functions. With the command :program:`dumpdata`
you can export the models of the application ``recipes``:

.. code-block:: text

    $ mkdir recipes/fixtures
    $ python manage.py dumpdata --indent 4 recipes > recipes/fixtures/initial_data.json

You can load the data with the command :program:`loaddata`:

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
