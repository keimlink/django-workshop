..  _migrations:

*******************
Database Migrations
*******************

Prior to version 1.7, Django only supported adding new models to the database.
It was not possible to alter or remove existing models via the
:command:`syncdb` command. Most people were using `South
<http://south.aeracode.org/>`_ to apply changes to their database.

Displaying all existing migrations
==================================

Use the :command:`migrate` command to display all existing migrations:

.. command-output:: python manage.py showmigrations
    :cwd: ../src/cookbook_migrations

Adding a new field to the model ``Recipe``
===========================================

Now add a new field to the ``Recipe`` model in :file:`recipes/models.py`, so
that you can enable and disable recipes:

.. literalinclude:: ../src/cookbook_migrations/recipes/models.py
    :lines: 44-49
    :emphasize-lines: 3

After that execute the :command:`makemigrations` command to create the a new
migration:

.. command-output:: python manage.py makemigrations
    :cwd: ../src/cookbook_migrations

The new migration is created by scanning and comparing to the versions
currently contained in your migration files to your :file:`recipes/models.py`.
But it has not yet been applied. You can see this by running the
:command:`showmigrations` command again, but now just for the `recipes` app:

.. command-output:: python manage.py showmigrations recipes
    :cwd: ../src/cookbook_migrations

So you need to apply the migration as a last step:

.. command-output:: python manage.py migrate
    :cwd: ../src/cookbook_migrations

You can now start the development web server and view the recipes in the admin,
where you see the new field named "active".

If you want to go back to the version of the database without the field
``is_active``, you can use the following command to do so:

.. command-output:: python manage.py migrate recipes 0001
    :cwd: ../src/cookbook_migrations

And of course the migration can be moved forward again:

.. command-output:: python manage.py migrate recipes
    :cwd: ../src/cookbook_migrations

Understanding migrations
========================

Migrations are simple Python files. Let's have a look at the migration you created:

.. Because the migration for the new is_active field is created when the
.. document gets rendered it can't be included using literalinclude.

::

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import models, migrations


    class Migration(migrations.Migration):

        dependencies = [
            ('recipes', '0001_initial'),
        ]

        operations = [
            migrations.AddField(
                model_name='recipe',
                name='is_active',
                field=models.BooleanField(default=True, verbose_name=b'active'),
                preserve_default=True,
            ),
        ]

You can see that the ``Migration`` class has two attributes:

* The ``operations`` attribute that defines a list of operations to be executed
* The ``dependencies`` attribute that defines a list of migrations this migration depends on

The operation that is executed here is quite clear: A new field is added to the
table. More important are the dependencies: This migration depends on the first
migration of the recipes app. So if you try to run this migration, migration
``0001_initial`` will be executed if has not been run before.

Therefore the migrations framework has to build a directed graph of all basic
migrations in memory before any migration can be executed. Furthermore the
state of every migration is tracked in a special database table, so that it's
known which migrations have been applied and which not.

If we take a look at the dependencies of the first migration, on which the
second migration depends, we see that it also has dependencies, but to a
different app:

.. literalinclude:: ../src/cookbook_migrations/recipes/migrations/0001_initial.py
    :lines: 1-12

It means that all migrations of the app managing the user model (which is
``django.contrib.auth`` by default) have to be run before the initial migration
of the recipes app can be executed.

Further links to the Django documentation
=========================================

* :djangodocs:`Migrations <topics/migrations/>`
* :djangodocs:`Migration Operations <ref/migration-operations/>`
