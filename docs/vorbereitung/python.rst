Python
******

Da Django komplett in Python geschrieben ist muss dies zuerst installiert
werden.

Python installieren
===================

Django 1.2 unterstützt die Python Versionen 2.4, 2.5 und 2.6. Wenn du eine
ältere Python Version hast, solltest du diese aktualisieren.

Deine Python Version kannst du heraus finden indem du den Python Interpreter
an der Kommandozeile startest:

..  code-block:: bash

    $ python
    Python 2.6.1 (r261:67515, Feb 11 2010, 00:51:29) 
    [GCC 4.2.1 (Apple Inc. build 5646)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    
Hier wurde eine Python 2.6 Installation unter Mac OS X gestartet.

Wenn du Python schon in der richtigen Version installiert hast, kannst du mit
der Installation des :ref:`Python Paketmanagers <python_paketmanager>`
weitermachen.

Linux
-----

Viele Linux Distributionen haben Python schon installiert. Solltest du noch
kein Python installiert haben kannst du dies meistens mit dem Paketmanager
nachholen.

Alternativ kannst du auch die `Quellen von der Python Website herunter laden
<http://python.org/download/>`_ und selbst kompilieren.

Mac OS X
--------

Mac OS X wird mit einer Python-Installation ausgeliefert: Snow Leopard bringt
eine Python 2.6 Installation mit.

Windows
-------

Lade den `Installer <http://python.org/download/>`_ von der Python Website
herunter und installiere Python.

..  _python_paketmanager:

Python Paketmanager
===================

Python benutzt ein eigenes Paketsystem zur Verteilung und Installation von
Python Paketen. Da wir einige Pakete installieren werden muss vorher der
Paketmanager installiert werden.

``distribute``
---------------

Zuerst muss ``distribute`` installiert werden. ``distribute`` ist ein Ersatz
für ``setuptools``, dass auf machen Systemen schon installiert ist.

Es wird mit Hilfe eines Bootstrap-Skripts installiert:

..  code-block:: bash

    $ wget http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation
    benötigt.

``pip``
-------

Das eigentliche Programm zum Installieren der Pakete ist ``pip``. Es ist ein
Ersatz für ``easy_install`` mit `größerem Funktionsumfang
<http://pip.openplans.org/#differences-from-easy-install>`_. Wer
``easy_install`` schon installiert hat, kann ``pip`` mit dessen Hilfe
installieren:

..  code-block:: bash

    $ easy_install pip

Wer ``easy_install`` nicht zur Verfügung hat lädt sich den Quellcode von
``pip`` herunter und installiert das Programm auf diesem Weg:

..  TODO: Link zur pip Downloadseite
..  TODO: Beispiel zur Installation vervollständigen

..  code-block:: bash

    $ tar xzf pip
    $ cd pip
    $ python setup.py install

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation
    benötigt.

Nach der Installation kannst du ``pip`` so testen:

..  code-block:: bash

    $ pip --help

Weiterführende Links
====================

    * `Python Homepage <http://python.org/>`_
    * `Offizielles Python Tutorial <http://docs.python.org/tut/tut.html>`_
    * `Dive Into Python <http://diveintopython.org/>`_
    * `Code Like a Pythonista: Idiomatic Python (interaktives Tutorial) <http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html>`_

..  TODO: Links zu distribute und pip einfügen
