Fehlerbehandlung
****************

.. todo:: Translate chapter

HTTP-Statuscode 404 (Not Found)
===============================

Immer wenn ein URL aufgerufen wird, der nicht durch die URLConf verarbeitet
werden kann oder wenn ein View eine ``Http404`` Exception auslöst, wird der in
``handler404`` definierte View aufgerufen.

Dies passiert aber nur, wenn ``DEBUG`` auf ``False`` gesetzt ist. Hat
``DEBUG`` den Wert ``True`` wird der in ``handler404`` definierte View nicht
aufgerufen, sondern ein Hinweisseite mit weiteren Informationen angezeigt.

Der ``handler404`` ist per Default ``django.views.defaults.page_not_found``.
Dieser View erwartet, dass in der Wurzel des Template-Verzeichnisses ein
Template mit dem Namen :file:`404.html` existiert, um dieses zu rendern.

Der View übergibt die Variable ``request_path`` an das Template, welchen den
URL enthält, der den 404 Fehler erzeugte. Außerdem kann über den Context auf
Variablen wie ``MEDIA_URL`` zugegriffen werden.

Existiert diese Datei nicht, so wird eine ``Http500`` Exception ausgelöst.

HTTP-Statuscode 500 (Internal Server Error)
===========================================

Eine ``Http500`` Exception wird immer dann ausgelöst, wenn beim Ausführen des
Codes Fehler auftreten. Hat ``DEBUG`` den Wert ``True``, wird der Traceback
sowie weitere Debug-Informationen angezeigt.

Ist ``DEBUG`` aber auf ``False`` gesetzt wird der in ``handler500`` definierte
View aufgerufen, welcher per Default ``django.views.defaults.server_error``
ist. Dieser rendert das Template :file:`500.html`, dass in der Wurzel des
Template-Verzeichnisses erwartet wird.

Das Template :file:`500.html` hat einen leeren Context und es sind keine
Variablen gesetzt.

Templates für die Fehlerbehandlung anlegen
==========================================

Testen kannst du diese Templates, indem du ``DEBUG`` in
:file:`local_settings.py` auf ``False`` setzt und einen URL aufrufst, der
nicht existiert.

Ganz ohne die beiden Templates siehst du die Meldung "A server error occurred.
Please contact the administrator.". Exception und Stack Trace siehst du auf der
Konsole.

Legt du jetzt die Datei :file:`500.html` im Template Verzeichnis im
Projektverzeichnis an, wird dieses Template gerendert und der Stack Trace
verschwindet auf der Konsole.

Das `HTML5 Boilerplate <http://de.html5boilerplate.com/>`_, dass du
schon im Kapitel :ref:`staticfiles` benutzt hast, enthält auch eine
fertige 404 Seite. Um diese zu nutzen kopierst du die Datei
:file:`404.html` aus dem HTML5 Boilerplate Verzeichnis in das Template
Verzeichnis im Projektverzeichnis. Wenn du jetzt den nicht existierenden
URL aufrufst, siehst du diese Seite,

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Anpassung der Views für Fehler <topics/http/views/#customizing-error-views>`
