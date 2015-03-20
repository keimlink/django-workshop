# encoding: utf-8
import platform
import unittest

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from django.test import skipIfDBFeature, TestCase
from django.utils import timezone
from freezegun import freeze_time

from recipes.models import Recipe


class RecipeSaveTests(TestCase):
    title = 'Pea soup with sausage'
    number_of_portions = 4

    def setUp(self):
        self.author = User.objects.create_user('testuser', 'test@example.com',
            'testuser')

    def test_date_created_autoset(self):
        """Verifies date_created is autoset correctly."""
        with freeze_time('2014-01-01 10:00:00'):
            recipe = Recipe.objects.create(title=self.title, slug=slugify(self.title),
                number_of_portions=self.number_of_portions, author=self.author)
            self.assertEqual(recipe.date_created, timezone.now())

    def test_slug_is_unique(self):
        """Verifies if a slug is unique."""
        Recipe.objects.create(title=self.title, slug=slugify(self.title),
            number_of_portions=self.number_of_portions, author=self.author)
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(title=self.title, slug=slugify(self.title),
                number_of_portions=self.number_of_portions, author=self.author)

    @skipIfDBFeature('supports_transactions')
    def test_no_transaction(self):
        """Demonstrates skipIfDBFeature decorator."""
        assert False

    @unittest.skipIf(platform.python_version_tuple() > ('2', '6'),
                     'Test runs only with Python 2.5 and lower')
    def test_python_25(self):
        """Demonstrates skipIf decorator."""
        assert False
