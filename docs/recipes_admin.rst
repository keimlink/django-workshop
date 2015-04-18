*********************
The Admin application
*********************

Next, we will enable the admin application so that we can enter, edit and
delete data in our app. This application is already included in Django.

Register your own application to the Admin
==========================================

In order that the admin can be used with our application, we need to make our
models known to the admin. To achieve this you have to edit the file
:file:`recipes/admin.py`. It has been created in the previous chapter when we
created the structure for the ``recipes`` app using the :command:`startapp`
command. Open the file in your editor and add the highlighted line:

.. literalinclude:: ../src/cookbook/recipes/admin.py
    :lines: 1-3
    :emphasize-lines: 3

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

Further links to the Django documentation
=========================================

- :djangodocs:`The Django admin site <ref/contrib/admin/>`
