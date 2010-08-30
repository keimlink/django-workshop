Softwaretests
*************

Ohne Softwaretests wird Softwareentwicklung schwieriger.

Man muss ständig manuell testen, ob ein Feature noch funktioniert. Da aber jeder anders testet kann man nicht garantieren, dass auch wirklich alle Feature zuverlässig funktionieren. Außerdem ist manuelles Testen sehr zeitaufwändig.

Softwaretests sind auch gleichzeitig eine Dokumentation, denn sie erklären wie ein Feature benutzt werden kann.

Django unterstützt mit dem eingebauten Testing Framework drei Arten von Tests:

* Doctests
* Unit Tests
* Funktionale Tests der Views

Mit Hilfe eines zusätzlichen Paketes lässt sich auch die Test-Abdeckung ermitteln.

Tests starten
=============

In Django ist bereits ein Framework für Softwaretests integriert - das "Python unit testing framework".

Der Test Runner erstellt bei jeden Start eine SQLite Datenbank für die Tests und lässt alle Tests voneinander abgekapselt in Transaktionen laufen. Bei der Auswahl des Datenbanksystems richtet sich der Test Runner nach dem Backend, der in der ``settings.py`` konfiguriert wurde.

Tests für alle Applikationen durchführen
----------------------------------------

Mit dem Befehl ``python manage.py test`` werden alle für das Projekt installierten Applikationen getestet::

    $ python manage.py test
    Creating test database 'default'...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table recipes_category
    Creating table recipes_recipe_category
    Creating table recipes_recipe
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for recipes.Recipe_category model
    Installing index for recipes.Recipe model
    No fixtures found.
    ..............................................................................................................................................................
    ----------------------------------------------------------------------
    Ran 158 tests in 3.406s

    OK
    Destroying test database 'default'...

Tests für eine Applikation durchführen
--------------------------------------

Man kann auch gezielt eine Applikation testen::

    $ python manage.py test recipes
    Creating test database 'default'...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table recipes_category
    Creating table recipes_recipe_category
    Creating table recipes_recipe
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for recipes.Recipe_category model
    Installing index for recipes.Recipe model
    No fixtures found.
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.097s

    OK
    Destroying test database 'default'...

Ausgabe der Tests verändern
---------------------------

Mit dem Parameter ``-v 0`` wird der Großteil der Ausgaben des Test Runners unterdrückt::

    $ python manage.py test recipes -v 0
    ----------------------------------------------------------------------
    Ran 2 tests in 0.007s

    OK

Umgekehrt kannst du mit dem Parameter ``-v 2`` alle Details beim Ablaufen der Tests beobachten::

    $ python manage.py test recipes -v 2
    Creating test database 'default'...
    Processing auth.Permission model
    Creating table auth_permission
    ...
    Running post-sync handlers for application auth
    Adding permission 'auth | permission | Can add permission'
    Adding permission 'auth | permission | Can change permission'
    Adding permission 'auth | permission | Can delete permission'
    ...
    No custom SQL for auth.Permission model
    ...
    Installing index for auth.Permission model
    ...
    Loading 'initial_data' fixtures...
    ...
    No fixtures found.
    test_basic_addition (recipes.tests.SimpleTest) ... ok
    Doctest: recipes.tests.__test__.doctest ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.008s

    OK
    Destroying test database 'default'...

Doctests schreiben
==================

Doctests sind die einfachste Art Tests zu schreiben. Starte dafür eine Python Shell und führe einige Operationen an der Datenbank durch, ähnlich wie im Kapitel :ref:`datenbank-api`.

