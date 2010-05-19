Django
******

Ein neues *virtual environment* für das Projekt anlegen
=======================================================

Nachdem nun Python und ``virtualenv`` installiert sind kann ein neues *virtual environment* für Django angelegt werden::

    $ mkvirtualenv --distribute --no-site-packages django-workshop

Falls kein ``virtualenvwrapper`` installiert wurde muss folgendes Kommando ausgeführt werden::

    $ virtualenv --distribute --no-site-packages .virtualenvs/django-workshop

Folgendes passiert:

    * Die Option ``--distribute`` installiert im *virtual environment* ``distribute`` statt ``setuptools``
    * Durch die Option ``--no-site-packages`` stehen die in der zentralen Python Installation vorhandenen Pakete nicht zur Verfügung
    * ``django-workshop`` ist der Name, unter dem das *virtual environment* später zur Verfügung steht

Falls der ``virtualenvwrapper`` benutzt wurde ist das *virtual environment* jetzt schon aktiviert.

Andernfalls muss es manuell aktiviert werden::

    $ cd .virtualenvs/django-workshop
    $ . bin/activate

Django installieren
===================

Jetzt installieren wir Django in das aktivierte *virtual environment*::

    $ pip install django

Wenn der ``virtualenvwrapper`` installiert ist, kann man sich die installierten Pakete mit folgendem Kommando anzeigen lassen::

    $ lssitepackages -l

Ohne ``virtualenvwrapper`` kann man sich die Pakete einfach direkt im Verzeichnis ansehen::

    $ ls -l .virtualenvs/django-workshop/lib/python2.6/site-packages/
