from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from .models import Recipe


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        filtering = {
            'username': ALL,
        }


class RecipeResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author')

    class Meta:
        queryset = Recipe.objects.all()
        resource_name = 'recipe'
        authorization = Authorization()
        filtering = {
            'title': ('exact', 'startswith', 'icontains', 'contains'),
            'number_of_portions': ALL,
            'author': ALL_WITH_RELATIONS,
        }
