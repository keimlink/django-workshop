Einführung
**********

Was ist Django?
===============

`Django <http://www.djangoproject.com/>`_ ist ein in `Python
<http://python.org/>`_ geschriebenes **Full Stack Framework**, dass die
schnelle Entwicklung von **Web-Applikationen** ermöglicht. Dabei wird Wert auf
sauberen Code und die **Wiederverwendbarkeit der einzelnen Komponenten**
gelegt.

Benannt wurde das Framework nach dem Gitarristen `Jean „Django“ Reinhardt
<http://de.wikipedia.org/wiki/Django_Reinhardt>`_, der als einer der Begründer
des europäischen Jazz gilt.

Der Quellcode und die `umfangreiche Dokumentation
<http://docs.djangoproject.com/>`_ sind unter einer **BSD-Lizenz** lizensiert.
Die `Django Software Foundation <http://www.djangoproject.com/foundation/>`_
stellt die Weiterentwicklung von Django sicher.

Rapid Development
=================

Django unterstützt durch seine Architektur und Werkzeuge eine schnelle
Entwicklung (**Rapid Development**) von Websites und neuen Komponenten.

Loose Coupling
==============

**Loose Coupling**, also die lose Koppelung der verschiedenen Teile des
Frameworks und der Applikation, stehen bei Django stark im Vordergrund.
Dadurch soll die Qualität und Wiederverwendbarkeit des Codes erhöht werden.

..  _dry:

Don't Repeat Yourself
=====================

Das Prinzip **Don't Repeat Yourself (DRY)** ist wie folgt definiert:

    *Every piece of knowledge must have a single, unambiguous, authoritative
    representation within a system.*
    
    http://c2.com/cgi/wiki?DontRepeatYourself
    
**DRY** ist damit unter anderem eine Vorraussetzung für **Loose Coupling**,
denn Komponenten lassen sich nur dann gut voneinander separieren, wenn man
klar sagen kann welche Aufgaben sie erledigen.

Außerdem erleichtert es die tägliche Arbeit, wenn der Code nicht über
verschiedene Teile der Applikation verteilt ist, sondern dort zu finden ist,
wo man ihn auch erwarten würde.

Model-Template-View
===================

Django ist nach dem **Model-Template-View (MTV)** Muster aufgebaut. **MTV**
orientiert sich am bekannten `Model-View-Controller Muster
<http://de.wikipedia.org/wiki/Model_View_Controller>`_ (MVC).

Der in Django enthaltene **Object Relational Mapper** (ORM) überträgt die
Models in Datenbankstrukturen und führt alle Operationen in der Datenbank
durch. Es können alle gängigen Datenbanken benutzt werden. Alle Models werden
in Python geschrieben.

Die **Template-Engine** unterstützt die Vererbung von Templates und bietet
umfangreiche Filter und Templates. Diese können auch selbst erweitert werden.

Der **View** holt die Daten, zum Beispiel mit Hilfe des **Object Relational
Mappers**. Es können aber auch andere Datenquellen genutzt werden.

Die **URLConf** steuert das Routing. Mit Hilfe von regulären Ausdrücken wird
der Request dem richtigen View zugewiesen.

..  _grafik_request_response:

..  digraph:: request_response

    label = "Schematische Darstellung einer Request / Response Verarbeitung"
    {rank=same; "Browser" "Webserver"}
    {rank=same; "URLConf" "View"}
    "Browser" -> "Webserver" [label="Request"];
    "Webserver" -> "URLConf" [label="Request"];
    "URLConf" -> "View" [label="Request"];
    "View" -> "Model (ORM)" -> "Datenbank"-> "Model (ORM)" -> "View"
    "View" -> "Template" [label="Context"];
    "Template" -> "Tags & Filter" -> "Template"
    "Template" -> "View" [label="HTML"];
    "View" -> "Webserver" [label="Response"];
    "Webserver" -> "Browser" [label="Response"];

Eingebauter Entwicklungs-Webserver
==================================

Der in Django enthaltene **Entwicklungs-Webserver** hilft bei der Entwicklung,
da nicht extra ein "vollwertiger" Webserver installiert werden muss.

Die Admin-Applikation
=====================

Django stellt mit der **Admin-Applikation** ein `CRUD
<http://de.wikipedia.org/wiki/CRUD>`_-Interface bereit, mit dem sich eine
Website ohne Aufwand pflegen läßt. Die **Admin-Applikation** wird mit Hilfe
der Models automatisch erstellt.
