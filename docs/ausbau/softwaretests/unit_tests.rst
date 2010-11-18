Unit Tests schreiben
********************

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
            self.author = User.objects.create_user('testuser', 'test@example.com',
                'testuser')

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
=================================

Vorteile
--------

* Ausgabe beim Ausführen der Tests ist eindeutiger
* Jeder Test kann einzeln aufgerufen werden
* Eindeutig vom Quellcode getrennt (kann auch ein Nachteil sein)
* Weniger Abhängigkeiten von der Umgebung (da nicht der Python-Interpreter benutzt wird)
* Jede Methode einer Test-Klasse wird automatisch innerhalb einer Transaktion aufgerufen
* Keine Unicode-Probleme

Nachteile
---------

* Erstellen der Unit Tests erfordert mehr Aufwand als das Erstellen von Doctests
* Auch eine Dokumentation des Quellcodes, aber nicht so offensichtlich wie beim Doctest