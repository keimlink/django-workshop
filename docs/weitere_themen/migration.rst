Datenbank Migration
*******************

South installieren
==================

Um Datenbank Migrationen durchzuführen benötigen wir die App South_::

    $ pip install south

..  _South: http://south.aeracode.org/

Zuerst muss South in die ``INSTALLED_APPS`` eingetragen werden. Außerdem
müssen die Tabellen in der Datenbank für South erzeugt werden::

    $ python manage.py syncdb
    Syncing...
    Creating tables ...
    Creating table south_migrationhistory
    Installing custom SQL ...
    Installing indexes ...
    No fixtures found.

    Synced:
     > django.contrib.auth
     > django.contrib.contenttypes
     > django.contrib.sessions
     > django.contrib.sites
     > django.contrib.messages
     > django.contrib.staticfiles
     > django.contrib.admin
     > recipes
     > debug_toolbar
     > userauth
     > south

    Not synced (use migrations):
     -
    (use ./manage.py migrate to migrate these)

Die bestehenden Apps für die Migration einrichten
=================================================

Dann müssen die bestehenden Apps konvertiert werden, damit diese mit South
arbeiten können::

    $ python manage.py convert_to_south recipes
    Creating migrations directory at '.../cookbook/recipes/migrations'...
    Creating __init__.py in '.../cookbook/recipes/migrations'...
     + Added model recipes.Category
     + Added model recipes.Recipe
     + Added M2M table for category on recipes.Recipe
    Created 0001_initial.py. You can now apply this migration with: ./manage.py migrate recipes
     - Soft matched migration 0001 to 0001_initial.
    Running migrations for recipes:
     - Migrating forwards to 0001_initial.
     > recipes:0001_initial
       (faked)

    App 'recipes' converted. Note that South assumed the application's models
    matched the database (i.e. you haven't changed it since last syncdb); if
    you have, you should delete the recipes/migrations directory, revert
    models.py so it matches the database, and try again.

South hat automatisch die erste Migration :file:`0001_initial.py` für die
App ``recipes`` in :file:`recipes/migrations` angelegt und diese als
ausgeführt gekennzeichnet. Das können wir sehen, in dem wir das folgende
Kommando ausgeführen::

    $ python manage.py migrate --list

     recipes
      (*) 0001_initial

Ein neues Feld zum Model ``Recipes`` hinzufügen
===============================================

Jetzt fügen wir dem Model ``Recipes`` ein neues Feld hinzu, damit wir Rezepte
aktivieren und deaktivieren können::

    class Recipe(models.Model):
        ...
        is_active = models.BooleanField(u'Aktiv')

        class Meta:
            ...

Normalerweise würden wir jetzt das Kommando :program:`syncdb` ausführen. Dazu
müssten wir aber die bestehenden Daten löschen. Das können wir mit South
vermeiden::

    $ python manage.py schemamigration recipes --auto
     + Added field is_active on recipes.Recipe
    Created 0002_auto__add_field_recipe_is_active.py. You can now apply this
    migration with: ./manage.py migrate recipes

South erkennt die Änderung automatisch und erstellt eine neue Migration. Damit
die Migration auch funktioniert müssen wir noch einen Defaultwert für das neue
Feld setzen. Das machen wir in der gerade erzeugten Datei
:file:`0002_auto__add_field_recipe_is_active.py`. Hier ersetzen wir
``default=False`` mit ``default=True``::

    class Migration(SchemaMigration):

        def forwards(self, orm):
            # Adding field 'Recipe.is_active'
            db.add_column('recipes_recipe', 'is_active',
                          self.gf('django.db.models.fields.BooleanField')(default=True),
                          keep_default=False)

Die Migration wurde aber noch nicht angewendet. Das kann man mit dem
``migrate --list`` Befehl sehen::

    $ python manage.py migrate --list

     recipes
      (*) 0001_initial
      ( ) 0002_auto__add_field_recipe_is_active

Also müssen wir als letzten Schritt die Migration auch anwenden::

    $ python manage.py migrate recipes
    Running migrations for recipes:
     - Migrating forwards to 0002_auto__add_field_recipe_is_active.
     > recipes:0002_auto__add_field_recipe_is_active
     - Loading initial data for recipes.
    No fixtures found.

Wenn wir jetzt noch einmal die Migrationen anschauen, können wir sehen, dass
beide ausgeführt wurden::

    $ python manage.py migrate --list

     recipes
      (*) 0001_initial
      (*) 0002_auto__add_field_recipe_is_active

Wir können jetzt den Entwicklungs-Webserver starten und uns die Rezepte
im Admin ansehen. Sie haben ein neues Feld mit dem Namen "Aktiv".

Wenn wir zu der Version der Datenbank ohne das Feld ``is_active`` zurückkehren
wollen, können wir das mit dem folgenden Kommando tun::

    $ python manage.py migrate recipes 0001
     - Soft matched migration 0001 to 0001_initial.
    Running migrations for recipes:
     - Migrating backwards to just after 0001_initial.
     < recipes:0002_auto__add_field_recipe_is_active

Und natürlich geht es auch wieder vorwärts::

    $ python manage.py migrate recipes
    Running migrations for recipes:
     - Migrating forwards to 0002_auto__add_field_recipe_is_active.
     > recipes:0002_auto__add_field_recipe_is_active
     - Loading initial data for recipes.
    No fixtures found.

Für Applikationen, die South für die Migration benutzen, kommen also statt dem
Kommando :program:`syncdb` die Kommandos :program:`schemamigration` und
:program:`migrate` zum Einsatz.
