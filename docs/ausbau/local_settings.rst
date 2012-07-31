Eine lokale Konfiguration
=========================

Einige Einstellungen in der Konfigurationsdatei :file:`settings.py` sind nur
für die Entwicklung sinnvoll. Zum Beispiel sollte ``DEBUG`` während der
Entwicklung den Wert ``True`` haben, auf dem Produktivsystem aber den Wert
``False``.

Um die Konfiguration für das Produktivsystem unverändert zu lassen bietet sich
folgendes Vorgehen an.

Am Ende der Datei :file:`settings.py` wird folgender Code eingefügt::

    try:
        from local_settings import *
    except ImportError:
        pass

Dieser Code lädt alle Einstellungen aus der Datei :file:`local_settings.py`
wenn diese existiert. Ist diese Datei nicht vorhanden passiert nichts. So kann
man in der Datei :file:`local_settings.py` bestimmte Werte neu definieren und
so die in :file:`settings.py` definierten Werte überschreiben.

Erweitere also deine Datei :file:`settings.py` am Ende wie oben angegeben.

Jetzt legst du in dem Verzeichnis, in dem sich auch die Datei
:file:`settings.py` befindet, die Datei :file:`local_settings.py` mit
folgendem Inhalt an (du kannst aus :file:`settings.py` kopieren)::

    import os

    from .settings import SITE_ROOT

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

Danach passe die folgenden Werte in :file:`settings.py` an::

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

    Natürlich kann man auch gleich die Werte für das Produktivsystem in die
    Datenbankkonfiguration eintragen (bis auf das Passwort!).

So lange also die Datei :file:`local_settings.py` vorhanden ist, arbeitest du
mit einer Konfiguration für die Entwicklung. Fehlt diese Datei benutzt du die
Einstellungen aus der Datei :file:`settings.py`, die für das Produktivsystem
optimiert sind.
