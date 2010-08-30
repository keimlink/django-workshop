# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
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