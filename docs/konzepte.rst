Wichtige Konzepte für die Arbeit mit Django
*******************************************

* ``virtualenv`` für die Isolation der Projekte nutzen
* ``pip`` zum Installieren von Python Paketen nutzen
* Django "Projekte" bestehen im Kern nur aus der Konfiguration in :file:`settings.py`

    * Diese verweist auf die zentrale URLConf (``ROOT_URLCONF``)
    * Sie enthält die Liste aller installierten Apps, die nicht zwingend im Projektverzeichnis sein müssen sondern aus dem ``PYTHONPATH`` geladen werden können
    * Eine Konstante wie zum Beispiel ``BASE_DIR`` nutzen, um den Pfad zum Konfigurationsverzeichnis zur Laufzeit zu ermitteln
    * Zusätzliche Dateien wie zum Beispiel :file:`local_settings.py` für das Trennen der Einstellungen benutzen
    * Eventuell `paster create <http://pythonpaste.org/script/#paster-create>`_ zur Erstellung von Projekten nutzen
* Das Verzeichnis einer App sollte immer alle nötigen Komponenten enthalten

    * URLConf (:file:`urls.py`)
        * In der URLConf immer "named URLs" benutzen
    * Models (:file:`models.py`)
    * Templates (:file:`templates/APPNAME/*.html`)
        * Die Verzeichnisstruktur so aufbauen, dass die Templateloader auch richtig funktionieren
    * Templatetags (:file:`templatetags`)
    * Views (:file:`views.py`)
    * Fomulare (:file:`forms.py`)
    * Fixtures (Verzeichis :file:`fixtures`)
    * Tests (:file:`tests.py`)
    * ...
* Innerhalb einer App immer relative Imports benutzen (siehe :pep:`328`)
* Falls nötig eine App in Python Packages für Models, Views oder Tests aufteilen
* Models

    * Für ``models.DateTimeField`` nicht ``auto_add`` und ``auto_add_now`` Argumente benutzen, sondern die Logik selbst implementieren
    * Methoden möglichst flexibel überschreiben::

        def save(self, *args, **kwargs):
            # Code, der beim Speichern ausgeführt wird
    * Ein ``QuerySet`` benutzt "lazy loading" und kann immer um neue Bedigungen erweitert werden, so lange es noch nicht ausgegeben oder ein Iterator benutzt wurde
    * ``QuerySet.count()`` statt ``len(QuerySet)`` benutzen
    * Mit einem "related manager" auf das andere Model einer Relation zugreifen
    * ``models.Q`` für ``OR`` Queries oder Factories nutzen
    * Komplexe Queries und Funktionen als :doc:`Methoden am Model <ausbau/modelmethoden>` implementieren

* Views

    * Funktionen aus ``django.shortcuts`` nutzen
    * :djangodocs:`Class-based views <topics/class-based-views/>` nutzen
* Templates

    * Keine Logik in Templates implementieren
    * ``block`` Tags können auch gut zum Kontrollieren von Templates benutzt werden, die man erweitert hat (Beispiel :ref:`toggle_login Block <toggle_login>`)
    * :file:`404.html` und :file:`500.html` anlegen (siehe :doc:`Fehlerbehandlung <ausbau/fehlerbehandlung>`)
* Debugging

    * :ref:`Django Debug Toolbar <debug_toolbar>` nutzen
    * Das in Django 1.3 eingeführte :ref:`Logging-Framework <logging_framework>` nutzen
    * :ref:`Den Python-Debugger nutzen <python_debugger>`
* Tests

    * Statt Doctests :ref:`besser Unittests nutzen <vor_und_nachteile_unittests>`
    * Test-Abdeckung mit Hilfe von :doc:`coverage <ausbau/softwaretests/coverage>` ermitteln
* Nicht davor zurückschrecken eine :doc:`Middleware zu schreiben <ausbau/middleware>`
