Eine lokale Konfiguration
=========================

Einige Einstellungen in der Konfigurationsdatei ``settings.py`` sind nur für die Entwicklung sinnvoll. Zum Beispiel sollte ``DEBUG`` während der Entwicklung den Wert ``True`` haben, auf dem Produktivsystem aber den Wert ``False``.

Um die Konfiguration für das Produktivsystem unverändert zu lassen bietet sich folgendes Vorgehen an.

Am Ende der Datei ``settings.py`` wird folgender Code eingefügt::

    try:
        from local_settings import *
    except ImportError:
        pass

Dieser Code lädt alle Einstellungen aus der Datei ``local_settings.py`` wenn diese existiert. Ist diese Datei nicht vorhanden passiert nichts. So kann man in der Datei ``local_settings.py`` bestimmte Werte neu definieren und so die in ``settings.py`` definierten Werte überschreiben.

Erweitere deine Datei ``settings.py`` am Ende wie oben angegeben. Dann passe die folgenden Werte an::

    DEBUG = False
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

..  note::

    Natürlich kann man auch gleich die Werte für das Produktivsystem in die Datenbankkonfiguration eintragen.

Jetzt legst du im Projektverzeichnis ``cookbook`` die Datei ``local_settings.py`` mit folgendem Inhalt an::

    import os

    from settings import SITE_ROOT

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'cookbook.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

So lange nun die Datei ``local_settings.py`` vorhanden ist arbeitest du mit einer Konfiguration für die Entwicklung. Fehlt diese Datei benutzt du die Einstellungen aus der Datei ``settings.py``, die für das Produktivsystem optimiert sind.
