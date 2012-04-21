Python
******

Da Django komplett in Python geschrieben ist muss dies zuerst installiert
werden.

Python installieren
===================

Django |djangoversion| unterstützt die Python Versionen 2.5, 2.6 und 2.7. Wenn
du eine ältere Python Version hast, solltest du diese aktualisieren. Ab Django
1.5 wird Python 2.5 nicht mehr unterstützt werden, dafür gibt es aber
experimetelle Unterstützung für Python 3.3.

Deine Python Version kannst du heraus finden, indem du den Python Interpreter
an der Kommandozeile mit der Option ``-V`` startest:

..  code-block:: bash

    $ python -V
    Python 2.6.1

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
eine Python 2.6 Installation mit, Lion hat Python 2.7.1 installiert.

Alternativ kannst du auch Python mit Hilfe von Homebrew_ installieren.

..  _Homebrew: http://mxcl.github.com/homebrew/

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

distribute
----------

Zuerst muss :program:`distribute` installiert werden. :program:`distribute`
ist ein Ersatz für :program:`setuptools`, dass auf machen Systemen schon
installiert ist.

Es wird mit Hilfe eines Bootstrap-Skripts installiert:

..  code-block:: bash

    $ wget http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation
    benötigt.

pip
---

Das eigentliche Programm zum Installieren der Pakete ist :program:`pip`. Es
ist ein Ersatz für :program:`easy_install` mit `größerem Funktionsumfang
<http://www.pip-installer.org/en/latest/index.html#pip-compared-to-easy-install>`_.
:program:`pip` kann mit dessen Hilfe von :program:`easy_install` installiert
werden:

..  code-block:: bash

    $ easy_install pip

Falls :program:`easy_install` nicht installiert ist, kann :program:`pip` auch
mit Hilfe eines Bootstrap-Skripts installiert werden:

..  code-block:: bash

    $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    $ python get-pip.py

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation
    benötigt.

Nach der Installation kannst du :program:`pip` so testen:

..  code-block:: bash

    $ pip --help

Weiterführende Links
====================

    * `Python Homepage <http://python.org/>`_
    * `Offizielles Python Tutorial <http://docs.python.org/tutorial/index.html>`_
    * `Learn Python The Hard Way <http://learnpythonthehardway.org/>`_
    * `Code Like a Pythonista: Idiomatic Python (interaktives Tutorial) <http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html>`_
    * `distribute Dokumentation <http://packages.python.org/distribute/>`_
    * `pip Homepage <http://www.pip-installer.org/>`_
