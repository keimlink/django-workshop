Rezepte mit einem Formular hinzufügen
*************************************

URLConf erweitern
=================

recipes/urls.py::

    url(r'^erstellen/$', 'add', name='recipes_recipe_add'),
    url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),
    

Die vollständige URLConf::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('recipes.views',
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
        url(r'^erstellen/$', 'add', name='recipes_recipe_add'),
        url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),
        url(r'^$', 'index', name='recipes_recipe_index'),
    )

Ein Formular erstellen
======================

recipes/forms.py::

    from django.forms import ModelForm
    from django.template.defaultfilters import slugify

    from recipes.models import Recipe

    class RecipeForm(ModelForm):
        class Meta:
            model = Recipe
            exclude = ('slug', 'author', 'date_created', 'date_updated')

        def __init__(self, **kwargs):
            try:
                self.__user = kwargs.pop('user')
            except KeyError:
                self.__user = None
            super(RecipeForm, self).__init__(**kwargs)

        def save(self, commit=True):
            if self.instance.pk is None:
                if self.__user is None:
                    raise TypeError("You didn't give an user argument to the constructor.")
                self.instance.slug = slugify(self.instance.title)
                self.instance.author = self.__user
            return super(RecipeForm, self).save(commit)

Zwei Views für das Formular
===========================

recipes/views.py

imports::

    from django.contrib.auth.decorators import login_required
    from django.http import HttpResponseForbidden, HttpResponseRedirect
    from django.template.defaultfilters import slugify
    from recipes.forms import RecipeForm

views::

    @login_required
    def add(request):
        if request.method == 'POST':
            form = RecipeForm(user=request.user, data=request.POST)
            if form.is_valid():
                recipe = form.save()
                return HttpResponseRedirect(recipe.get_absolute_url())
        else:
            form = RecipeForm(user=request.user)
        return render_to_response('recipes/form.html',
            {'form': form, 'add': True},
            context_instance=RequestContext(request))

    @login_required
    def edit(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe.author != request.user and request.user.is_staff == False:
            return HttpResponseForbidden()
        if request.method == 'POST':
            form = RecipeForm(instance=recipe, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(recipe.get_absolute_url())
        else:
            form = RecipeForm(instance=recipe)
        return render_to_response('recipes/form.html',
            {'form': form, 'add': False, 'object': recipe},
            context_instance=RequestContext(request))

Templates anlegen und erweitern
===============================

recipes/templates/recipes/form.html:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}
    {{ block.super }} - Rezept {% if add %}erstellen{% else %}"{{ object.title }}" bearbeiten{% endif %}
    {% endblock %}

    {% block content %}
    {% if add %}
    <h2>Rezept erstellen</h2>
    {% url recipes_recipe_add as action_url %}
    {% else %}
    <h2>Rezept "{{ object.title }}" bearbeiten</h2>
    {% url recipes_recipe_edit as action_url %}
    {% endif %}
    <form action="{{ action_url }}" method="post" accept-charset="utf-8">
        {{ form.as_p }}
        {% csrf_token %}
        <p><input type="submit" value="Speichern"/></p>
    </form>
    <a href="{% url recipes_recipe_index %}">zurück zur Übersicht</a>
    {% endblock %}

recipes/templates/recipes/detail.html:

..  code-block:: html+django

    <a href="{% url recipes_recipe_edit object.pk %}">Rezept bearbeiten</a>

recipes/templates/recipes/index.html:

..  code-block:: html+django

    <a href="{% url recipes_recipe_add %}">Ein Rezept hinzufügen</a>

Test: http://127.0.0.1:8000/

Weiterführende Links zur Django Dokumentation
=============================================

TBD
