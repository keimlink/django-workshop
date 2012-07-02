Generische Views
****************

Viele Views rendern nur ein Queryset mit einem Template. Die "Handarbeit" in
den View-Funktionen zum Erstellen von Queryset und Context ist also eigentlich
überflüssig. Generische Views sollen diese Arbeit übernehmen und so das
Erstellen von Views noch einfacher machen. Besonders eignen sich generische
Views für immer wiederkehrende Darstellungsformen, wie z.B. Listenansichten.

Seit Django 1.3 gibt es "class-based generic views". Diese sind noch flexibler
als die vorher schon vorhandenen generischen Views, die aber noch auf
Funktionen basierten.

Erstellen der generischen Views
===============================

Ersetzen wir also die beiden Funktionen ``index`` und ``detail`` durch "class-
based generic views" in der Datei :file:`recipes/views.py`. Zuerst müssen zwei
weiterere Imports hinzugefügt werden:

..  code-block:: python

    from django.shortcuts import render
    from django.views.generic import DetailView, ListView

Nun werden die beiden Funktionen durch die Klassen ersetzt:

..  code-block:: python

    class RecipeListView(ListView):
        template_name = 'recipes/index.html'

        def get_queryset(self):
            recipes = Recipe.objects.all()
            logger.debug('Anzahl der Rezepte: %d' % recipes.count())
            return recipes


    class RecipeDetailView(DetailView):
        model = Recipe
        template_name = 'recipes/detail.html'

Die generischen Views in der URLConf
====================================

Damit diese auch benutzt werden muss auch die URLConf :file:`recipes/urls.py`
angepasst werden. Die beiden alten URLs werden entfernt und durch neue
am Ende der Datei ersetzt.

..  code-block:: python

    from django.conf.urls import patterns, include, url

    from .views import RecipeDetailView, RecipeListView

    urlpatterns = patterns('recipes.views',
        url(r'^erstellen/$', 'add', name='recipes_recipe_add'),
        url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', name='recipes_recipe_edit'),
    )

    urlpatterns += patterns('',
        url(r'^rezept/(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(),
            name='recipes_recipe_detail'),
        url(r'^$', RecipeListView.as_view(), name='recipes_recipe_index'),
    )

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Allgemeines zu class-based generic views <topics/class-based-views/>`
* :djangodocs:`Class-based generic views Referenz <ref/class-based-views/>`
