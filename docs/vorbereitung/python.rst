Python
******

Da Django komplett in Python geschrieben ist muss dies zuerst installiert werden.

Python installieren
===================

Django 1.2 unterstützt die Python Versionen 2.4, 2.5 und 2.6. Wenn du eine ältere Python Version hast, solltest du diese aktualisieren.

Deine Python Version kannst du heraus finden indem du den Python Interpreter an der Kommandozeile startest:

..  code-block:: bash

    $ python
    Python 2.6.1 (r261:67515, Feb 11 2010, 00:51:29) 
    [GCC 4.2.1 (Apple Inc. build 5646)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    
Hier wurde eine Python 2.6 Installation unter Mac OS X gestartet.

Wenn du Python schon in der richtigen Version installiert hast, kannst du mit der Installation des :ref:`Python Paketmanagers <python_paketmanager>` weitermachen.

Linux
-----

Viele Linux Distributionen haben Python schon installiert. Solltest du noch kein Python installiert haben kannst du dies meistens mit dem Paketmanager nachholen.

Alternativ kannst du auch die `Quellen von der Python Website herunter laden <http://python.org/download/>`_ und selbst kompilieren.

Mac OS X
--------

Mac OS X hat Python schon installiert. Snow Leopard bringt eine Python 2.6 Installation mit.

Windows
-------

Lade den `Installer <http://python.org/download/>`_ von der Python Website herunter und installiere Python.

..  _python_paketmanager:

Python Paketmanager
===================

Python benutzt ein eigenes Paketsystem zur Verteilung und Installation von Python Paketen. Da wir einige Pakete installieren werden muss vorher der Paketmanager installiert werden.

``setuptools``
--------------

Eine Anleitung zur Installation von ``setuptools`` für alle Betriebssysteme findest du hier: http://pypi.python.org/pypi/setuptools

Falls sich die ``setuptools`` nicht nach der oben genannten Anleitung installieren lassen gibt es auch die Möglichkeit dies mit Hilfe eines *bootstrap*-Skripts zu tun.

Dazu muss das Skript ``ez_setup.py`` herunterladen werden: http://peak.telecommunity.com/dist/ez_setup.py

Und dann das Skript starten:

..  code-block:: bash

    $ python ez_setup.py

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation benötigt.

``easy_install``
----------------

Nach der Installation der ``setuptools`` steht das Programm ``easy_install`` zur Verfügung. Du kannst es so ausprobieren:

..  code-block:: bash

    $ easy_install --help

``pip``
-------

Mit Hilfe von ``easy_install`` wird jetzt ``pip`` installiert. ``pip`` ist ein Ersatz für ``easy_install`` mit `größerem Funktionsumfang <http://pip.openplans.org/#differences-from-easy-install>`_:

..  code-block:: bash

    $ easy_install pip

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation benötigt.

Nach der Installation kannst du ``pip`` so testen:

..  code-block:: bash

    $ pip --help

``distribute``
---------------

Zuletzt muss ``distribute`` als Ersatz für ``setuptools`` installiert werden:

..  code-block:: bash

    $ wget http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py

..  note::
    
    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation benötigt.

Weiterführende Links
====================

    * `Python Homepage <http://python.org/>`_
    * `Offizielles Python Tutorial <http://docs.python.org/tut/tut.html>`_
    * `Dive Into Python <http://diveintopython.org/>`_
    * `Code Like a Pythonista: Idiomatic Python (interaktives Tutorial) <http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html>`_
