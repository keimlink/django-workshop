Ein neues Projekt beginnen
**************************

Nachdem nun alle Vorbereitungen getroffen wurden, um mit Django und Python zu
arbeiten, kann das erste Projekt beginnen.

Ein Verzeichnis für alle Python Projekte
========================================

Zuerst erstellst du ein Verzeichnis für dieses und alle zukünftigen Projekte:

..  code-block:: bash

    $ mkdir pythonprojects

Es ist sinnvoll, alle Python Projekte in einem Verzeichnis zu haben.

Das Django Projekt erstellen
============================

Jetzt werden wir das Django Projekt erstellen. Es soll ein Kochbuch werden,
also nennen wir das Projekt :file:`cookbook`.

Wechsel nun in das neu erstellte Verzeichnis und erstelle ein Django Projekt:

..  code-block:: bash

    $ cd pythonprojects
    $ django-admin.py startproject cookbook

..  note::

    Unter Windows kann es nötig sein, dass den kompletten Pfad zu :file:`django-admin.py` angeben musst::

        > python C:\virtualenvs\django-workshop\Scrips\django-admin.py startproject cookbook

Dein neues Projekt wurde erstellt. Das Verzeichnis :file:`cookbook` enthält
erstmal nicht viel:

..  code-block:: bash

    cookbook # Projektverzeichnis
    |-- cookbook # Konfigurationsverzeichnis
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    `-- manage.py

Das erste Verzeichnis :file:`cookbook` ist das Projektverzeichnis. Es enthält
die Datei :file:`manage.py`, die du benutzen wirst, um dein Projekt zu
verwalten. Auf dieses Verzeichnis wird in allen anderen Kapiteln mit
**Projektverzeichnis** Bezug genommen.

Außerdem enthält es das `Python Paket
<http://docs.python.org/tutorial/modules.html#packages>`_ :file:`cookbook`
innnerhalb des Projektverzeichnisses, mit der zentralen Konfiguration für das
Django Projekt. Dies wird durch die leere Datei :file:`__init__.py` angezeigt.
Die Datei :file:`settings.py` enthält alle Einstellungen deines Projekts. In
:file:`urls.py` sind die regulären Ausdrücke enthalten, um einen URL zum
richtigen View zu leiten aber dazu später mehr. Die :file:`wsgi.py` definiert die WSGI
Applikation, die später beim Deployment benötigt wird. Auf dieses Verzeichnis
wird in allen anderen Kapiteln mit **Konfigurationsverzeichnis** Bezug
genommen.

Den Entwicklungsserver ausprobieren
===================================

Nachdem du das Projekt erstellt hast kannst du den Entwicklungsserver
mit dem folgenden Kommando ausprobieren::

    $ python manage.py runserver
    Validating models...

    0 errors found
    Django version 1.5.1, using settings 'cookbook.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Jetzt kannst du unter http://127.0.0.1:8000/ die "Welcome to Django"
Seite sehen. Nachdem du die Seite aufgerufen hast beende die Ausführung
des Entwicklungsservers wieder mit ``STRG + C``.

.. image:: /images/welcome_to_django.png

Anpassen der Konfiguration
==========================

Damit wir mit dem Projekt arbeiten können muss als erstes die Konfiguration
angepasst werden. Dazu öffnest du die Datei :file:`settings.py` in einem
Texteditor.

Damit wir das Arbeitsverzeichnis nicht mehrfach in die Konfiguration eintragen
müssen, ermitteln wir es dynamisch und speichern es in einer "Konstanten"::

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

..  note::

    In Python sind Bezeichner in Grossbuchstaben per Konvention Konstanten.

Nun konfigurieren wir die Datenbankverbindung. Wir werden eine `SQLite
<http://www.sqlite.org/>`_ Datenbank benutzen, da ein ``sqlite3`` Paket ab der
Version 2.5 in Python enthalten ist.

Konfiguriere die Datenbankverbindung ``default`` wie folgt::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'cookbook.db'),
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
        os.path.join(BASE_DIR, 'templates'),
    )

Das Verzeichnis für die Templates erzeugen wir später in der Wurzel des
Projekts. Deshalb benutzen wir wieder den zu Beginn definierten Pfad als
Präfix.

..  note::

    Es wäre auch möglich die Templates außerhalb des Projekts zu speichern.
    Dazu muss der Pfad auf dieses Verzeichnis verweisen.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Konfiguration von Django <topics/settings/#topics-settings>`
* :djangodocs:`Liste aller möglichen Konstanten für die Konfiguration <ref/settings/#ref-settings>`
