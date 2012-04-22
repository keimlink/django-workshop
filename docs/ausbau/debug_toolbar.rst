..  _debug_toolbar:

Debug Toolbar
*************

Der `Debug Toolbar <https://github.com/robhudson/django-debug-toolbar>`_ kann
während der Entwicklung eines Projekts mit Django eine große Hilfe sein.
Folgende Panels können im Browser eingeblendet werden:

* Django Version
* Python Version
* Versionen der installierten Python Packages
* Benutze Resourcen
* Eine Liste der Werte aus :file:`settings.py`
* HTTP Header
* GET/POST/cookie/session Variablen
* SQL Queries mit Ausführungszeit und Links, die für jeden Query ein EXPLAIN
  aufrufen
* Templates und deren Context sowie die Template-Pfade
* Liste der Signale mit deren Argumenten und Empfängern
* Log-Ausgabe mit dem in Python integrierten ``logging`` Modul

Außerdem wird ein weiteres Kommando zur :file:`manage.py` hinzugefügt:

* :command:`debugsqlshell`: Während der Arbeit mit der :ref:`Datenbank API <datenbank-api>` im Python
  Interpreter werden die SQL Queries ausgegeben

Installation
============

So kannst du den Debug Toolbar installieren:

..  code-block:: bash

    $ pip install django-debug-toolbar

Konfiguration
=============

Um den Debug Toolbar für dein Projekt zu aktivieren fügst du den folgenden
Code in die Datei :file:`settings.py` ein::

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

..  note::

    Die Einstellung ``INTERNAL_IPS`` bestimmt, welche IP Adressen den Debug
    Toolbar sehen können. Hier kannst du noch weitere Adressen eintragen, wenn
    du zum Beispiel eine virtuelle Maschine als Entwicklungsumgebung benutzt.
