********************
An AJAX-based search
********************

AJAX, short for asynchronous JavaScript and XML, is a set of web development
techniques utilizing many web technologies used on the client-side to create
asynchronous web applications. Despite the name, the use of XML is not
required, and we will use JSON to sent and receive the content. Sometimes this
variant is called AJAJ.

JavaScript and the `XMLHttpRequest (XHR)
<https://en.wikipedia.org/wiki/XMLHttpRequest>`_ object provide a method for
exchanging data asynchronously between browser and server to avoid full page
reloads.

The following technologies are incorporated:

* HTML and CSS for presentation
* The Document Object Model (DOM) for dynamic display of and interaction with data
* XML or JSON for the interchange of data
* The XMLHttpRequest object for asynchronous communication
* JavaScript to bring these technologies together

.. note::

    Note that the `same origin policy
    <https://en.wikipedia.org/wiki/Same-origin_policy>`_ prevents some Ajax
    techniques from being used across domains, so you can't send or receive
    content from a different domain.

To simplify the client-side scripting of HTML we will use the cross-platform
JavaScript library `jQuery <https://jquery.com/>`_. jQuery is free, open-source
software licensed under the MIT License. We installed it already together with
the HTML5 Boilerplate.

Generating JSON with a view
===========================

In this chapter we want to build a small search with autocompletion. There
should be an input field, in which you type in the search term. It should,
after the second letter has been entered, fetch recipe titles from the server
and display them below the input field. The recipe titles must be JSON, so we
need a view that generates a JSON. It will be used by the browser to present a
list of choices.

The path component of the URL that is called to get a list of choices should
look like this:

::

    /autocomplete/?term=cake

First, we add the corresponding new URL for the ``autocomplete`` view in
:file:`recipes/urls.py` at the top of ``urlpatterns``:

::

    urlpatterns = [
        url(r'^autocomplete/$', 'recipes.views.autocomplete', name='recipes_recipe_autocomplete'),
        url(r'^recipe/(?P<slug>[-\w]+)/$', 'recipes.views.detail', name='recipes_recipe_detail'),
        url(r'^add/$', 'recipes.views.add', name='recipes_recipe_add'),
        url(r'^edit/(?P<recipe_id>\d+)/$', 'recipes.views.edit', name='recipes_recipe_edit'),
        url(r'^$', 'recipes.views.index', name='recipes_recipe_index'),
    ]

Then we write the appropriate view in :file:`recipes/views.py` that uses the
GET parameter ``term`` to search the database:

::

    import json

    from django.http import HttpResponse

    def autocomplete(request):
        term = request.GET.get('term')
        if term:
            recipes = Recipe.objects.filter(title__icontains=term).order_by('title')
            titles = recipes.values_list('title', flat=True)[:20]
            content = json.dumps(titles, ensure_ascii=False)
        else:
            content = ''
        return HttpResponse(content, mimetype='application/json; charset=utf-8')

If you now call the ``autocomplete`` URL, the titles of all recipes are
displayed as JSON, which contain the word "cake".

For Firefox and Chrome there is the very useful extension `JSONView
<http://jsonview.com/>`_ representing JSON in a coloured tree structure. This
can be very helpful when working with JSON data.

Displaying the search results
=============================

In addition, we need a second view, which then performs the search and displays
the results. This should use the following URL path component:

::

    /search/?term=ko

Add an URL for the view `search` to :file:`recipes/urls.py` right below the
``autocomplete`` URL:

::

    urlpatterns = [
        url(r'^autocomplete/$', 'recipes.views.autocomplete', name='recipes_recipe_autocomplete'),
        url(r'^search/$', 'recipes.views.search', name='recipes_recipe_search'),
        url(r'^recipe/(?P<slug>[-\w]+)/$', 'recipes.views.detail', name='recipes_recipe_detail'),
        url(r'^add/$', 'recipes.views.add', name='recipes_recipe_add'),
        url(r'^edit/(?P<recipe_id>\d+)/$', 'recipes.views.edit', name='recipes_recipe_edit'),
        url(r'^$', 'recipes.views.index', name='recipes_recipe_index'),
    ]

Add the corresponding view to :file:`recipes/views.py`:

::

    def search(request):
        term = request.GET.get('term', '')
        results = Recipe.objects.filter(title__icontains=term).order_by('title')
        return render(request, 'recipes/search.html', {'results': results})

