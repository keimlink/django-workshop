.. _mehrere_datenbanken:

Mehrere Datenbanken nutzen
**************************

Seit Django 1.2 kann man mit mehreren Datenbanken gleichzeitig arbeiten.

Dazu tragen wir zuerst die neue Datenbank in die Datei
:file:`local_settings.py` ein::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'cookbook.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
        'newsdb': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'news.db'),
        },
    }

Eine neue App "news" erstellen
==============================

Diese Datenbank soll von einer News App genutzt werden. Sie soll das folgende
Datenmodell haben:

.. graphviz:: news.dot

- Ein Model **Article**, dass von einem abstrakten Model **DateTimeInfo** erbt
- Das abstrakte Model speichert die beiden Felder automatisch

Also erstellen wir als erstes die neue App::

    $ python manage.py startapp news

Der nächste Schritt ist das Anlegen des abstrakten Models. Dazu legen wir im
Konfigurationsverzeichnis die Datei :file:`basemodels.py` mit folgendem Inhalt
an::

    from django.db import models
    from django.utils.timezone import now


    class DateTimeInfo(models.Model):
        date_created = models.DateTimeField(editable=False)
        date_updated = models.DateTimeField(editable=False)

        class Meta:
            abstract = True

        def save(self, *args, **kwargs):
            if not self.id:
                self.date_created = now()
            self.date_updated = now()
            super(DateTimeInfo, self).save(*args, **kwargs)

Danach erstellen wir das Model ``Article`` in der Datei
:file:`news/models.py`::

    # encoding: utf-8
    from django.db import models

    from cookbook.basemodels import DateTimeInfo


    class Article(DateTimeInfo):
        headline = models.CharField(u'Überschrift', max_length=100)
        body = models.TextField(u'Inhalt')

        class Meta:
            verbose_name = u'Artikel'
            verbose_name_plural = u'Artikel'
            ordering = ['-date_updated']

        def __unicode__(self):
            return self.headline

Dadurch, dass das Model ``Article`` von dem Model ``DateTimeInfo`` erbt, erhält
es automatisch die beiden ``DateTimeField`` Felder und deren Verhalten beim
Speichern.

Jetzt brauchen wir noch eine :file:`admin.py`, um das Model im Admin nutzen zu
können::

    from django.contrib import admin

    from .models import Article


    class ArticleAdmin(admin.ModelAdmin):
        list_display = ('headline', 'date_created', 'date_updated')


    admin.site.register(Article, ArticleAdmin)

Die Klasse ``CookbookRouter`` erstellen
=======================================

Damit wir die neue Datenbank auch mit der App "news" nutzen können benötigen
wir einen "database router". Diesen legen wir in der Datei
:file:`router.py` im Konfigurationsverzeichnis an:

..  literalinclude:: ../../src/cookbook/router.py
    :lines: 1-6, 9-13, 16-20, 23-
    :linenos:

Danach müssen wir ``DATABASE_ROUTERS`` in der Datei :file:`settings.py`
konfigurieren::

    DATABASE_ROUTERS = ['cookbook.router.CookbookRouter']

Außerdem aktivieren wir noch die neue App "news" in den ``INSTALLED_APPS``.

Die initiale Migration durchführen
==================================

Da wir im Kapitel :doc:`Migration <migration>` auf South umgestellt haben
nutzen wir zum Erstellen des neue Models ``Article`` nicht mehr den Befehl
:program:`syncdb`, sondern wir erstellen zuerst eine Migration mit dem Kommando
:program:`schemamigration`::

    $ python manage.py schemamigration news --initial
    Creating migrations directory at '.../cookbook/news/migrations'...
    Creating __init__.py in '.../cookbook/news/migrations'...
     + Added model news.Article
    Created 0001_initial.py. You can now apply this migration with: ./manage.py migrate news

Da die Datenbank ``newsdb`` noch neu ist müssen wir einmalig die Tabellen für
South anlegen::

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

Dabei sieht es so aus, als ob noch weitere Tabellen angelegt werden. Das ist
aber nicht der Fall, denn der ``CookbookRouter`` unterbindet das anlegen der
Tabellen. Wir können das auch prüfen::

    $ python manage.py dbshell --database=newsdb
    SQLite version 3.7.6.3
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> .tables
    south_migrationhistory

Jetzt führen wir die erste Migration durch::

    $ python manage.py migrate news --database=newsdb
    Running migrations for news:
     - Migrating forwards to 0001_initial.
     > news:0001_initial
     - Loading initial data for news.
    No fixtures found.

Danach können wir den Entwicklungs-Webserver starten und einige Artikel in der
neuen News App anlegen.

Eine existierende Datenbank einbinden
=====================================

Seit Django 1.2 ist es auch möglich eine existierende Datenbank in Django
einzubinden. Dazu müssen wir zuerst eine solche anlegen. Dafür habe ich ein
Python Skript geschrieben, dass eine SQLite Datenbank mit Adressen füllt:

..  literalinclude:: ../../src/cookbook/sqltestdata.py
    :linenos:

Wenn man das Skript an der Kommandozeile aufruft, werden die erzeugten SQL
Queries ausgegeben::

    $ python sqltestdata.py

Man kann auch mit einem Argument die Anzahl der erzeugten Adressen bestimmen::

    $ python sqltestdata.py 200

Zuerst muss aber die Datenbankverbidung in der :file:`local_settings.py`
angelegt werden::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'cookbook.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
        'newsdb': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'news.db'),
        },
        'addressdb': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'address.db'),
        },
    }

Nun können wir die Queries mit der neuen Datenbank ausführen::

    $ python sqltestdata.py 2000 | python manage.py dbshell --database=addressdb

Und uns auch gleich die Daten ansehen::

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

Als nächstes erstellen wir eine App für die neue Datenbank::

    $ python manage.py startapp addressbook

Und lassen Django mit Hilfe des Befehls :program:`inspectdb` Models aus den
Tabellen der Datenbank erzeugen::

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

Diese schreiben wir dann in die Datei :file:`addressbook/models.py`::

    $ python manage.py inspectdb --database=addressdb > addressbook/models.py

Damit die Models auch funktionieren passen wir sie noch ein wenig an (Zeilen
5, 10, 14, 16-17, 21, 23, 26, 28-29):

..  literalinclude:: ../../src/cookbook/addressbook/models.py
    :emphasize-lines: 5, 10, 14, 16-17, 21, 23, 26, 28-29
    :linenos:

Außerdem müssen wir den ``CookbookRouter`` erweitern (Zeilen 7-8, 14-15,
21-22):

..  literalinclude:: ../../src/cookbook/router.py
    :emphasize-lines: 7-8, 14-15, 21-22
    :linenos:

Jetzt benötigen wir nur noch eine :file:`addressbook/admin.py`, um die Daten
im Admin anzuzeigen. Wir aktivieren Suche und Filter, zeigen mehr Felder in
der Liste an und machen alle Felder im Formular nur lesbar:

..  literalinclude:: ../../src/cookbook/addressbook/admin.py
    :linenos:

Zuletzt aktivieren wir noch die App ``addressbook`` in den ``INSTALLED_APPS``
in der :file:`settings.py` und starten dann den Entwicklungs-Webserver, um uns
die Daten anzusehen.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Abstract base classes <topics/db/models/#abstract-base-classes>`
* :djangodocs:`Mehrere Datenbank nutzen <topics/db/multi-db/>`
