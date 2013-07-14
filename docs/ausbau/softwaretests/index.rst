Softwaretests
*************

Ohne Softwaretests wird Softwareentwicklung schwieriger.

Man muss ständig manuell testen, ob ein Feature noch funktioniert. Da aber
jeder anders testet kann man nicht garantieren, dass auch wirklich alle
Features zuverlässig arbeiten. Außerdem ist manuelles Testen sehr
zeitaufwändig.

Softwaretests sind auch gleichzeitig eine Dokumentation, denn sie erklären wie
ein Feature benutzt werden kann.

Django unterstützt mit dem eingebauten Testing Framework vier Arten von Tests:

* Doctests
* Unit Tests
* Funktionale Tests der Views
* GUI Tests mit Selenium

Mit Hilfe eines zusätzlichen Paketes lässt sich auch die Test-Abdeckung
ermitteln.

Bis auf das Testen mit Selenium werden die oben genannten Themen in den
folgenden Kapiteln behandelt.

.. toctree::
   :maxdepth: 2

   tests_ausfuehren
   doctests
   unit_tests
   coverage
   test_organisation
   views_testen

Weiterführende Links zur Django und Python Dokumentation
========================================================

* :djangodocs:`Django Applikationen testen <topics/testing/>`
* `Python unit testing framework <http://docs.python.org/library/unittest.html>`_
