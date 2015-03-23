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

.. command-output:: python manage.py migrate --list
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

The migration has not yet been applied. You can see this by running the
:command:`migrate --list` command again, but now just for the `recipes` app:

.. command-output:: python manage.py migrate --list recipes
    :cwd: ../src/cookbook_migrations

So you need to apply the migration as a last step:

.. command-output:: python manage.py migrate
    :cwd: ../src/cookbook_migrations

Migrations are simple Python files. Let's have a look at the migrate you created:

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

You can now start the development web server and view the recipes in the admin,
where you see the new field named "active".

If you want to go back to the version of the database without the field
``is_active``, you can use the following command to do so:

.. command-output:: python manage.py migrate recipes 0001
    :cwd: ../src/cookbook_migrations

And of course the migration can be moved forward again:

.. command-output:: python manage.py migrate recipes
    :cwd: ../src/cookbook_migrations

Further links to the Django documentation
=========================================

* :djangodocs:`Migrations <topics/migrations/>`