Since this view renders a template, it also requires a template file, namely
:file:`recipes/templates/recipes/search.html`:

.. code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Search{% endblock %}

    {% block content %}
    <h2>Search results</h2>
    <ul>
        {% for recipe in results %}
          <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
        {% empty %}
          <li>No recipes found.</li>
        {% endfor %}
    </ul>
    {% endblock %}

You can test this view already, by visiting
http://127.0.0.1:8000/search/?term=cake, for example. This should display a
list of recipes that contain the letters "cake" in it's title.

Using jQuery for autocompletion
===============================

We will use the JavaScript library jQuery to add the autocompletion
functionality. But we also need `jQuery UI <https://jqueryui.com/>`_, a
collection of GUI widgets, animated visual effects, and themes. It is free,
open-source software licensed under the MIT License like jQuery.

So visit the `jQuery UI download page <https://jqueryui.com/download/>`_. The
latest stable version should already be pre-selected. You should check that the
selected version is compatible with the jQuery version you are using. You can
find out which jQuery version you using by looking at the first line of the
jQuery JavaScript file in :file:`static/js/vendor/`. It should look like this:

::

    /*! jQuery v1.10.1 | (c) 2005, 2013 jQuery Foundation, Inc. | jquery.org/license

To keep the size of the jQuery UI JavaScript file small select only the
components we need for the autocompletion feature. Do the following on the
jQuery UI download page:

#. Below "Components" deselect the "Toggle All" check box
#. Scroll down to "Widgets"
#. Select the check box beside "Autocomplete", all requirements will be selected automatically
#. Scroll down to the "Theme" section
#. Select the "Smoothness" theme
#. Click on the "Download" button

Now unzip the archive you downloaded. After that you have a directory whose
name begins with :file:`jquery-ui`. Move the complete directory into the
directory :file:`static`.

First, we add the new CSS and JavaScript from jQuery UI to the template
:file:`base.html`:

.. code-block:: html+django

    <head>
      ...
      <link rel="stylesheet" href="{% static "jquery-ui-1.11.4.custom/jquery-ui.min.css" %}">
      ...
    </head>
    <body>
      ...
      <script src="{% static "js/vendor/jquery-1.11.2.min.js" %}"></script>
      <script src="{% static "jquery-ui-1.11.4.custom/jquery-ui.min.js" %}"></script>
      ...
    </body>

.. note::

    The name of your jQuery UI directory may be different if you downloaded a
    different version.

.. note::

    It is important that jQuery UI is loaded **after** jQuery.

Then we add the search form to the navigation bar, also in :file:`base.html`:

.. code-block:: html+django

      <form class="navbar-form navbar-left" role="search" action="{% url "recipes_recipe_search" %}">
        <div class="form-group ui-widget">
          <input type="text" class="form-control" placeholder="Search" id="search" name="term">
        </div>
      </form>

Finally, we write the JavaScript code that will send the request for the
autocompletion choices to the server in :file:`static/js/main.js`:

.. code-block:: javascript

    $(function() {
        $("#search").autocomplete({
            source: autocomplete_url,
            minLength: 2
        });
    });

To populate the variable ``autocomplete_url`` used in the JavaScript code
above, we need to add the following line to the template :file:`base.html`:

.. code-block:: html+django

      ...
      <script>
        var autocomplete_url = "{% url "recipes_recipe_autocomplete" %}";
      </script>
      <script src="{% static "js/main.js" %}"></script>
    </body>

.. note::

    The code must be placed **before** :file:`main.js` gets loaded.

Now you can enter the name of a recipe into the search box that already exists
in the database. After you enter the second letter, a list of all recipes
beginning with those letters should appear below the entry field. Now you
either can press Enter to search immediately for all the recipes that contain
the character sequence you entered, or you can select one of the recipe titles
and search only for this recipe.

Extending the search
====================

Here are a few ideas how you could extend this simple search:

* Display the search term on top of the results
* Search also for other fields of the ``Recipe`` model like ``ingredients`` or ``author`` in the view ``search()``

Further links to the Django documentation
=========================================

* :djangodocs:`Serializing Django objects <topics/serialization/>`
* :djangodocs:`The HttpResponse class <ref/request-response/#django.http.HttpResponse>`
