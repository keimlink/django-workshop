Ein neues Projekt beginnen
**************************

Nachdem nun alle Vorbereitungen getroffen wurden, um mit Django und Python zu arbeiten kann das erste Projekt beginnen.

Ein Verzeichnis für alle Python Projekte
========================================

Zuerst erstellst du ein Verzeichnis für dies und alle zukünftigen Projekte:

    $ mkdir pythonprojects

Es ist gut, alle Python Projekte in einem Verzeichnis zu haben.

Das Django Projekt erstellen
============================

Wechsel nun in das neu erstellte Verzeichnis und erstelle ein Django Projekt::

    $ cd pythonprojects
    $ django-admin.py startproject cookbook

Dein neues Projekt wurde erstellt. Erstmal enthält es nicht viel::

    __init__.py
    manage.py
    settings.py
    urls.py

Die leere Datei ``__init__.py`` zeigt an, dass es sich beim Verzeichnis ``cookbook`` um ein Python Package handelt.

``manage.py`` wirst du benutzen, um dein Projekt zu verwalten.

Die Datei ``settings.py`` enthält alle Einstellungen deines Projekts.

In ``urls.py`` sind die regulären Ausdrücke enthalten, um einen URL zum richtigen View zu leiten. Dazu später mehr.

Anpassen der Konfiguration
==========================

Als erstes muss die Konfiguration angepasst werden. Dazu öffnest du die Datei ``settings.py`` in einem Texteditor.

Damit wir das Arbeitsverzeichnis nicht mehrfach in die Konfiguration eintragen müssen ermitteln wir er dynamisch und speichern es in einer "Konstanten"::

    import os

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

..  note::

    In Python sind Bezeichner in Grossbuchstaben per Konvention Konstanten.

Nun konfigurieren wir die Datenbankverbindung. Wir werden eine `SQLite <http://www.sqlite.org/>`_ Datenbank benutzen, da ein ``sqlite3`` Package ab der Version 2.5 in Python enthalten ist.

Wenn du Python 2.4 benutzt musst du selbst ein Package für SQLite installieren.

Konfiguriere die Datenbankverbindung ``default`` wird folgt::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'cookbook.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

Als nächstes passen wir Zeitzone und Sprache an::

    TIME_ZONE = 'Europe/Berlin'

    LANGUAGE_CODE = 'de-de'

Als letztes muss der Pfad zu den Templates definiert werden::

    TEMPLATE_DIRS = (
        os.path.join(SITE_ROOT, 'templates')
    )

Das Verzeichnis für die Templates erzeugen wir später in der Wurzel des Projekts. Deshalb benutzen wir wieder den zu Beginn definierten Pfad als Präfix.

..  note::

    Es wäre auch möglich die Templates außerhalb des Projekts zu speichern. Dazu muss der Pfad auf dieses Verzeichnis verweisen.

Mehr zur Konfiguration von Django kannst du in der `Dokumentation nachlesen <http://docs.djangoproject.com/en/1.2/topics/settings/#topics-settings>`_. Dort findest du auch eine `Liste aller in der Konfiguration benutzten Konstanten <http://docs.djangoproject.com/en/1.2/ref/settings/#ref-settings>`_.
