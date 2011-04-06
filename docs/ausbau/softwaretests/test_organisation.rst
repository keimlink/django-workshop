Die Tests als Paket organisieren
********************************

Da die Menge der Tests meist so gross ist, dass eine Datei für alle Test
schnell unübersichtlich wird, ist es sinnvoll die Tests als Python Paket zu
organisieren.

Erstelle dazu ein Verzeichnis :file:`tests` und darin die Datei
:file:`__init__.py`::

    $ cd recipes
    $ mkdir tests
    $ touch tests/__init__.py

Nun verschiebst du die Datei :file:`tests.py` in das neue Verzeichnis und
benennst sie in :file:`model_tests.py` um::

    $ mv tests.py tests/model_tests.py

Als nächstes löscht du noch den Bytecode der Datei :file:`tests.py`, damit
dieser nicht die Ausführung des Codes im Paket ``tests`` verhindert::

    $ rm tests.pyc

Zuletzt fügst du folgenden Code in die Datei :file:`recipes/tests/__init__.py`
ein, damit unsere Tests aus dem Modul ``model_tests`` auch geladen werden::

    from model_tests import RecipeSaveTest, __test__