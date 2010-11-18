Softwaretests
*************

Ohne Softwaretests wird Softwareentwicklung schwieriger.

Man muss ständig manuell testen, ob ein Feature noch funktioniert. Da aber
jeder anders testet kann man nicht garantieren, dass auch wirklich alle
Feature zuverlässig funktionieren. Außerdem ist manuelles Testen sehr
zeitaufwändig.

Softwaretests sind auch gleichzeitig eine Dokumentation, denn sie erklären wie
ein Feature benutzt werden kann.

Django unterstützt mit dem eingebauten Testing Framework drei Arten von Tests:

* Doctests
* Unit Tests
* Funktionale Tests der Views

Mit Hilfe eines zusätzlichen Paketes lässt sich auch die Test-Abdeckung
ermitteln.

Diese Themen werden in den folgenden Kapiteln behandelt.

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

* `Django Applikationen testen <http://docs.djangoproject.com/en/1.2/topics/testing/>`_
* `Python unit testing framework <http://docs.python.org/library/unittest.html>`_
