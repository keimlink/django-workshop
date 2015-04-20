..  _templatetags:

************
Templatetags
************

Django's template tags are good to work with. But what's really interesting is
the possibility to write your own template tags.

We want to write a template tag for our project, with which we can determine
whether a user is the author of a recipe. In addition, it should provide the
ability to render an alternative block, if this is not the case.

The template tag should look like this:

..  code-block:: html+django

    {% is_author user recipe %}
        The user is owner of this recipe or a staff member.
    {% else %}
        The user has no permissions to edit this recipe.
    {% endis_author %}

The name of the template tag is ``is_author``. The first argument ``user`` is a
``User`` object. The second argument ``recipe`` is a ``Recipe`` instance.
Otherwise, the template tag should work like an ``if`` condition.

The directory structure for template tags
=========================================

Template tags must be created with a specific directory structure. In the
application directory :file:`recipes` a new directory :file:`templatetags`
needs to be created. In this directory an empty file :file:`__init __ py` has
to be created to mark the directory as Python package. Finally, we create a
Python file that is the module for our template tags: :file:`recipes.py`.

::

    recipes
    `-- templatetags
        |-- __init__.py
        `-- recipes.py

Create the template tag
=======================

A template tag always consists of a parser and a node. The parser walks through the
template and collects the tags. As a result, it returns instances of nodes.
Nodes have a ``render()`` method that generates the output.

The Parser
----------

First you create the parser in the file :file:`recipes.py` you just created:

..  code-block:: python

    from django import template

    register = template.Library()

    @register.tag(name='is_author')
    def do_is_author(parser, token):
        """The ``{% is_author %}`` tag displays the first section, if the user is
        the author of the recipe or a staff member. Otherwise the second section
        is displayed.

        ::

            {% is_author user recipe %}
                The user is owner of this recipe or a staff member.
            {% else %}
                The user has no permissions to edit this recipe.
            {% endis_author %}
        """
        try:
            tag_name, user, recipe = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                '%s requires a Recipe and an User as arguments' % token.contents.split()[0])
        nodelist_true = parser.parse(('else', 'endis_author'))
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('endis_author',))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()
        return IsAuthorNode(user, recipe, nodelist_true, nodelist_false)

The Renderer
------------

Then you write the node that renders the output. This code must stand above the
function ``do_is_author()``, otherwise the class ``IsAuthorNode`` is not
available inside the function.

..  code-block:: python

    class IsAuthorNode(template.Node):
        def __init__(self, user, recipe, nodelist_true, nodelist_false):
            self.user = template.Variable(user)
            self.recipe = template.Variable(recipe)
            self.nodelist_true = nodelist_true
            self.nodelist_false = nodelist_false

        def render(self, context):
            try:
                user = self.user.resolve(context)
                recipe = self.recipe.resolve(context)
            except template.VariableDoesNotExist:
                return ''
            if recipe.author.id == user.id or user.is_staff:
                return self.nodelist_true.render(context)
            else:
                return self.nodelist_false.render(context)

Use the template tag
====================

Now you can use the new template tag, for example in the template
:file:`recipes/templates/recipes/detail.html`.

At first our template tag must be loaded. The best place to do this is the head
of the template:

..  code-block:: html+django

    {% load recipes %}

..  note::

    The identifier behind the ``load`` template tag is always the name of the
    Python module that contains the template tags that are to be loaded
    (without the ".py" ending). The Python module must be in the directory
    :file:`templatetags` of an application listed in ``INSTALLED_APPS``.

Then you replace the line:

..  code-block:: html+django

    <a href="{% url 'recipes_recipe_edit' object.pk %}">Edit recipe</a>

With the new template tag:

..  code-block:: html+django

    {% is_author user object %}
        <a href="{% url 'recipes_recipe_edit' object.pk %}">Edit recipe</a>
    {% else %}
        To edit this recipe please <a href="{% url 'userauth_login' %}">log in</a>
            as author of the recipe or as editor.
    {% endis_author %}

Django apps for easy writing of template tags
=============================================

Since the writing of template tags is quite cumbersome with Django's standard
tools, various Django apps have been created to simplify it. An overview is the
`Templatetags Grid <http://www.djangopackages.com/grids/g/templatetags/>`_ on
Django Packages. Two of the most popular template tag apps are `django-classy-
tags <http://pypi.python.org/pypi/django-classy-tags/>`_ and `django-ttag
<http://pypi.python.org/pypi/django-ttag>`_.

Further links to the Django documentation
=========================================

* :djangodocs:`Writing custom template tags <howto/custom-template-tags/#writing-custom-template-tags>`
