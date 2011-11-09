Wichtige Konzepte für die Arbeit mit Django
*******************************************

* ``virtualenv`` für die Isolation der Projekte nutzen
* ``pip`` zum Installieren von Python Paketen nutzen
* Django "Projekte" bestehen im Kern nur aus der Konfiguration in :file:`settings.py`

    * Diese verweist auf die zentrale URLConf (``ROOT_URLCONF``)
    * Sie enthält die Liste aller installierten Apps, die nicht zwingend im Projektverzeichnis sein müssen sondern aus dem ``PYTHONPATH`` geladen werden können
    * Eine Konstante wie zum Beispiel ``SITE_ROOT`` nutzen, um den Pfad zum Projektverzeichnis zur Laufzeit zu ermitteln
    * Zusätzliche Dateien wie zum Beispiel :file:`local_settings.py` für das Trennen der Einstellungen benutzen
    * Eventuell `paster create <http://pythonpaste.org/script/#paster-create>`_ zur Erstellung von Projekten nutzen
* Jede App sollte immer alle nötigen Komponenten enthalten

    * URLConf
    * Models
    * Templates
    * Templatetags
    * Views
    * Fomulare
    * Fixtures
    * Tests
    * ...
* Eine App sollte sich nur dann auf ein Projekt beziehen, wenn sie auch zum Projekt gehört

    * ``from cookbook.recipes.models import Recipe`` nur nutzen, wenn man die App nicht aus der Projekt entfernt
    * Sonst ``from recipes.models import Recipe`` benutzen
* Falls nötig eine App in Python Packages für Models, Views oder Tests aufteilen
* Models

    * Für ``models.DateTimeField`` nicht ``auto_add`` und ``auto_add_now`` Argumente benutzen, sondern die Logik selbst implementieren
    * Methoden möglichst flexibel überschreiben::

        def save(self, *args, **kwargs):
            # Code, der beim Speichern ausgeführt wird
    * Ein ``QuerySet`` benutzt "lazy loading" und kann immer um neue Bedigungen erweitert werden
    * ``QuerySet.count()`` statt ``len(QuerySet)`` benutzen
    * Mit einem "related manager" auf das andere Model einer Relation zugreifen
    * ``models.Q`` für ``OR`` Queries oder Factories nutzen
    * Komplexe Queries und Funktionen als :doc:`Methoden am Model <ausbau/modelmethoden>` implementieren

* Views

    * Funktionen aus ``django.shortcuts`` nutzen
    * :djangodocs:`Class-based views <topics/class-based-views/>` nutzen
* Templates

    * ``block`` Tags können auch gut zum Kontrollieren von Templates benutzt werden, die man erweitert hat (Beispiel :ref:`toggle_login Block <toggle_login>`)
    * :file:`404.html` und :file:`500.html` anlegen (siehe :doc:`ausbau/fehlerbehandlung`)
* Debugging

    * :ref:`Django Debug Toolbar <debug_toolbar>` nutzen
    * Das in Django 1.3 eingeführte :ref:`Logging-Framework <logging_framework>` nutzen
    * :ref:`python_debugger`
* Tests
    * Statt Doctests besser Unittests nutzen
    * Test-Abdeckung mit Hilfe von :doc:`coverage <ausbau/softwaretests/coverage>` ermitteln
* Nicht davor zurückschrecken eine :doc:`Middleware zu schreiben <ausbau/middleware_403>`
