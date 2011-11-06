..  _datenbank-api:

Die Datenbank API
*****************

Django bringt eine Datenbank API mit, die Objekte erstellen, lesen, schreiben
und löschen kann.

Arbeiten mit der Datenbank API
==============================

Ein Weg mit der Datenbank API zu Arbeiten ist der Python Interpreter. Mit dem
folgenden Befehl kannst du diesen starten:

..  code-block:: bash

    $ python manage.py shell

Dieser Befehl lädt die Einstellungen aus :file:`settings.py` für das aktuelle
Projekt, was beim Start durch die Eingabe von :program:`python` nicht
passieren würde.

..  code-block:: pycon

    # Importieren der Models
    >>> from recipes.models import Category, Recipe

    # Ein QuerySet mit allen Rezepten
    >>> all_recipes = Recipe.objects.all()
    >>> all_recipes
    [<Recipe: Omas beste Frikadellen>, <Recipe: Aglio e Olio>, <Recipe: Bratnudeln auf deutsche Art>]
    # all_recipes ist ein QuerySet
    >>> type(all_recipes)
    <class 'django.db.models.query.QuerySet'>
    >>> all_recipes.count()
    3

    # Betrachten eines Rezepts
    >>> all_recipes[0]
    <Recipe: Omas beste Frikadellen>
    >>> all_recipes[0].title
    u'Omas beste Frikadellen'
    >>> all_recipes[0].number_of_portions
    4

    # Eine neue Kategorie
    >>> salate = Category(name='Leckere Salate')
    >>> salate.save()
    >>> salate.id
    6
    >>> salate.name
    'Leckere Salate'
    >>> salate.slug
    ''

    # Den Slug füllen
    >>> from django.template.defaultfilters import slugify
    >>> salate.slug = slugify(salate.name)
    >>> salate.save()
    >>> salate.slug
    u'leckere-salate'

    # Wenn eine Model nicht gefunden wird, wird immer eine DoesNotExist Exception ausgelöst
    >>> Category.objects.get(pk=23)
    Traceback (most recent call last):
        ...
    DoesNotExist: Category matching query does not exist.

    # Ein einziges Objekt holen
    >>> Category.objects.get(pk=6)
    <Category: Leckere Salate>

    # Filter benutzen
    >>> Category.objects.filter(name__startswith='Salate')
    []
    # Es wird ein QuerySet zurückgegeben
    >>> Category.objects.filter(name__startswith='Lecker')
    [<Category: Leckere Salate>]
    # So kann man direkt das Objekt bekommen
    >>> Category.objects.filter(name__startswith='Lecker')[0]
    <Category: Leckere Salate>
    # Auch auf ein QuerySet kann ein Filter angewendet werden
    >>> categories = Category.objects.all()
    >>> categories.filter(title__startswith='Lecker')
    [<Category: Leckere Salate>]

    # Die Kategorie benutzen, um auf die Rezepte zuzugereifen
    >>> categories[0]
    <Category: Nudeln und Pasta>
    >>> type(categories[0].recipe_set)
    <class 'django.db.models.fields.related.ManyRelatedManager'>
    >>> categories[0].recipe_set.all()
    [<Recipe: Aglio e Olio>, <Recipe: Bratnudeln auf deutsche Art>]

    # Über die Relation eines Rezepts eine Kategorie anlegen
    >>> recipe = all_recipes[0]
    # Zwei Kategorien am Model
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>]
    >>> recipe.category.create(name='Foo')
    <Category: Foo>
    # Jetzt sind es drei Kategorien
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>, <Category: Foo>]
    # Die neu angelegte Kategorie wieder löschen
    >>> foo = Category.objects.filter(name='Foo')
    >>> foo
    [<Category: Foo>]
    >>> foo.delete()
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>]

    # Komplexe Abfragen mit Q Objekten
    # Die folgende Abfrage verknüpft beide Bedingungen mit "AND"
    >>> Recipe.objects.filter(number_of_portions=4).filter(title__startswith='Oma')
    []
    # Mit einem Q Objekt kann man eine "ODER" Verknüpfung realisieren
    >>> Recipe.objects.filter(Q(number_of_portions=4) | Q(title__startswith='Oma'))
    [<Recipe: Aprikosenknödel>, <Recipe: Omas beste Frikadellen>, <Recipe: Aglio e Olio>, <Recipe: Bratnudeln auf deutsche Art>]

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Query API <topics/db/queries/#topics-db-queries>`
* :djangodocs:`QuerySet API <ref/models/querysets/>`
