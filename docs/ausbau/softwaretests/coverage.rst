Test-Abdeckung ermitteln
************************

Natürlich ist es auch wichtig zu wissen, für welche Teile der Applikation schon Tests geschrieben wurden. Dabei hilft das Python Paket `coverage <http://nedbatchelder.com/code/coverage/>`_. Bis jetzt wurde es noch nicht in Django integriert und muss daher manuell installiert werden::

    $ pip install coverage

Damit ``coverage`` auch nur unsere Applikationen und nicht das Framework selbst betrachtet legst du die Datei ``.coveragerc`` mit folgendem Inhalt im Projektverzeichnis an::

    [report]
    omit = /path/to/.virtualenvs

Jetzt kannst du mit dem folgenden Kommando die Daten für den Coverage-Report der Applikation ``recipes`` erzeugen::

    $ coverage run manage.py test recipes

Die Daten kannst auf der Shell mit diesem Befehl ausgeben::

    $ coverage report -m

Einen HTML-Coverage-Report kannst du mit diesem Befehl erstellen::

    $ coverage html

Die HTML-Dateien befinden sich dann im Verzeichnis ``htmlcov``.