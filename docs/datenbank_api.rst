Die Datenbank API
*****************

Arbeiten mit der Datenbank API
==============================

Den Python Interpreter starten:

..  code-block:: bash

    $ python manage.py shell

..  code-block:: pycon

    >>> from recipes.models import Category, Recipe
    >>> all_recipes = Recipe.objects.all()
    >>> all_recipes
    [<Recipe: Omas beste Frikadellen>, <Recipe: Aglio e Olio>, <Recipe: Bratnudeln auf deutsche Art>]
    >>> all_recipes.count()
    3
    >>> all_recipes[0]
    <Recipe: Omas beste Frikadellen>
    >>> all_recipes[0].title
    u'Omas beste Frikadellen'
    >>> all_recipes[0].number_of_portions
    4

..  code-block:: pycon

    >>> salate = Category(name='Leckere Salate')
    >>> salate.save()
    >>> salate.id
    6
    >>> salate.name
    'Leckere Salate'
    >>> salate.slug
    ''
    >>> from django.template.defaultfilters import slugify
    >>> salate.slug = slugify(salate.name)
    >>> salate.save()
    >>> salate.slug
    u'leckere-salate'

..  code-block:: pycon

    >>> Category.objects.get(pk=23)
    Traceback (most recent call last):
        ...
    DoesNotExist: Category matching query does not exist.
    >>> Category.objects.get(pk=6)
    <Category: Leckere Salate>
    >>> Category.objects.filter(name__startswith='Salate')
    []
    >>> Category.objects.filter(name__startswith='Lecker')
    [<Category: Leckere Salate>]

..  code-block:: pycon

    >>> recipe = all_recipes[0]
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>]
    >>> recipe.category.create(name='Foo')
    <Category: Foo>
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>, <Category: Foo>]
    >>> foo = Category.objects.filter(name='Foo')
    >>> foo
    [<Category: Foo>]
    >>> foo.delete()
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>]

Weiterführende Links zur Django Dokumentation
=============================================

    * `Query API <http://docs.djangoproject.com/en/1.2/topics/db/queries/#topics-db-queries>`_
    * `QuerySet API <http://docs.djangoproject.com/en/1.2/ref/models/querysets/>`_