..  code-block:: pycon

    $ python manage.py shell
    Python 2.6.1 (r261:67515, Feb 11 2010, 00:51:29) 
    [GCC 4.2.1 (Apple Inc. build 5646)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from recipes.models import Recipe
    >>> title = 'Doctest'
    >>> from django.template.defaultfilters import slugify
    >>> from django.contrib.auth.models import User
    >>> admin = User.objects.get(username='admin')
    >>> r = Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    >>> r.title
    'Doctest'
    >>> r.slug
    u'doctest'
    >>> r.number_of_portions
    4
    >>> r.author
    <User: admin>
    >>> import datetime
    >>> r.date_created.date() == datetime.datetime.now().date()
    True
    >>> r.date_updated.date() == datetime.datetime.now().date()
    True
    >>> r.difficulty == Recipe.DIFFICULTY_MEDIUM
    True

Die gerade durchgeführten Operationen haben ein neues Rezept erstellt und einige Attribute getestet.

Jetzt wollen wir noch einige Fehler provozieren:

..  code-block:: pycon

    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    Traceback (most recent call last):
      ...
    IntegrityError: column slug is not unique
    >>> title = 'Doctest 2'
    >>> Recipe.objects.create(title=title, slug=slugify(title))
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.number_of_portions may not be NULL
    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4)
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.author_id may not be NULL

Damit sind wir mit der Erstellung der Doctests fertig. Du musst den Code aus der Shell jetzt nur noch in die Datei ``recipes/tests.py`` kopieren. Und zwar als Ersatz für den einfachen Beispiel-Doctest::

    __test__ = {"doctest": """
    Another way to test that 1 + 1 is equal to 2.

    >>> 1 + 1 == 2
    True
    """}

Da der Benutzer "admin" in der Testdatenbank nicht existiert musst du ihn manuell während des Tests erstellen. Ersetze dazu die Zeile::

    >>> admin = User.objects.get(username='admin')

mit folgendem Code::

    >>> admin = User.objects.create(username='admin', password='admin')

Die Datei ``recipes/tests.py`` sieht dann so aus::

    """
    This file demonstrates two different styles of tests (one doctest and one
    unittest). These will both pass when you run "manage.py test".

    Replace these with more appropriate tests for your application.
    """

    from django.test import TestCase

    class SimpleTest(TestCase):
        def test_basic_addition(self):
            """
            Tests that 1 + 1 always equals 2.
            """
            self.failUnlessEqual(1 + 1, 2)

    __test__ = {"doctest": """
    >>> from recipes.models import Recipe
    >>> title = 'Doctest'
    >>> from django.template.defaultfilters import slugify
    >>> from django.contrib.auth.models import User
    >>> admin = User.objects.create(username='admin', password='admin')
    >>> r = Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    >>> r.title
    'Doctest'
    >>> r.slug
    u'doctest'
    >>> r.number_of_portions
    4
    >>> r.author
    <User: admin>
    >>> import datetime
    >>> r.date_created.date() == datetime.datetime.now().date()
    True
    >>> r.date_updated.date() == datetime.datetime.now().date()
    True
    >>> r.difficulty == Recipe.DIFFICULTY_MEDIUM
    True
    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    Traceback (most recent call last):
      ...
    IntegrityError: column slug is not unique
    >>> title = 'Doctest 2'
    >>> Recipe.objects.create(title=title, slug=slugify(title))
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.number_of_portions may not be NULL
    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4)
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.author_id may not be NULL
    """}

..  note::

    Die Details der Tracebacks werden wirklich durch den String "..." ersetzt.

Jetzt kannst du mit dem Kommando ``python manage.py test recipes -v 2`` die Tests laufen lassen und sehen, dass die Doctests ausgeführt werden. Mit ``python manage.py test recipes.doctest -v 2`` kannst du auch nur die Doctests alleine aufrufen.

Vor- und Nachteile von Doctests
-------------------------------

Vorteile
^^^^^^^^

* Einfach zu Erstellen
* Gleichzeitig Dokumentation des Codes
* Tests sind dort, wo sich auch der Quellcode befindet

Nachteile
^^^^^^^^^

* Dokumentation kann zu umfangreich werden (kann durch Verschieben in die Testsuite umgangen werden)
* Ausgabe beim Ausführen der Tests nicht immer eindeutig
* Abhängigkeiten von der Umgebung (zum Beispiel Ausgaben im Interpreter)
* Datenbank-Operationen sind nicht in Transaktionen gekapselt
* Unicode-Probleme

