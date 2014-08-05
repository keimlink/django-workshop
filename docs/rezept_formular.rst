Rezepte mit einem Formular hinzufügen
*************************************

.. todo:: Translate chapter

Nun wollen wir das Erstellen von Rezepten im Frontend für
authentifizierte Benutzer ermöglichen.

URLConf erweitern
=================

Dazu legst du zuerst die entsprechenden URLs zum Erstellen und
Bearbeiten der Rezepte an in :file:`recipes/urls.py` an::

    url(r'^erstellen/$', 'add', name='recipes_recipe_add'),
    url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),

Die vollständige URLConf sieht dann so aus::

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('recipes.views',
        url(r'^rezept/(?P<slug>[-\w]+)/$', 'detail', name='recipes_recipe_detail'),
        url(r'^erstellen/$', 'add', name='recipes_recipe_add'),
        url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),
        url(r'^$', 'index', name='recipes_recipe_index'),
    )

Ein Formular erstellen
======================

Als nächstes legst du das Formular an. Erstelle dazu die Datei
:file:`recipes/forms.py`::

    from django.forms import ModelForm

    from .models import Recipe


    class RecipeForm(ModelForm):
        class Meta:
            model = Recipe
            exclude = ('slug', 'author', 'date_created', 'date_updated')

Mit Hilfe von ``ModelForm`` kannst du direkt aus dem Model ``Recipe``
ein Formular bauen und musst nur noch angeben welche Felder nicht im
Formular auftauchen sollen.

Zwei Views für das Formular
===========================

Jetzt wollen wir die Views zum Erstellen und Bearbeiten der Rezepte in
:file:`recipes/views.py` erstellen.

Dazu sind zuerst einige weitere Imports nötig::

    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied
    from django.shortcuts import redirect, render
    from django.template.defaultfilters import slugify

    from .forms import RecipeForm

Zuerst legst du den View zum Erstellen eines neuen Rezeptes an::

    @login_required
    def add(request):
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
        return render(request, 'recipes/form.html',
            {'form': form, 'add': True})

Statt dem :ref:`schon bekannten <request_context_vorstellung>` Shortcut
``render_to_response`` benutzen wir hier den mit Django 1.3 neu
eingeführten Shortcut ``render``, um den ``RequestContext`` zu erzeugen.
Dieser erstellt aus dem ersten Argument ``request`` automatisch einen
``RequestContext``. Mit ``render_to_response`` hätte der Code so
ausgehen::

    return render_to_response('recipes/form.html',
        {'form': form, 'add': True}, context_instance=RequestContext(request))

Wenn POST-Daten vorhanden sind werden diese an die Instanz von
``RecipeForm`` gebunden. Danach wird überprüft, ob die Daten valide
sind. Beim Speichern des Formulars wird das Rezept selbst nicht
gespeichert (durch setzen von ``commit=False``), damit noch Autor und
Slug definiert werden können. Dann wird zuerst das Rezept und danach die
Many-To-Many- Relations gespeichert. Am Schluss wird zur Seite des neuen
Rezeptes weitergeleitet.

Sind keine POST-Daten vorhanden wird nur eine Instanz der Formulars erstellt.

Mit dem Parameter ``add`` unterscheiden wir später im Template, ob wir
gerade ein Rezept erstellen oder hinzufügen. Denn wir benutzen nur ein
Template für beide Aktionen.

Durch den Decorator ``login_required`` kann dieser View nur von
angemeldeten Benutzern aufgerufen werden.

Der zweite View dient zum Bearbeiten der Rezepte::

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
        return render(request, 'recipes/form.html',
            {'form': form, 'add': False, 'object': recipe})

Aus dem URL bekommen wir die Id des Rezeptes. Diese wird dazu benutzt
eine Instanz zu holen oder eine 404 Seite anzuzeigen, falls dies nicht
möglich ist.

Falls der angemeldete Benutzer nicht der Autor ist oder nicht zu den
Redakteuren der Website gehört wird ein 403 Fehler angezeigt, da die
Benutzer nur ihre eigenen Rezepte bearbeiten sollen.

Die restliche Verarbeitung der POST-Daten unterscheidet sich nur in drei
Punkten vom View ``add``:

#. Die Instanz von RecipeForm wird mit ``instance=recipe`` erstellt.
#. Der Parameter ``add`` im Kontext ist ``False``.
#. Zusätzlich wird die Instanz des Rezeptes als ``object`` in den Kontext gegeben.

Templates anlegen und erweitern
===============================

Nun geht es daran das Template anzulegen. In den beiden Views wurde
:file:`recipes/templates/recipes/form.html` genutzt. So sieht das Template
aus:

..  code-block:: html+django

    {% extends "base.html" %}

    {% load crispy_forms_tags %}

    {% block title %}
        {{ block.super }} - Rezept {% if add %}erstellen
            {% else %}"{{ object.title }}" bearbeiten{% endif %}
    {% endblock %}

    {% block content %}
        {% if add %}
            <h2>Rezept erstellen</h2>
            {% url 'recipes_recipe_add' as action_url %}
        {% else %}
            <h2>Rezept "{{ object.title }}" bearbeiten</h2>
            {% url 'recipes_recipe_edit' object.pk as action_url %}
        {% endif %}
        <form action="{{ action_url }}" method="post" accept-charset="utf-8">
            {{ form|crispy }}
            {% csrf_token %}
            <p><input type="submit" value="Speichern"/></p>
        </form>
    {% endblock %}

Im Template kann man jetzt sehen, wie der Parameter ``add`` zur
Unterscheidung zwischen Erstellen und Bearbeiten genutzt wird.

Jetzt kannst du das Template :file:`recipes/templates/recipes/detail.html`
um einen Link zum Bearbeiten des Rezeptes erweitern:

..  code-block:: html+django

    <a href="{% url 'recipes_recipe_edit' object.pk %}">Rezept bearbeiten</a>

Und im Listentemplate :file:`recipes/templates/recipes/index.html` einen
Link zum Hinzufügen eines Rezeptes einsetzen:

..  code-block:: html+django

    <a href="{% url 'recipes_recipe_add' %}">Ein Rezept hinzufügen</a>

Fertig! Nun kannst du als angemeldeter Benutzer im Frontend Rezepte
erstellen und bearbeiten.

Wenn du möchtest, kannst du außerdem  die Datei :file:`403.html` im
Template Verzeichnis des Projekts angelegen. Diese wird dann anstelle
der Meldung "403 Forbidden" angezeigt wenn eine ``PermissionDenied``
Exception ausgelöst wird.

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Zugriff nicht erlaubt{% endblock %}

    {% block content %}
        <h2>Zugriff nicht erlaubt</h2>
        <p>Sie haben nicht ausreichende Rechte, um auf diese Seite zuzugereifen.</p>
    {% endblock %}

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Forms API <ref/forms/api/>`
* :djangodocs:`Formulare für Models erstellen <topics/forms/modelforms/>`
* :djangodocs:`Der render Shortcut <topics/http/shortcuts/#render>`
* :djangodocs:`Der 403 (HTTP Forbidden) View <topics/http/views/#the-403-http-forbidden-view>`
