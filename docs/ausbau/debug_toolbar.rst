..  _debug_toolbar:

Debug Toolbar
*************

Der `Debug Toolbar <http://github.com/robhudson/django-debug-toolbar>`_ kann während der Entwicklung eines Projekts mit Django eine große Hilfe sein. Folgende Panels können im Browser eingeblendet werden:

* Django Version
* Request Timer
* Eine Liste der Werte aus ``settings.py``
* HTTP Header
* GET/POST/cookie/session Variablen
* Templates und deren Context sowie die Template-Pfade
* SQL Queries mit Ausführungszeit und Links, die für jeden Query ein EXPLAIN aufrufen
* Liste der Signale mit deren Argumenten und Empfängern
* Log-Ausgabe mit dem in Python integrierten ``logging`` Modul

Außerdem wird ein weiteres Kommando zur ``manage.py`` hinzugefügt:

* *debugsqlshell*: Während der Arbeit mit der Datenbank API im Python Interpreter werden die SQL Queries ausgegeben

Installation
============

So kannst du den Debug Toolbar installieren:

..  code-block:: bash

    $ pip install django-debug-toolbar

Konfiguration
=============

Um den Debug Toolbar für dein Projekt zu aktivieren fügst du den folgenden Code in die Datei ``settings.py`` ein::

    MIDDLEWARE_CLASSES = (
        ...
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS = (
        ...
        'debug_toolbar',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

Der Debug Toolbar ist nun im Browser auf der rechten Seite verfügbar.