Unit Tests schreiben
====================

Mit Hilfe des "Python unit testing frameworks" kannst du klassenbasierte Unit Tests schreiben.

Ersetzte den folgenden Teil der Datei ``recipes/tests.py``::

    """
    This file demonstrates two different styles of tests (one doctest and one
    unittest). These will both pass when you run "manage.py test".

    Replace these with more appropriate tests for your application.
    """

    from django.test import TestCase

    class SimpleTest(TestCase):
        def test_basic_addition(self):
            """
            Tests that 1 + 1 always equals 2.
            """
            self.failUnlessEqual(1 + 1, 2)

mit diesem Code::

    # -*- coding: utf-8 -*-
    
    import datetime

    from django.contrib.auth.models import User
    from django.db import IntegrityError
    from django.template.defaultfilters import slugify
    from django.test import TestCase
    
    from recipes.models import Recipe
    
    class RecipeSaveTest(TestCase):
        title = u'Erbsensuppe mit Würstchen'
        number_of_portions = 4

        def setUp(self):
            self.author = User.objects.create(username='testuser',
                password='testuser')

        def testDateCreatedAutoset(self):
            """Verify date_created is autoset correctly"""
            recipe = Recipe.objects.create(title=self.title, slug=slugify(self.title),
                number_of_portions=self.number_of_portions, author=self.author)
            now = datetime.datetime.now()
            self.assertEqual(recipe.date_created.date(), now.date())
            self.assertEqual(recipe.date_created.hour, now.hour)
            self.assertEqual(recipe.date_created.minute, now.minute)

        def testSlugIsUnique(self):
            """Verify if a slug is unique"""
            Recipe.objects.all().delete()
            Recipe.objects.create(title=self.title, slug=slugify(self.title),
                number_of_portions=self.number_of_portions, author=self.author)
            self.assertRaises(IntegrityError, Recipe.objects.create,
                title=self.title, slug=slugify(self.title),
                number_of_portions=self.number_of_portions, author=self.author)

Der Kommentar ``# -*- coding: utf-8 -*-`` zu Beginn der Datei ist bei Python 2.x Code nötig, damit Zeichen außerhalb der ASCII-Tabelle benutzt werden können.

Die Methode ``setUp`` wird vor dem Aufruf jeder Testmethode der Testklasse aufgerufen. In diesem Fall legt sie einen neuen Benutzer zum Testen an.

Danach folgen zwei Tests, die zwei Features des ``Recipe`` Models testen.

Du kannst diese Tests mit den schon gezeigten Kommandos starten oder gezielt nur diese Testklasse mit dem folgenden Kommando aufrufen::

    $ python manage.py test recipes.RecipeSaveTest

Vor- und Nachteile von Unit Tests
---------------------------------

Vorteile
^^^^^^^^

* Ausgabe beim Ausführen der Tests ist eindeutiger
* Jeder Test kann einzeln aufgerufen werden
* Eindeutig vom Quellcode getrennt (kann auch ein Nachteil sein)
* Weniger Abhängigkeiten von der Umgebung (da nicht der Python-Interpreter benutzt wird)
* Jede Methode einer Test-Klasse wird automatisch innerhalb einer Transaktion aufgerufen
* Keine Unicode-Probleme

Nachteile
^^^^^^^^^

* Erstellen der Unit Tests erfordert mehr Aufwand als das Erstellen von Doctests
* Auch eine Dokumentation des Quellcodes, aber nicht so offensichtlich wie beim Doctest

Test-Abdeckung ermitteln
========================

Natürlich ist es auch wichtig zu wissen, für welche Teile der Applikation schon Tests geschrieben wurden. Dabei hilft das Python Paket `coverage <http://nedbatchelder.com/code/coverage/>`_. Bis jetzt wurde es noch nicht in Django integriert und muss daher manuell installiert werden::

    $ pip install coverage

