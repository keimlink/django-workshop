Das erste Django Projekt
************************

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
    $ django-admin.py startproject kochbuch

Dein neues Projekt wurde erstellt. Erstmal enthält es nicht viel::

    __init__.py
    manage.py
    settings.py
    urls.py

Die leere Datei ``__init__.py`` zeigt an, dass es sich beim Verzeichnis ``kochbuch`` um ein Python Package handelt.

``manage.py`` wirst du benutzen, um dein Projekt zu verwalten.

Die Datei ``settings.py`` enthält alle Einstellungen deines Projekts.

In ``urls.py`` enthält die regulären Ausdrücke, um einen URL zum richtigen View zu leiten. Dazu später mehr.

Die Konfiguration anpassen
==========================


