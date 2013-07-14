Views testen
************

Natürlich möchte man auch gerne das Frontend der Applikation testen. Dafür
gibt es zum Beispiel Werkzeuge wie `Selenium <http://seleniumhq.org/>`_.

Mit dem in Django eingebauten Testclient steht ein einfacher Testbrowser zur
Verfügung, der zwar nicht alle Features von Selenium bietet, aber dafür auch
einfacher einzusetzen ist.

Wir werden einige Tests mit dem Testbrowser erstellen.

Fixtures erstellen
==================

Zuerst benötigen wir einige Fixtures, damit Daten im Frontend zum Testen zur
Verfügung stehen.

Erstelle dazu das Verzeichnis :file:`fixtures` für die Applikationen ``recipes``
und ``userauth``::

    $ mkdir recipes/fixtures
    $ mkdir userauth/fixtures

Dann erstellst du eine JSON-Datei mit den Models jeder Applikation::

    $ python manage.py dumpdata recipes --indent 4 > recipes/fixtures/view_tests_data.json
    $ python manage.py dumpdata auth --indent 4 > userauth/fixtures/test_users.json

Mit dem folgenden Kommando können wir diese Fixtures in einen Testserver laden
und uns im Browser ansehen::

    $ python manage.py testserver view_tests_data.json test_users.json
    Creating test database for alias 'default'...
    Installed 43 object(s) from 2 fixture(s)
    Validating models...

    0 errors found
    Django version 1.3.1, using settings 'cookbook.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Tests für die Rezept-Views schreiben
====================================

Damit die Frontend-Tests auch geladen werden müssen sie in
:file:`recipes/tests/__init__.py` importiert werden::

    from view_tests import RecipeViewsTests

Nun erstellst du die Datei :file:`recipes/tests/view_tests.py` mit folgendem
Inhalt::

    # -*- coding: utf-8 -*-

    from django.core.urlresolvers import reverse
    from django.test import TestCase

    from ..models import Recipe

    class RecipeViewsTests(TestCase):
        """Test the views for the recipes"""
        fixtures = ['view_tests_data.json', 'test_users.json']

        def test_index(self):
            """Test the index view"""
            response = self.client.get(reverse('recipes_recipe_index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Kochbuch', count=2)
            with self.settings(TEMPLATE_STRING_IF_INVALID='INVALID CONTENT'):
                self.assertNotContains(response,
                    settings.TEMPLATE_STRING_IF_INVALID,
                    msg_prefix='Missing template variable')
            self.assertTemplateUsed(response, 'recipes/index.html')
            self.assertEqual(
                [recipe.slug for recipe in response.context['object_list']],
                [recipe.slug for recipe in Recipe.objects.all()]
            )


Die Funktion ``reverse`` importieren wir, damit wir die Namen der URLs auch
auflösen können und diese nicht "hart" in den Test eintragen müssen.

Mit dem vom Testbrowser erzeugten Response-Objekt führen wir dann die Tests
durch. Wir können sowohl das generierte HTML, die verwendeten Templates als
auch den Kontext testen.

Um die Testsuite für das Frontend zu erweitern kannst du noch den folgenden
Import::

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

    def test_add_login_required(self):
        """Test the add view without an authenticated user"""
        response = self.client.get(reverse('recipes_recipe_add'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'recipes/form.html')

Die letzten beiden Tests ``test_add`` und ``test_add_302`` demonstrieren das
Versenden von POST-Daten mit dem Testbrowser, um die Formulare und die
Authentifizierung zu testen.

Die Frontend-Tests können gezielt mit diesem Befehl aufgerufen werden::

    $ python manage.py test recipes.RecipeViewsTests

Weitere Möglichkeiten beim Testen von Views
===========================================

* HTTP Methoden ``HEAD``, ``OPTIONS``, ``PUT`` und ``DELETE`` nutzen
* ``Client.session`` und ``Client.cookies`` bilden die Sitzungsdaten ab
* ``Client.template`` führt eine Liste aller gerenderten Templates
* ``TestCase`` stellt mit ``django.core.mail.outbox`` ein Mock-Outbox zum
  Testen des E-Mail-Versands zur Verfügung
* Jede Test-Klasse kann eine eigene URLConf haben
