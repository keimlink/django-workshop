*********************
The Admin application
*********************

Next, we will enable the admin application so that we can enter, edit
and delete data in our app.

This application is already included in Django.

Register your own application to the Admin
==========================================

In order that the admin can be used with our application, we need to
make our models known to the admin.

This requires the file :file:`admin.py` to be created in the
application. The project will then look like this::

    cookbook
    |-- cookbook
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    |-- manage.py
    |-- recipes
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- models.py
    |   |-- tests.py
    |   `-- views.py
    |-- static
    `-- templates

Then you open the file in your editor and add the following two lines of code:

.. literalinclude:: ../src/cookbook/recipes/admin.py
    :lines: 1-3

The ``admin`` module and the ``models`` of the application are now available.

.. note::

    The second ``import`` is a relative import. These were defined in
    :pep:`328` and introduced in Python 2.6.

Next, we create a class in order to register the model ``Category`` with
the admin:

.. literalinclude:: ../src/cookbook/recipes/admin.py
    :lines: 6-9, 14

There is nothing else to do.

The attribute ``prepopulated_fields`` helps the admin application to
fill the field ``slug`` automatically as you type. In this case, the
``name`` attribute of the model is used.

That's what we do now for the model ``Recipe``:

.. literalinclude:: ../src/cookbook/recipes/admin.py
    :lines: 10-13, 15

The complete file
-----------------

The file :file:`admin.py` should look like this:

.. literalinclude:: ../src/cookbook/recipes/admin.py
    :linenos:

Activate the admin application
==============================

To activate the admin application, two steps are necessary.

Customizing the configuration
-----------------------------

In the file :file:`settings.py` remove the comment before the line
``'django.contrib.admin'`` in ``INSTALLED_APPS`` to enable the admin
application.

Customize URLconf
-----------------

Thus the admin application can also be accessed in the browser we must
also enable the URL of the admin.

Jump to the file :file:`cookbook/urls.py` and uncomment the emphasized
lines. Then the file looks like this:

.. literalinclude:: ../src/cookbook/cookbook/urls.py
    :lines: 1, 3-18
    :emphasize-lines: 4, 5, 16
    :linenos:

Further links to the Django documentation
=========================================

- :djangodocs:`The Django admin site <ref/contrib/admin/>`