Damit ``coverage`` auch nur unsere Applikationen und nicht das Framework selbst betrachtet legst du die Datei ``.coveragerc`` mit folgendem Inhalt im Projektverzeichnis an::

    [report]
    omit = /path/to/.virtualenvs

Jetzt kannst du mit dem folgenden Kommando die Daten für den Coverage-Report der Applikation ``recipes`` erzeugen::

    $ coverage run manage.py test recipes

Die Daten kannst auf der Shell mit diesem Befehl ausgeben::

    $ coverage report -m

Einen HTML-Coverage-Report kannst du mit diesem Befehl erstellen::

    $ coverage html

Die HTML-Dateien befinden sich dann im Verzeichnis ``htmlcov``.

Die Tests als Paket organisieren
================================

Da die Menge der Tests meist so gross ist, dass eine Datei für alle Test schnell unübersichtlich wird, ist es sinnvoll die Tests als Python Paket zu organisieren.

Erstelle dazu ein Verzeichnis ``tests`` und darin die Datei ``__init__.py``::

    $ cd recipes
    $ mkdir tests
    $ touch tests/__init__.py

Nun verschiebst du die Datei ``tests.py`` in das neue Verzeichnis und benennst sie in ``model_tests.py`` um::

    $ mv tests.py tests/model_tests.py

Als nächstes löscht du noch den Bytecode der Datei ``tests.py``, damit dieser nicht die Ausführung des Codes im Paket ``tests`` verhindert::

    $ rm tests.pyc

Zuletzt fügst du folgenden Code in die Datei ``recipes/tests/__init__.py`` ein, damit unsere Tests aus dem Modul ``model_tests`` auch geladen werden::

    from model_tests import RecipeSaveTest, __test__

Views testen
============

Natürlich möchte man auch gerne das Frontend der Applikation testen. Dafür gibt es zum Beispiel Werkzeuge wie `Selenium <http://selenium.openqa.org/>`_. Selenium lässt sich mit Hilfe von `django-sane-testing <http://devel.almad.net/trac/django-sane-testing/>`_ in Django integrieren.

Mit dem in Django eingebauten Testclient steht ein einfacher Testbrowser zur Verfügung, der zwar nicht alle Features von Selenium bietet, aber dafür auch einfacher einzusetzen ist.

Wir werden einige Tests mit dem Testbrowser erstellen.

Fixtures erstellen
------------------

Zuerst benötigen wir einige Fixtures, damit Daten im Frontend zum Testen zur Verfügung stehen.

Erstelle dazu das Verzeichnis ``fixtures`` für die Applikationen ``recipes`` und ``userauth``::

    $ mkdir recipes/fixtures
    $ mkdir userauth/fixtures

Dann erstellst du eine JSON-Datei mit den Models jeder Applikation::

    $ python manage.py dumpdata recipes --indent 4 > recipes/fixtures/view_tests_data.json
    $ python manage.py dumpdata auth --indent 4 > userauth/fixtures/test_users.json

Mit dem folgenden Kommando können wir diese Fixtures in einen Testserver laden und uns im Browser ansehen::

    $ python manage.py testserver view_tests_data.json test_users.json
    Creating test database 'default'...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table recipes_category
    Creating table recipes_recipe_category
    Creating table recipes_recipe
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for recipes.Recipe_category model
    Installing index for recipes.Recipe model
    No fixtures found.
    Installing json fixture 'view_tests_data' from '/Users/zappi/Projekte/Python/cookbook/recipes/fixtures'.
    Installing json fixture 'test_users' from '/Users/zappi/Projekte/Python/cookbook/userauth/fixtures'.
    Installed 43 object(s) from 2 fixture(s)
    Validating models...
    0 errors found

    Django version 1.2.1, using settings 'cookbook.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Tests für die Rezept-Views schreiben
------------------------------------

Damit die Frontend-Tests auch geladen werden müssen sie in ``recipes/tests/__init__.py`` importiert werden::

    from view_tests import RecipeViewsTests

