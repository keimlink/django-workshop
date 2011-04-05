Django
******

Ein neues *virtual environment* für das Projekt anlegen
=======================================================

Nachdem nun Python und :program:`virtualenv` installiert sind kann ein neues
*virtual environment* für Django angelegt werden:

..  code-block:: bash

    $ mkvirtualenv --distribute --no-site-packages django-workshop

Falls kein :program:`virtualenvwrapper` installiert wurde muss folgendes
Kommando ausgeführt werden:

..  code-block:: bash

    $ virtualenv --distribute --no-site-packages .virtualenvs/django-workshop

Folgendes passiert:

    * Die Option ``--distribute`` installiert im *virtual environment*
      ``distribute`` statt ``setuptools``
    * Durch die Option ``--no-site-packages`` stehen die in der zentralen
      Python Installation vorhandenen Pakete nicht zur Verfügung
    * ``django-workshop`` ist der Name, unter dem das *virtual environment*
      später zur Verfügung steht

Falls der :program:`virtualenvwrapper` benutzt wurde ist das *virtual
environment* jetzt schon aktiviert.

Andernfalls muss es manuell aktiviert werden:

..  code-block:: bash

    $ cd .virtualenvs/django-workshop
    $ . bin/activate

Django installieren
===================

Jetzt installieren wir Django in das aktivierte *virtual environment*:

..  code-block:: bash

    $ pip install django

Wenn der :program:`virtualenvwrapper` installiert ist, kann man sich die
installierten Pakete mit folgendem Kommando anzeigen lassen:

..  code-block:: bash

    $ lssitepackages -l

Ohne :program:`virtualenvwrapper` kann man sich die Pakete einfach direkt im
Verzeichnis ansehen:

..  code-block:: bash

    $ ls -l .virtualenvs/django-workshop/lib/python2.6/site-packages/

Weiterführende Links
====================

    * `Django Homepage <http://www.djangoproject.com/>`_
    * `The Django Book <http://djangobook.com/en/2.0/>`_
