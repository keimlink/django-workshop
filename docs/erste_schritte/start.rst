Ein neues Projekt beginnen
**************************

Nachdem nun alle Vorbereitungen getroffen wurden, um mit Django und Python zu
arbeiten kann das erste Projekt beginnen.

Ein Verzeichnis für alle Python Projekte
========================================

Zuerst erstellst du ein Verzeichnis für dies und alle zukünftigen Projekte:

..  code-block:: bash

    $ mkdir pythonprojects

Es ist sinnvoll, alle Python Projekte in einem Verzeichnis zu haben.

Das Django Projekt erstellen
============================

Jetzt werden wir das Django Projekt erstellen. Es soll ein Kochbuch werden,
also nennen wir das Projekt ``cookbook``.

Wechsel nun in das neu erstellte Verzeichnis und erstelle ein Django Projekt:

..  code-block:: bash

    $ cd pythonprojects
    $ django-admin.py startproject cookbook

Dein neues Projekt wurde erstellt. Das Verzeichnis ``cookbook`` enthält
erstmal nicht viel:

..  code-block:: bash

    cookbook/
    |-- __init__.py
    |-- manage.py
    |-- settings.py
    `-- urls.py

Die leere Datei ``__init__.py`` zeigt an, dass es sich beim Verzeichnis
``cookbook`` um ein `Python Paket
<http://docs.python.org/tutorial/modules.html#packages>`_ handelt.

``manage.py`` wirst du benutzen, um dein Projekt zu verwalten.

Die Datei ``settings.py`` enthält alle Einstellungen deines Projekts.

In ``urls.py`` sind die regulären Ausdrücke enthalten, um einen URL zum
richtigen View zu leiten. Dazu später mehr.

Das Projekt in das *virtual environment* einbinden
==================================================

Der Code aus unserem Projekt muss auch im *virtual environment* zur Verfügung
stehen. Also müssen wir dem *virtual environment* mitteilen, wo sich unser
Projekt befindet.

Das Paket ``virtualenvwrapper`` hat dafür ein Kommando:

..  code-block:: bash

    $ add2virtualenv pythonprojects

Wenn ``virtualenvwrapper`` nicht installiert ist muss der Pfad zum Verzeichnis
``pythonprojects`` per Hand eingefügt werden:

..  code-block:: bash

    $ cd .virtualenvs/django-workshop/lib/python2.6/site-packages
    $ echo $HOME/pythonprojects > virtualenv_path_extensions.pth

..  note::

    Wenn das *virtual environment* mit einer anderen Python Version erzeugt wurde
    kann der Pfad zum Verzeichnis ``site-packages`` abweichen.

Anpassen der Konfiguration
==========================

Damit wir mit dem Projekt arbeiten können muss als erstes die Konfiguration
angepasst werden. Dazu öffnest du die Datei ``settings.py`` in einem
Texteditor.

Damit wir das Arbeitsverzeichnis nicht mehrfach in die Konfiguration eintragen
müssen ermitteln wir er dynamisch und speichern es in einer "Konstanten"::

    import os

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

..  note::

    In Python sind Bezeichner in Grossbuchstaben per Konvention Konstanten.

Nun konfigurieren wir die Datenbankverbindung. Wir werden eine `SQLite
<http://www.sqlite.org/>`_ Datenbank benutzen, da ein ``sqlite3`` Paket ab der
Version 2.5 in Python enthalten ist.

Wenn du Python 2.4 benutzt musst du selbst ein Paket für SQLite installieren.

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

    LANGUAGE_CODE = 'de'

Als letztes muss der Pfad zu den Templates definiert werden::

    TEMPLATE_DIRS = (
        os.path.join(SITE_ROOT, 'templates')
    )

Das Verzeichnis für die Templates erzeugen wir später in der Wurzel des
Projekts. Deshalb benutzen wir wieder den zu Beginn definierten Pfad als
Präfix.

..  note::

    Es wäre auch möglich die Templates außerhalb des Projekts zu speichern. Dazu
    muss der Pfad auf dieses Verzeichnis verweisen.

Weiterführende Links zur Django Dokumentation
=============================================

* `Konfiguration von Django <http://docs.djangoproject.com/en/1.2/topics/settings/#topics-settings>`_
* `Liste aller möglichen Konstanten für die Konfiguration <http://docs.djangoproject.com/en/1.2/ref/settings/#ref-settings>`_
