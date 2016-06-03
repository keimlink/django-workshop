**************************
Create Recipes with a Form
**************************

Now we want to allow all authenticated users to create recipes in the front end.

Expand URLConf
==============

To do this you first create the corresponding URLs to create and edit recipes
in :file:`recipes/urls.py`:

::

    url(r'^create/$', 'recipes.views.create', name='recipes_recipe_create'),
    url(r'^edit/(?P<recipe_id>\d+)/$', 'recipes.views.edit', name='recipes_recipe_edit'),

The full URLconf looks like this:

::

    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^recipe/(?P<slug>[-\w]+)/$', 'recipes.views.detail', name='recipes_recipe_detail'),
        url(r'^create/$', 'recipes.views.create', name='recipes_recipe_create'),
        url(r'^edit/(?P<recipe_id>\d+)/$', 'recipes.views.edit', name='recipes_recipe_edit'),
        url(r'^$', 'recipes.views.index', name='recipes_recipe_index'),
    ]

Create a form
=============

Next, you create the form. Therefore create the file :file:`recipes/forms.py`:

::

    from django.forms import ModelForm

    from .models import Recipe


    class RecipeForm(ModelForm):
        class Meta:
            model = Recipe
            exclude = ('slug', 'author', 'date_created', 'date_updated')

With the help of ``ModelForm`` you can build a form directly from the model
``Recipe`` and all you have to do is just to specify which fields should not
appear in the form.

Two views of the form
=====================

Now we want to create the views to create and edit recipes in
:file:`recipes/views.py`. At first a few more imports have to be added:

::

    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied
    from django.shortcuts import redirect, render
    from django.template.defaultfilters import slugify

    from .forms import RecipeForm

Then you add the view to create a new recipe:

::

    @login_required
    def create(request):
        if request.method == 'POST':
            form = RecipeForm(request.POST)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.slug = slugify(recipe.title)
                recipe.save()
                form.save_m2m()
                return redirect(recipe)
        else:
            form = RecipeForm()
        context = {'form': form, 'create': True}
        return render(request, 'recipes/form.html', context)

Instead of using the :ref:`already known <using_request_context>` shortcut
``render_to_response()`` we use the new shortcut ``render()``. It was added
with Django 1.3 and  generates the ``RequestContext`` automtically from the
first argument ``request``. The code for ``render_to_response()`` would look
like so:

::

    return render_to_response('recipes/form.html',
        {'form': form, 'create': True}, context_instance=RequestContext(request))

If POST data is available it will be used to create the ``RecipeForm``
instance. Thereafter, it is checked whether the data is valid or not. When the
form is saved the recipe itself is not stored in the database (by setting
``commit=False``), so author and slug can still be defined. Then, at first the
recipe and the many-to-many relations are stored. Finally a redirect to the new
recipe is made. If no POST data is available only an instance of the form is
created.

The parameter ``create`` is used to distinguish later in the template, if a recipe
is just created or created. Because we only use a single template for both
actions. By using the decorator ``login_required`` this view can only be called
by authenticated users.

The second view is used to edit the recipes:

::

    @login_required
    def edit(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe.author != request.user and not request.user.is_staff:
            raise PermissionDenied
        if request.method == 'POST':
            form = RecipeForm(instance=recipe, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(recipe)
        else:
            form = RecipeForm(instance=recipe)
        context = {'form': form, 'create': False, 'object': recipe}
        return render(request, 'recipes/form.html', context)

The id of the recipe is extracted from the URL and passed to the view function
as an argument. It is used a to get an instance or display a 404 page if this
is not possible. If the logged in user is neither the author nor an editor a
403 error appears because the users are only allowed to edit their own recipes.

The rest of the processing of POST data differs only in three points of the
``create()`` view:

#. The ``RecipeForm`` instance is created using the additional keyword argment ``instance=recipe``.
#. The context parameter ``create`` is set to ``False``.
#. In addition, the instance of the recipe is called ``object`` in the context.

Create and expand the templates
===============================

Now we have to create the template. Both views are using the template
:file:`recipes/templates/recipes/form.html`. This is how the template looks
like:

..  code-block:: html+django

    {% extends "base.html" %}

    {% load crispy_forms_tags %}

    {% block title %}
        {{ block.super }} - {% if create %}Create{% else %}
            Edit "{{ object.title }}"{% endif %} recipe
    {% endblock %}

    {% block content %}
        {% if create %}
            <h2>Create recipe</h2>
            {% url 'recipes_recipe_create' as action_url %}
        {% else %}
            <h2>Edit "{{ object.title }}" recipe</h2>
            {% url 'recipes_recipe_edit' object.pk as action_url %}
        {% endif %}
        <form action="{{ action_url }}" method="post" accept-charset="utf-8">
            {{ form|crispy }}
            {% csrf_token %}
            <p><input type="submit" value="Save"/></p>
        </form>
    {% endblock %}

In the template, you can now see how the parameter ``create`` is used to
distinguish between creating and editing.

Now you can expand the template :file:`recipes/templates/recipes/detail.html`
with a link to edit the recipe:

..  code-block:: html+django

    <a href="{% url 'recipes_recipe_edit' object.pk %}">Edit recipe</a>

And add a link to create a recipe to the list template
:file:`recipes/templates/recipes/index.html`:

..  code-block:: html+django

    <a href="{% url 'recipes_recipe_create' %}">Create new recipe</a>

Finished! As a registered user you can now create and edit recipes in the front
end.

If you wish, you can also create the template :file:`403.html` in the template
directory of the project. This will then be displayed instead of the message
"403 Forbidden" if a ``PermissionDenied`` exception is raised.

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Permission denied{% endblock %}

    {% block content %}
        <h2>Permission denied</h2>
        <p>You have insufficient permissions to access this page.</p>
    {% endblock %}

Further links to the Django documentation
=========================================

* :djangodocs:`Forms API <ref/forms/api/>`
* :djangodocs:`Creating forms from models <topics/forms/modelforms/>`
* :djangodocs:`The render shortcut <topics/http/shortcuts/#render>`
* :djangodocs:`The 403 (HTTP Forbidden) view <ref/views/#the-403-http-forbidden-view>`
