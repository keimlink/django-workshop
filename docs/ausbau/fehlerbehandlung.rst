Fehlerbehandlung
****************

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

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Anpassung der Views für Fehler <topics/http/views/#customizing-error-views>`
