Alternative Authentifizierung
*****************************

Eine alternative Authentifizierung kann man in der Datei :file:`userauth/backends.py` wie folgt implementieren:

..  literalinclude:: ../../src/cookbook/userauth/backends.py

.. note::

    ``SettingsBackend`` nutzt das
    :djangodocs:`UserProfile <topics/auth/#storing-additional-information-about-users>`
    zum Speichern zusätzlicher Informationen.

Um das ``SettingsBackend`` zu verwenden muss in :file:`cookbook/settings.py`
folgende Einstellung hinzugefügt werden::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'cookbook.userauth.backends.SettingsBackend'
    )

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Authentifizierungs-Alternativen <topics/auth/#other-authentication-sources>`
