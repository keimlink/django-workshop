# encoding: utf-8
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase

from ..models import Recipe


class RecipeViewsTests(TestCase):
    """Test the views for the recipes"""
    fixtures = ['test_views_data.json']

    @classmethod
    def setUpClass(cls):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        super(cls, RecipeViewsTests).setUpClass()

    def test_index(self):
        """Test the index view"""
        response = self.client.get(reverse('recipes_recipe_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kochbuch', count=2)
        with self.settings(TEMPLATE_STRING_IF_INVALID='INVALID CONTENT'):
            self.assertNotContains(response,
                'INVALID CONTENT',
                msg_prefix='Missing template variable')
        self.assertTemplateUsed(response, 'recipes/index.html')
        self.assertQuerysetEqual(
            response.context['object_list'],
            Recipe.objects.values_list('slug', flat=True),
            transform=lambda value: value.slug,
            ordered=False
        )

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
        photo_path = os.path.join(settings.BASE_DIR, 'recipes/fixtures/3215317191_209e19288f_t.jpg')
        with open(photo_path) as fp:
            post_data = {
                'title': u'Spätzle',
                'number_of_portions': 4,
                'ingredients': u'Lorem ipsum',
                'preparation': u'Lorem ipsum',
                'difficulty': 2,
                'category': 1,
                'photo': fp,
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
