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

