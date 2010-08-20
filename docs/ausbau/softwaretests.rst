Softwaretests
*************

Tests für alle Applikationen durchführen
========================================

::

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
======================================

::

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
===========================

::

    $ python manage.py test recipes -v 0
    ----------------------------------------------------------------------
    Ran 2 tests in 0.007s

    OK

::

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

Der Benutzer "admin" existiert nicht in der Testdatenbank, daher funktioniert der Doctest so nicht.

::

    admin = User.objects.create(username='admin', password='admin')

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

Fixtures erstellen
------------------

::

    $ mkdir recipes/fixtures
    $ python manage.py dumpdata auth --indent 4 > recipes/fixtures/initial_data.json

::

    # coding: utf-8
    
    import datetime

    from django.contrib.auth.models import User
    from django.db import IntegrityError
    from django.template.defaultfilters import slugify
    
    from recipes.models import Recipe
    
    class RecipeSaveTest(TestCase):
        title = u'Erbsensuppe mit Würstchen'
        number_of_portions = 4

        def setUp(self):
            # self.author = User.objects.get(username='admin')
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

::

    $ pip install coverage

Datei .coveragerc erstellen::

    [report]
    omit = /path/to/.virtualenvs

::

    $ coverage run manage.py test recipes
    $ coverage report -m
    $ coverage html

Die Tests als Package organisieren
==================================

::

    $ cd recipes
    $ mkdir tests
    $ touch tests/__init__.py
    $ mv tests.py tests/model_tests.py
    $ rm tests.pyc

recipes/tests/__init__.py::

    from model_tests import RecipeSaveTest, __test__

Views testen
============

Fixtures erstellen
------------------

::

    $ python manage.py dumpdata recipes --indent 4 > recipes/fixtures/view_tests_data.json

Tests für die Rezept-Views schreiben
------------------------------------

recipes/tests/__init__.py::

    from view_tests import RecipeViewsTests

::

    $ python manage.py testserver view_tests_data.json

recipes/tests/view_tests.py::

    # coding: utf-8

    from django.core.urlresolvers import reverse
    from django.template.defaultfilters import slugify
    from django.test import TestCase

    from recipes.models import Recipe

    class RecipeViewsTests(TestCase):
        """Test the views for the recipes"""
        fixtures = ['view_tests_data.json']

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

        def test_detail(self):
            """Test the detail view"""
            recipe = Recipe.objects.all()[0]
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
            """Test the add view without an autheticated user"""
            self.client.logout()
            response = self.client.get(reverse('recipes_recipe_add'))
            self.assertEqual(response.status_code, 302)
            self.assertTemplateNotUsed(response, 'recipes/form.html')

::

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

* `Django Applikationen testen <http://docs.djangoproject.com/en/dev/topics/testing/>`_
* `Python Unit testing framework <http://docs.python.org/library/unittest.html>`_
