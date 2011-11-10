Mehrere Datenbanken nutzen
==========================

Seit Django 1.2 kann man mit mehreren Datenbanken gleichzeitig arbeiten.

Dazu tragen wir zuerst die neue Datenbank in die Datei
:file:`local_settings.py`` ein::

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

Diese Datenbank soll von einer News App genutzt werden. Also erstellen wir
diese jetzt::

    $ python manage.py startapp news

Zuerst wollen wir das Model anlegen. Dies soll auf einem abstrakten Model
aufbauen. Für dieses abstrakte Model legen wir im Verzeichnis :file:`cookbook`
die Datei :file:`basemodels.py` mit folgendem Inhalt an::

    import datetime

    from django.db import models


    class DateTimeInfo(models.Model):
        date_created = models.DateTimeField(editable=False)
        date_updated = models.DateTimeField(editable=False)

        class Meta:
            abstract = True

        def save(self, *args, **kwargs):
            if not self.id:
                self.date_created = datetime.datetime.now()
            self.date_updated = datetime.datetime.now()
            super(DateTimeInfo, self).save(*args, **kwargs)

Danach erstellen wir das Model ``Article`` in der Datei
:file:`news/models.py`::

    # encoding: utf-8
    from django.db import models

    from cookbook.basemodels import DateTimeInfo


    class Article(DateTimeInfo):
        headline = models.CharField('Überschrift', max_length=100)
        body = models.TextField('Inhalt')

        class Meta:
            verbose_name = 'Artikel'
            verbose_name_plural = 'Artikel'
            ordering = ['-date_updated']

        def __unicode__(self):
            return self.headline

Dadurch, dass das Model ``Article`` von dem Model ``DateTimeInfo`` erbt erhält
es automatisch die beiden ``DateTimeField`` Felder.

Jetzt brauchen wir noch eine :file:`admin.py`, um das Model im Admin nutzen zu
können::

    from django.contrib import admin

    from news.models import Article


    class ArticleAdmin(admin.ModelAdmin):
        list_display = ('headline', 'date_created', 'date_updated')


    admin.site.register(Article, ArticleAdmin)

Die Klasse ``NewsRouter`` erstellen
===================================

Damit wir die neue Datenbank auch mit der App "news" nutzen können benötigen
wir einen "database router". Diesen legen wir in der Datei
:file:`cookbook/router.py` an::

    class NewsRouter(object):
        """A router to control all database operations on models in the news application.
        """
        def db_for_read(self, model, **hints):
            "Point all operations on the news app models to newsdb."
            if model._meta.app_label == 'news':
                return 'newsdb'
            return None

        def db_for_write(self, model, **hints):
            "Point all operations on the news app models to newsdb."
            if model._meta.app_label == 'news':
                return 'newsdb'
            return None

        def allow_relation(self, obj1, obj2, **hints):
            "Allow no relation if a model in news app is involved."
            if obj1._meta.app_label == 'news' or obj2._meta.app_label == 'news':
                return False
            return None

        def allow_syncdb(self, db, model):
            "Make sure the news app only appears on the newsdb."
            allowed = ['south']
            if model._meta.app_label in allowed:
                return True
            elif db == 'newsdb':
                return model._meta.app_label == 'news'
            elif model._meta.app_label == 'news':
                return False
            return None

Danach müssen wir ``DATABASE_ROUTERS`` in der Datei :file:`settings.py`
konfigurieren::

    DATABASE_ROUTERS = ['cookbook.router.NewsRouter']

Außerdem aktivieren wir noch die neue App "news" in den ``INSTALLED_APPS``.

Die initiale Migration durchführen
==================================

Da wir im Kapitel :doc:`Migration <migration>` auf South umgestellt haben
können wir das neue Model ``Article`` nicht mehr mit dem Befehl ``syncdb``
erstellen. Also erstellen wir zuerst eine Migration mit dem Kommando
``schemamigration``::

    $ python manage.py schemamigration news --initial
    Creating migrations directory at '/Users/zappi/Projekte/Python/django-workshop/src/cookbook/news/migrations'...
    Creating __init__.py in '/Users/zappi/Projekte/Python/django-workshop/src/cookbook/news/migrations'...
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
aber nicht der Fall, denn der ``NewsRouter`` unterbindet das anlegen der
Tabellen. Wir können das auch prüfen::

    $ python manage.py dbshell --database=newsdb
    SQLite version 3.7.6.3
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> .tables
    news_article            south_migrationhistory

Jetzt führen wir die erste Migration durch::

    $ python manage.py migrate news
    Running migrations for news:
     - Migrating forwards to 0001_initial.
     > news:0001_initial
     - Loading initial data for news.
    No fixtures found.

Danach können wir den Entwicklungs-Webserver starten und einige Artikel in der
neuen News App anlegen.
