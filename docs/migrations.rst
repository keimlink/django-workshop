*******************
Database Migrations
*******************

Install South
=============

To perform database migrations we need to install `South <http://south.aeracode.org/>`_ ::

    $ pip install south

First South must be added to the ``INSTALLED_APPS`` setting. In addition
the database tables for South must be generated::

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

Setting up the existing apps for migration
==========================================

Now the existing apps need to be converted so that they can work with South::

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

South has automatically created the first migration :file:`0001_initial.py` for the
App ``recipes`` in the directory :file:`recipes/migrations` and marked it as
executed. That we can see when we run the following command::

    $ python manage.py migrate --list

     recipes
      (*) 0001_initial

Add a new field to the model ``recipes``
========================================

Now we add a new field to the model ``recipes``, so that we can enable
and disable recipes::

    class Recipe(models.Model):
        ...
        is_active = models.BooleanField('active')

        class Meta:
            ...

Normally we would now execute the command :program:`syncdb`. To do that
we would have to delete the existing data. With South we can avoid
this::

    $ python manage.py schemamigration recipes --auto
     + Added field is_active on recipes.Recipe
    Created 0002_auto__add_field_recipe_is_active.py. You can now apply this
    migration with: ./manage.py migrate recipes

South detects the change automatically and creates a new migration. In
order to make the migration work, we need to set a default value for the
new field. We do this in the file
:file:`0002_auto__add_field_recipe_is_active.py` which just has been
created. Here we replace ``default = False`` with ``default = True``::

    class Migration(SchemaMigration):

        def forwards(self, orm):
            # Adding field 'Recipe.is_active'
            db.add_column('recipes_recipe', 'is_active',
                          self.gf('django.db.models.fields.BooleanField')(default=True),
                          keep_default=False)

The migration has not yet been applied. This can seen by running the
``migrate --list`` command::

    $ python manage.py migrate --list

     recipes
      (*) 0001_initial
      ( ) 0002_auto__add_field_recipe_is_active

So we also need to apply the migration as a last step::

    $ python manage.py migrate recipes
    Running migrations for recipes:
     - Migrating forwards to 0002_auto__add_field_recipe_is_active.
     > recipes:0002_auto__add_field_recipe_is_active
     - Loading initial data for recipes.
    No fixtures found.

If we now have another look at the migrations, we can see that
both were carried out::

    $ python manage.py migrate --list

     recipes
      (*) 0001_initial
      (*) 0002_auto__add_field_recipe_is_active

We can now start the development web server and view the recipes
in the admin where we see the new field named "active".

If we want to go back to the version of the database without the field
``is_active``, we can use the following command to do so::

    $ python manage.py migrate recipes 0001
     - Soft matched migration 0001 to 0001_initial.
    Running migrations for recipes:
     - Migrating backwards to just after 0001_initial.
     < recipes:0002_auto__add_field_recipe_is_active

And of course the migration can be moved forward again::

    $ python manage.py migrate recipes
    Running migrations for recipes:
     - Migrating forwards to 0002_auto__add_field_recipe_is_active.
     > recipes:0002_auto__add_field_recipe_is_active
     - Loading initial data for recipes.
    No fixtures found.

Applications that use South to migrate, use :program:`schemamigration`
and :program:`migrate` instead of :program:`syncdb`. There is also a way
to run both commands at once with :program:`syncdb --migrate`.
