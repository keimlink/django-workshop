..  _datenbank-api:

Die Datenbank API
*****************

Django bringt eine Datenbank API mit, die Objekte erstellen, lesen, schreiben
und löschen kann.

Backup und Einspielen der Fixtures
==================================

Damit du alle Operationen durchführen kannst benötigst du exakt die gleichen
Daten. Also musst du zuerst ein Backup deiner Daten machen, deine Daten löschen
und dann die Fixtures importieren. Am Ende spielst du dann dein Backup wieder
ein.

..  note::

    Du benötigst das Programm `sqlite3 <https://www.sqlite.org/>`_, um den
    Befehl :program:`dbshell` nutzen zu können.

Das Backup erstellst du so:

..  code-block:: bash

    $ python manage.py dumpdata > backup.json

Nun kannst du die gesamte Datenbank löschen:

..  code-block:: bash

    $ python manage.py sqlflush | python manage.py dbshell

Bevor du die Daten importieren kannst muss wieder ein Superuser angelegt werden:

..  code-block:: bash

    $ python manage.py createsuperuser
    Username (leave blank to use 'vagrant'): admin
    E-mail address: admin@example.com
    Password:
    Password (again):
    Superuser created successfully.

Jetzt importierst du die Daten, die du im Mercurial-Repository dieses Projekts
`findest <https://bitbucket.org/keimlink/django-workshop/raw/bdabf8fb9e5d/src/e
rste_schritte/cookbook/recipes/fixtures/initial_data.json>`_.

..  code-block:: bash

    $ wget -O import.json https://bitbucket.org/keimlink/django-workshop/raw/bdabf8fb9e5d/src/erste_schritte/cookbook/recipes/fixtures/initial_data.json
    $ python manage.py loaddata import.json
    Installed 9 object(s) from 1 fixture(s)

Arbeiten mit der Datenbank API
==============================

Ein Weg mit der Datenbank API zu Arbeiten ist der Python Interpreter. Mit dem
folgenden Befehl kannst du diesen starten:

..  code-block:: bash

    $ python manage.py shell

..  code-block:: pycon

    # Importieren der Models
    >>> from recipes.models import Category, Recipe

    # Ein QuerySet mit allen Rezepten
    >>> all_recipes = Recipe.objects.all()
    >>> all_recipes
    [<Recipe: Bärlauchstrudel>, <Recipe: Kohleintopf mit Tortellini>,
        <Recipe: Käsespiegelei auf Spinatnudeln>]
    # all_recipes ist ein QuerySet
    >>> type(all_recipes)
    <class 'django.db.models.query.QuerySet'>
    >>> all_recipes.count()
    3

    # Ausgabe aller Feldnamen eines Models
    >>> Recipe._meta.get_all_field_names()
    ['author', 'category', 'date_created', 'date_updated', 'difficulty', 'id',
        'ingredients', 'number_of_portions', 'preparation', 'slug',
        'time_for_preparation', 'title']


    # Betrachten eines Rezepts
    >>> all_recipes[1]
    <Recipe: Kohleintopf mit Tortellini>
    >>> all_recipes[1].title
    u'Kohleintopf mit Tortellini'
    >>> all_recipes[1].number_of_portions
    4

    # Eine neue Kategorie
    >>> salate = Category(name='Leckere Salate')
    >>> salate.id
    >>> salate.save()
    >>> salate.id
    7
    >>> salate.name
    'Leckere Salate'
    >>> salate.slug
    ''

    # Den Slug füllen
    >>> from django.template.defaultfilters import slugify
    >>> slugify(salate.name)
    u'leckere-salate'
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
    >>> Category.objects.get(pk=7)
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
    >>> categories.filter(name__startswith='Lecker')
    [<Category: Leckere Salate>]

    # Eine Kategorie benutzen, um auf die Rezepte zuzugereifen
    >>> categories[1]
    <Category: Pasta>
    >>> type(categories[1].recipe_set)
    <class 'django.db.models.fields.related.ManyRelatedManager'>
    >>> categories[1].recipe_set.all()
    [<Recipe: Kohleintopf mit Tortellini>, <Recipe: Käsespiegelei auf Spinatnudeln>]

    # Über die Relation eines Rezepts eine Kategorie anlegen
    >>> recipe = all_recipes[0]
    # Drei Kategorien am Model
    >>> recipe.category.all()
    [<Category: Fleisch>, <Category: Backen>, <Category: Frühling>]
    >>> recipe.category.create(name='Foo')
    <Category: Foo>
    # Jetzt sind es vier Kategorien
    >>> recipe.category.all()
    [<Category: Hauptspeise>, <Category: Party>, <Category: Foo>]
    # Die neu angelegte Kategorie wieder löschen
    >>> foo = Category.objects.filter(name='Foo')
    >>> foo
    [<Category: Foo>]
    >>> foo.delete()
    >>> recipe.category.all()
    [<Category: Fleisch>, <Category: Backen>, <Category: Frühling>]

    # Komplexe Abfragen mit Q Objekten
    # Ein einfacher Filter
    >>> Recipe.objects.filter(number_of_portions=4)
    [<Recipe: Bärlauchstrudel>, <Recipe: Kohleintopf mit Tortellini>]

    # Alle Rezepte, die nicht dem Kriterium entsprechen
    >>> Recipe.objects.exclude(number_of_portions=4)
    [<Recipe: Käsespiegelei auf Spinatnudeln>]

    # Die folgende Abfrage verknüpft beide Filer mit "AND"
    >>> Recipe.objects.filter(number_of_portions=4).filter(title__startswith='K')
    [<Recipe: Kohleintopf mit Tortellini>]

    # Mit einem Q Objekt kann man eine "ODER" Verknüpfung realisieren
    >>> from django.db.models import Q
    >>> Recipe.objects.filter(Q(number_of_portions=4) | Q(title__startswith='K'))
    [<Recipe: Bärlauchstrudel>, <Recipe: Kohleintopf mit Tortellini>,
        <Recipe: Käsespiegelei auf Spinatnudeln>]

Die Testdaten löschen und das Backup einspielen
===============================================

Jetzt löscht du die Testdaten:

..  code-block:: bash

    $ python manage.py sqlflush | python manage.py dbshell

Und lädst dein Backup:

..  code-block:: bash

    $ python manage.py loaddata backup.json
    Installed 57 object(s) from 1 fixture(s)

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Query API <topics/db/queries/#topics-db-queries>`
* :djangodocs:`QuerySet API <ref/models/querysets/>`
