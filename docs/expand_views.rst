..  _expand_views:

*******************
Expanding the Views
*******************

Although the views are already relatively compact, they still contain
some code that repeats itself. So this something we can improve.

The function ``render_to_response``
===================================

First, we remove the following three imports at the beginning of the file
:file:`recipes/views.py`:

.. literalinclude:: ../src/cookbook/recipes/views.py
    :lines: 1-3

We will replace it with the following import:

.. literalinclude:: ../src/cookbook_improved/recipes/views.py
    :lines: 1

In ``django.shortcuts`` there are several features that are intended to
facilitate the work with the views. One of them is
``render_to_response``.

It takes care of the following things:

* Load the template
* Providing of the context
* Render template with the context
* Return a ``HttpResponse`` that contains the result of the rendering

This allows us to greatly reduce the first function in the view. The
beginning of the file :file:`recipes/views.py` looks now like this:

.. literalinclude:: ../src/cookbook_improved/recipes/views.py
    :lines: 1-8

The function ``get_object_or_404``
==================================

But we also want to simplify the second view function. For this we use
another function that ``django.shortcuts`` provides - it is called
``get_object_or_404``:

.. literalinclude:: ../src/cookbook_improved/recipes/views.py
    :lines: 11-13

The function ``get_object_or_404`` tries to get an instance of the given
model with the manager method ``get``. The second argument ``slug =
slug`` is passed to the ``get`` method. If no appropriate model is
found, a ``Http404`` exception is triggered.

The complete file
=================

.. literalinclude:: ../src/cookbook_improved/recipes/views.py

Further links to the Django documentation
=========================================

- :djangodocs:`Django shortcut functions <topics/http/shortcuts/>`
