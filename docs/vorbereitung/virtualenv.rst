Virtualenv
**********

Was ist virtualenv?
===================

Wenn man beginnt an mehreren Projekten parallel zu arbeiten kommt irgendwann
der Zeitpunkt, an den Kollisionen bei den installierten Paketen auftreten.

Ein altes Projekt benutzt zum Beispiel noch Django 1.1 und kann aus Zeitmangel
nicht migriert werden. Gleichzeitig soll aber ein neues Projekt mit Django
|djangoversion| gestartet werden.

Solche Probleme kann :program:`virtualenv` lösen.

:program:`virtualenv` kann für jedes Projekt einen "Container" erstellen, der
die installierten Pakete von der Basisinstallation abkapselt.

Außerdem kann :program:`virtualenv` jeder Umgebung eine bestimmte Python
Version zuordnen. Man kann also ein virtuelle Arbeitsumgebung mit Python 2.5
erstellen, das nächste mit Python 2.6.

Außerdem lässt sich :program:`virtualenv` auch im Produktivbetrieb auf dem
Server einsetzen. Man kann dort also die gleiche Umgebung nutzen wie schon
während der Entwicklung.

Installation
============

:program:`virtualenv` wird mit Hilfe von :program:`pip` installiert:

..  code-block:: bash

    $ pip install virtualenv

..  note::

    Unter Linux und Mac OS X werden evtl. *root*-Rechte für die Installation
    benötigt.

Nach der Installation sollte ein Verzeichnis für *alle* virtuellen Projekte
anlegt werden, zum Beispiel im Home-Verzeichnis:

..  code-block:: bash

    $ mkdir .virtualenvs

Einfacher Arbeiten mit virtualenvwrapper
========================================

Um die Arbeit mit :program:`virtualenv` zu vereinfachen kann man unter Linux
oder Mac OS X das Paket :program:`virtualenvwrapper` installieren:

..  code-block:: bash

    $ pip install virtualenvwrapper

Nach der Installation werden die folgenden beiden Zeilen in die Datei
:file:`.bashrc` oder :file:`.profile` eingefügt:

..  code-block:: bash

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

Dadurch "weiss" :program:`virtualenvwrapper` wo sich alle virtuellen
Arbeitsumgebungen befinden. Das Skript :file:`virtualenvwrapper.sh` lädt die
Shell-Befehle, mit denen wir arbeiten werden.

Weiterführende Links
====================

    * `virtualenv Dokumentation <http://www.virtualenv.org/en/latest/>`_
    * `virtualenvwrapper Homepage <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