Nun erstellst du die Datei ``recipes/tests/view_tests.py`` mit folgendem Inhalt::

    # -*- coding: utf-8 -*-

    from django.core.urlresolvers import reverse
    from django.test import TestCase

    from recipes.models import Recipe

    class RecipeViewsTests(TestCase):
        """Test the views for the recipes"""
        fixtures = ['view_tests_data.json', 'test_users.json']

        def test_index(self):
            """Test the index view"""
            response = self.client.get(reverse('recipes_recipe_index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Kochbuch', count=2)
            self.assertNotContains(response, 'Cookbook',
                msg_prefix='Found untranslated string in response')
            self.assertTemplateUsed(response, 'recipes/index.html')
            self.assertEqual(map(repr, response.context['object_list']),
                map(repr, Recipe.objects.all()))

Die Funktion ``reverse`` importieren wir, damit wir die Namen der URLs auch auflösen können und diese nicht "hart" in den Test eintragen müssen.

Mit dem vom Testbrowser erzeugten Response-Objekt führen wir dann die Tests durch. Wir können sowohl das generierte HTML, die verwendeten Templates als auch den Kontext testen.

Um die Testsuite für das Frontend zu erweitern kannst du noch den folgenden Import::

    from django.template.defaultfilters import slugify

und diese Testmethoden zur Klasse ``RecipeViewsTests`` hinzufügen::

    def test_detail(self):
        """Test the detail view"""
        recipe = Recipe.objects.all()[2]
        response = self.client.get(recipe.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.title, count=2,
            msg_prefix='The response must contain the recipe title two times')
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertEqual(response.context['object'], recipe)

    def test_detail_404(self):
        """Test a detail view with a missing recipe"""
        response = self.client.get(reverse('recipes_recipe_detail',
            kwargs={'slug': 'missing_recipe'}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'recipes/detail.html')
        self.assertTemplateUsed(response, '404.html')

    def test_add(self):
        """Test the add view which requires a login"""
        username = password = 'admin'
        login = self.client.login(username=username, password=password)
        self.assertTrue(login, 'Login as "%s" using password "%s" failed.' %
            (username, password))
        add_url = reverse('recipes_recipe_add')
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)
        post_data = {
            'title': u'Spätzle',
            'number_of_portions': 4,
            'ingredients': u'Lorem ipsum',
            'preparation': u'Lorem ipsum',
            'difficulty': 2,
            'category': 1
        }
        response = self.client.post(add_url, post_data)
        redirect_url = reverse('recipes_recipe_detail',
            kwargs={'slug': slugify(post_data['title'])})
        self.assertRedirects(response, redirect_url)
        self.assertTemplateNotUsed(response, 'recipes/form.html')

    def test_add_302(self):
        """Test the add view without an authenticated user"""
        self.client.logout()
        response = self.client.get(reverse('recipes_recipe_add'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'recipes/form.html')

Die letzten beiden Tests ``test_add`` und ``test_add_302`` demonstrieren das Versenden von POST-Daten mit dem Testbrowser, um die Formulare und die Authentifizierung zu testen.

Die Frontend-Tests können gezielt mit diesem Befehl aufgerufen werden::

    $ python manage.py test recipes.RecipeViewsTests

Weitere Möglichkeiten beim Testen von Views
-------------------------------------------

* HTTP Methoden ``HEAD``, ``OPTIONS``, ``PUT`` und ``DELETE`` nutzen
* ``Client.session`` und ``Client.cookies`` bilden die Sitzungsdaten ab
* ``Client.template`` führt eine Liste aller gerenderten Templates
* ``TestCase`` stellt mit ``django.core.mail.outbox`` ein Mock-Outbox zum Testen des E-Mail-Versands zur Verfügung
* Jede Test-Klasse kann eine eigene URLConf haben

Weiterführende Links zur Django und Python Dokumentation
========================================================

* `Django Applikationen testen <http://docs.djangoproject.com/en/1.2/topics/testing/>`_
* `Python unit testing framework <http://docs.python.org/library/unittest.html>`_
