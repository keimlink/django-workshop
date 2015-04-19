***************
The first Views
***************

After you have created some records using the admin the next step is to
display them also in the frontend. Therefore you have do three things:

    #. Define URLs
    #. Write views
    #. Create templates

..  note::

    See :ref:`Illustration: Schematic Diagram of Django's
    Request/Response Processing <request_response_graph>`

Define URLs
===========

First we define the URLs that are used for calling the different views.
For now, we want to create two URLs. Jump to the file :file:`urls.py`
and add at the end of ``urlpatterns`` the following two lines:

.. literalinclude:: ../src/cookbook/cookbook/urls.py
    :linenos:
    :emphasize-lines: 12-13

..  note::

    The first argument of the ``url()`` function is a `raw string
    <http://docs.python.org/reference/lexical_analysis.html#string-literals>`_,
    which contains a regular expression.

    If you encounter regular expressions for the first time, you can
    learn more about it in the `Regular-Expression-HOWTO
    <http://docs.python.org/howto/regex.html>`_, on `Regular Expressions.info
    <http://www.regular-expressions.info/>`_ or in the `article by Doug
    Hellmann about the re-Modul <http://www.doughellmann.com/PyMOTW/re/>`_.
    At `RegexPlanet <http://www.regexplanet.com/advanced/python/index.html>`_
    you can test regular expressions directly in the browser.

Now you start the development server:

.. literalinclude:: runserver.log

Calling the URL http://127.0.0.1:8000/ shows a ``ViewDoesNotExist``
Exception. That's right, because until now you still have no view
written. But it shows that your URL works.

How to render a template?
=========================

Before we write the first views we want to look how Django templates are
rendered.

Django templates are simple Python objects whose constructor expectes a
string. With the help of a context object the placeholders in the
template are replaced by the desired values.

The first example shows how to use a dictionary as a data structure:

::

    $ python manage.py shell

.. note::

    The command :program:`shell` loads the settings from
    :file:`settings.py` for the current project, which would not happen
    if you had simply typed :program:`python`.

.. doctest::

    >>> from django.template import Context, Template
    >>> t = Template('My name is {{ person.first_name }}.')
    >>> d = {'person': {'first_name': 'Alice'}}
    >>> t.render(Context(d))
    u'My name is Alice.'

In the second example, we use a simple Python object as a data structure:

.. doctest::

    >>> class Person: pass
    ...
    >>> p = Person()
    >>> p.first_name = 'Bob'
    >>> c = Context({'person': p})
    >>> t.render(c)
    u'My name is Bob.'

Lists can also be used:

.. doctest::

    >>> t = Template('First article: {{ articles.0 }}')
    >>> c = Context({'articles': ['bread', 'eggs', 'milk']})
    >>> t.render(c)
    u'First article: bread'

Write the first view
====================

So now the views have to be created. You want to display the data that
is retrieved from the database using the ORM. For this you open the file
:file:`recipes/views.py`.

Most views return a ``HttpResponse`` object. So we write a very simple
view, which does this:

.. testcode::

    from django.http import HttpResponse


    def index(request):
        return HttpResponse('My first view.')

.. testcode::
    :hide:

    print index(None).content

.. testoutput::
    :hide:

    My first view.

After you have saved the view and called http://127.0.0.1:8000/
you'll see the string that you passed to the ``HttpResponse`` object. So
a ``HttpResponse`` always expects a string as first argument.

Now we will replace the string with a ``Template`` and render it with a
``Context`` which contains a ``Recipe`` object. The ``HttpResponse``
will then return the string rendered by the ``Template``:

.. literalinclude:: ../src/cookbook/recipes/views.py
    :lines: 2-12

If you now call http://127.0.0.1:8000/ a ``TemplateDoesNotExist``
exception is raised. Sure - you didn't create the template yet.

Create Templates
================

First you need a basic template for your website. Create the file
:file:`base.html` in the :file:`templates` directory with the following
content:

.. literalinclude:: ../src/cookbook/templates/base.html
    :language: html+django

It contains HTML and two **blocks**. These will be filled by the other
templates which derive from this template.

