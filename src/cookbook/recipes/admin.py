from django.contrib import admin

from recipes.models import Category, Recipe

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
