********************
A new Django Project
********************

.. index:: Project structure, startproject

Start the Django Project
========================

You can create a new Django project with the following command::

    $ django-admin.py startproject cookbook

After you've run the command you'll find the following structure::

    cookbook
    |-- cookbook
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    `-- manage.py

.. index:: Development server, runserver

Test the Development Server
===========================

After you've created the project, you can change to the directory
:file:`cookbook`::

    $ cd cookbook

And try out the development server with the following command:

.. literalinclude:: runserver.log

Now you can open the "Welcome to Django" site from
http://127.0.0.1:8000/.  After you've opened the site, you can kill the
development server with :kbd:`CTRL + C`.

.. image:: /images/welcome_to_django.jpg
    :alt: Welcome to Django
    :align: center

.. index:: Configuration

Configuration
=============

In order to work with the project, you need to configure it. To do that,
open the file :file:`settings.py` in a text editor.

So that you don't need to enter the project directory several times in
the configuration, you can save it in a "constant". This constant can
then be used everywhere where the project directory is required.

.. literalinclude:: ../src/cookbook/cookbook/settings.py
    :lines: 2-4

.. note::

    It is important that the constant is defined at the very beginning
    of the configuration file.

.. doctest::
    :hide:

    >>> settings.BASE_DIR.endswith('/cookbook')
    True

Next the database needs to be configured. We'll use `SQLite
<http://www.sqlite.org/>`_, as it's built into Python.

Configure the existing database connection ``default`` as follows by
editing the emphasized lines:

.. literalinclude:: ../src/cookbook/cookbook/settings.py
    :lines: 15-25
    :emphasize-lines: 3-4

.. doctest::
    :hide:

    >>> settings.DATABASES['default']['ENGINE'].endswith('sqlite3')
    True
    >>> settings.DATABASES['default']['NAME'].startswith(settings.BASE_DIR)
    True

Next change the timezone and language to suit:

.. literalinclude:: ../src/cookbook/cookbook/settings.py
    :lines: 31-39

.. doctest::
    :hide:

    >>> settings.TIME_ZONE == 'Europe/Berlin'
    True
    >>> settings.LANGUAGE_CODE == 'en-us'
    True

The constant ``LANGUAGE_CODE`` configures the language of the Admin
inferface which we will use later to English. You can change it to a
different language, e.g. use ``de`` as ``LANGUAGE_CODE`` if you want
to use German.

Lastly, the paths to static files and templates must be defined. Add the
emphasized lines to the already existing constants. You can find them
further below the configuration file:

.. literalinclude:: ../src/cookbook/cookbook/settings.py
    :lines: 73-80, 114-119
    :emphasize-lines: 6, 13

.. doctest::
    :hide:

    >>> settings.STATICFILES_DIRS[0].startswith(settings.BASE_DIR)
    True
    >>> settings.STATICFILES_DIRS[0].endswith('static')
    True
    >>> settings.TEMPLATE_DIRS[0].startswith(settings.BASE_DIR)
    True
    >>> settings.TEMPLATE_DIRS[0].endswith('templates')
    True

Now create the directory for static files and templates under directory
:file:`cookbook`::

    $ mkdir static templates

Afterwards the directory structure should look as follows::

    cookbook
    |-- cookbook
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    |-- manage.py
    |-- static
    `-- templates

Further links to the Django documentation
=========================================

- :djangodocs:`Django settings <topics/settings/>`
- :djangodocs:`Full list of Django settings <ref/settings/>`
