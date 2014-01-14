.. _multiple_databases:

******************
Multiple Databases
******************

Since Django 1.2 you can work with several databases simultaneously.

At first we add the new database ``newsdb`` to the database
configuration in :file:`local_settings.py`:

.. literalinclude:: ../src/cookbook_multi_db/cookbook/local_settings.py
    :lines: 10-23,28

Eine neue App "news" erstellen
==============================

This database will be used by a app called "news". It should have the
following data model:

.. graphviz:: news.dot

- A model **Article** which inherits from an abstract model **DateTimeInfo**
- The abstract model saves both datetime fields automatically

So we create at first the new app::

    $ python manage.py startapp news

The next step is the creation of the abstract model. We put the file
:file:`basemodels.py` with the following contents into the configuration
directory:

.. literalinclude:: ../src/cookbook_multi_db/cookbook/basemodels.py
    :linenos:

Then we create the model ``Article`` in :file:`news/models.py`:

.. literalinclude:: ../src/cookbook_multi_db/news/models.py
    :linenos:

Now we need an :file:`admin.py` file to use the model with the admin:

.. literalinclude:: ../src/cookbook_multi_db/news/admin.py
    :linenos:

Create the ``CookbookRouter`` router
====================================

In order we can use the new database with the app "news", we need a
"database router". We place this in the file :file:`router.py` in the
configuration directory:

..  literalinclude:: ../src/cookbook_multi_db/cookbook/router.py
    :lines: 1-6, 9-13, 16-20, 23-
    :linenos:

After that we have to configure the ``DATABASE_ROUTERS`` in :file:`settings.py`::

    DATABASE_ROUTERS = ['cookbook.router.CookbookRouter']

We also have to activate the new app "news" in ``INSTALLED_APPS``.

Perform the initial Migration
=============================

At first we create a new schemamigration for the model ``Article``::

    $ python manage.py schemamigration news --initial
    Creating migrations directory at '.../cookbook/news/migrations'...
    Creating __init__.py in '.../cookbook/news/migrations'...
     + Added model news.Article
    Created 0001_initial.py. You can now apply this migration with: ./manage.py migrate news

Since the database ``newsdb`` still is new, we must once create the
tables for South::

    $ python manage.py syncdb --noinput --database=newsdb
    Syncing...
    Creating tables ...
    Creating table south_migrationhistory
    Installing custom SQL ...
    Installing indexes ...
    No fixtures found.

    Synced:
     > django.contrib.auth
     > django.contrib.contenttypes
     > django.contrib.sessions
     > django.contrib.sites
     > django.contrib.messages
     > django.contrib.staticfiles
     > django.contrib.admin
     > debug_toolbar
     > userauth
     > south

    Not synced (use migrations):
     - recipes
     - news
    (use ./manage.py migrate to migrate these)

It looks as if there are more tables created. This is not the case,
because the ``CookbookRouter`` suppresses the creation of the tables. We
can also examine that::

    $ python manage.py dbshell --database=newsdb
    SQLite version 3.7.6.3
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> .tables
    south_migrationhistory

Now we perform the first migration::

    $ python manage.py migrate news --database=newsdb
    Running migrations for news:
     - Migrating forwards to 0001_initial.
     > news:0001_initial
     - Loading initial data for news.
    No fixtures found.

Then we can start the development web server and create several articles
in the new news app.

Integrate an existing database
==============================

Since Django 1.2, it is also possible to integrate an existing database in Django. For this we need to create such at first. I have written a
Python script that fills a SQLite database with addresses:

..  literalinclude:: ../src/cookbook_multi_db/sqltestdata.py
    :linenos:

If you call the script from the command line, the generated SQL
queries are issued:

.. command-output:: python sqltestdata.py
    :cwd: ../src/cookbook_multi_db

You can determine the number of addresses generated with an argument::

    $ python sqltestdata.py 200

First, however, has the database connection in :file:`local_settings.py`
to be created:

.. literalinclude:: ../src/cookbook_multi_db/cookbook/local_settings.py
    :lines: 10-28

Now we can run the queries with the new database::

    $ python sqltestdata.py 2000 | python manage.py dbshell --database=addressdb

And look at the data::

    $ python manage.py dbshell --database=addressdb
    SQLite version 3.7.6.3
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> .tables
    address  city
    sqlite> select * from address join city on city_id = city.id limit 10;
    1|Andrea|Schulze|Alte Straße 73|64831|5|5|Bremen
    2|Malte|Schulze|Neuer Ring 35|87214|5|5|Bremen
    3|Maria|Hirsch|Hauptstraße 78|68412|5|5|Bremen
    4|Malte|Weiland|Brunnengasse 70|48076|2|2|Dresden
    5|Andrea|Drescher|Am Markt 35|91046|1|1|Berlin
    6|Maria|Drescher|Hauptstraße 13|08457|6|6|Stuttgart
    7|Peter|Drescher|Hauptstraße 67|69318|3|3|Hamburg
    8|Maria|Drescher|Alte Straße 89|87126|4|4|Bonn
    9|Maria|Hirsch|Hauptstraße 25|41359|4|4|Bonn
    10|Maria|Meier|Neuer Ring 17|95746|1|1|Berlin

Next, we create an app for the new database::

    $ python manage.py startapp addressbook

And let Django create the models from the tables in the database using
the command :program:`inspectdb`::

    $ python manage.py inspectdb --database=addressdb
    # This is an auto-generated Django model module.
    # You'll have to do the following manually to clean this up:
    #     * Rearrange models' order
    #     * Make sure each model has one field with primary_key=True
    # Feel free to rename the models, but don't rename db_table values or field names.
    #
    # Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
    # into your database.

    from django.db import models

    class Address(models.Model):
        id = models.IntegerField(primary_key=True)
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        street = models.CharField(max_length=255)
        zipcode = models.CharField(max_length=5)
        city = models.ForeignKey(City)
        class Meta:
            db_table = u'address'

    class City(models.Model):
        id = models.IntegerField(primary_key=True)
        name = models.CharField(max_length=255)
        class Meta:
            db_table = u'city'

This we then write to the file :file:`addressbook/models.py`::

    $ python manage.py inspectdb --database=addressdb > addressbook/models.py

In order for the models to work, we adapt it a little (lines 5, 10, 14,
16-17, 21, 23, 26, 28-29):

..  literalinclude:: ../src/cookbook_multi_db/addressbook/models.py
    :emphasize-lines: 5, 10, 14, 16-17, 21, 23, 26, 28-29
    :linenos:

And we need to extend the ``CookbookRouter`` (lines 7-8, 14-15, 21-22):

..  literalinclude:: ../src/cookbook_multi_db/cookbook/router.py
    :emphasize-lines: 7-8, 14-15, 21-22
    :linenos:

Now we just need the file :file:`addressbook/admin.py` to display the data
in the admin. We enable search and filter, show more fields in
the list and make all fields in the form read only:

..  literalinclude:: ../src/cookbook_multi_db/addressbook/admin.py
    :linenos:

Finally, we activate the app ``addressbook`` in ``INSTALLED_APPS`` in
the in :file:`settings.py` and then start the development web server to
view the data.

Further links to the Django documentation
=========================================

* :djangodocs:`Abstract base classes <topics/db/models/#abstract-base-classes>`
* :djangodocs:`Multiple databases <topics/db/multi-db/>`