Within the application, you have to create two directories for the
templates, namely :file:`recipes/templates/recipes`. In it you create
the file :file:`index.html`:

.. literalinclude:: ../src/cookbook/recipes/templates/recipes/index.html
    :language: html+django

Now your directory structure should look like this:

::

    cookbook
    |-- cookbook
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    |-- default.db
    |-- manage.py
    |-- media
    |-- recipes
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- migrations
    |   │   |-- 0001_initial.py
    |   │   `-- __init__.py
    |   |-- fixtures
    |   |   `-- initial_data.json
    |   |-- models.py
    |   |-- templates
    |   |   `-- recipes
    |   |       `-- recipe.html
    |   |-- tests.py
    |   `-- views.py
    |-- static
    `-- templates
        `-- base.html

After you have started the development web server you should now see a
list of recipes if you call http://127.0.0.1:8000/.

Add the second view
===================

Thus the detail view of the recipes work, a second view must are written.

First you need an additional import at the beginning of the file
:file:`views.py`:

.. literalinclude:: ../src/cookbook/recipes/views.py
    :lines: 1

At the end of the file comes a new function for the new view:

.. literalinclude:: ../src/cookbook/recipes/views.py
    :lines: 15-22

The entire file now looks like this:

.. literalinclude:: ../src/cookbook/recipes/views.py
    :linenos:

Create a second template
========================

Now only the second template is missing: :file:`recipes/detail.html`.
Put it in the same directory as :file:`recipes/index.html`:

.. literalinclude:: ../src/cookbook/recipes/templates/recipes/detail.html
    :language: html+django

Now you can also view all the details of the recipes by clicking on the
links on the index page.

Why does the template engine hide variables that do not exist?
==============================================================

If a variable is not defined as key in the context, this is ignored by
the Django template engine. This is mainly makes sense in the production
environemnt, since as the site despite the absence of another variable
can be rendered.

To see anyway, if a variable has not been rendered, one can define the option
``string_if_invalid`` for Django's template backend in the configuration
:file:`settings.py` which in this case appears:

::

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'string_if_invalid': 'TEMPLATE NAME ERROR: %s not found',
            },
        },
    ]

This setting should be disabled again in a production environment.

Escaping of HTML and JavaScript
===============================

For safety reasons the Django template engine escapes all HTML and
JavaScript that is in the context. Suppose a user uses the following
text in the field "preparation" of a recipe:

::

    <script>alert('The best recipe in the world!')</script>
    Heat the water in the pot to 100 °C.

Then this HTML would be generated:

..  code-block:: html

    <p>&lt;script&gt;alert(&#39;The best recipe in the <world!&#39;)&lt;/script&gt;</p>
    <p>Heat the water in the pot to 100 °C.</p>

The JavaScript code would therefore not be executed.

It is also possible to remove HTML tags completely. To do this you'd
have to use the ``striptags`` filter in the template:

..  code-block:: html+django

    <h3>Preparation</h3>
    {{ object.preparation|striptags|linebreaks }}

Now the HTML looks like this:

..  code-block:: html

    <p>alert(&#39;The best recipe in the world!&#39;)</p>
    <p>Heat the water in the pot to 100 °C.</p>

Are you sure, however, that HTML or JavaScript should be rendered and
possibly be executed, you can use the ``safe`` filter to explicitly
allow this:

..  code-block:: html+django

    <h3>Preparation</h3>
    {{ object.preparation|safe|linebreaks }}

Now actually the JavaScript is executed as desired by the user:

..  code-block:: html

    <p><script>alert('The best recipe in the world!')</script></p>
    <p>Heat the water in the pot to 100 °C.</p>

.. note::

    This allows of course `XSS attacks
    <https://en.wikipedia.org/wiki/Cross-site_scripting>`_ and should
    therefore be used with caution.


Further links to the Django documentation
=========================================

- :djangodocs:`URL dispatcher <topics/http/urls/>`
- :djangodocs:`Writing views <topics/http/views/>`
- :djangodocs:`The Django template language <topics/templates/>`
- :djangodocs:`Automatic HTML escaping <ref/templates/language/#automatic-html-escaping>`
- :djangodocs:`The Django template language: For Python programmers <ref/templates/api/>`
