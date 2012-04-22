Ausbau der Views
****************

Die Views sind zwar schon relativ kompakt, enthalten aber immer noch einigen
Code, der sich wiederholt. Also machen wir uns daran das zu verbessern.

Die Funktion ``render_to_response``
===================================

Als Erstes entfernen wir die beiden folgenden Imports am Anfang der Datei
:file:`recipes/views.py`::

    from django.http import Http404, HttpResponse
    from django.template import Context, loader

Wir ersetzen sie mit dem folgenden Import::

    from django.shortcuts import render_to_response

In ``django.shortcuts`` befinden sich mehrere Funktionen, die die Arbeit mit
den Views erleichtern sollen. Eine davon ist ``render_to_response``.

Sie kümmert sich um die folgenden Dinge:

* Laden des Templates
* Bereitstellen des Contexts
* Template mit dem Context rendern
* Einen HttpResponse zurückgeben, der das Ergebnis der Renderns enthält

Dadurch können wir die erste Funktion im View stark reduzieren. Der Beginn der
Datei :file:`recipes/views.py` sieht dann wie folgt aus::

    from django.shortcuts import render_to_response

    from recipes.models import Recipe

    def index(request):
        recipes = Recipe.objects.all()
        return render_to_response('recipes/index.html', {'object_list': recipes})

Die Funktion ``get_object_or_404``
==================================

Aber auch die zweite View Funktion wollen wir vereinfachen. Dazu nutzen wir
eine weitere Funktion, die ``django.shortcuts`` bereitstellt - sie heißt
``get_object_or_404``::

    from django.shortcuts import get_object_or_404

    def detail(request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        return render_to_response('recipes/detail.html', {'object': recipe})

Die Funktion ``get_object_or_404`` versucht eine Instanz des übergebenen
Models mit der Manager-Methode ``get()`` zu holen. Das zweite Argument
``slug=slug`` wird dabei an ``get()`` übergeben. Wird kein entsprechendes
Model gefunden wird eine ``Http404`` Exception ausgelöst.

Die vollständige Datei
======================

Wir haben also mit Hilfe der beiden Hilfsfunktionen den Code, den wir im View
selbst schreiben müssen, stark reduziert.

..  code-block:: python

    from django.shortcuts import get_object_or_404, render_to_response

    from recipes.models import Recipe

    def index(request):
        recipes = Recipe.objects.all()
        return render_to_response('recipes/index.html', {'object_list': recipes})

    def detail(request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        return render_to_response('recipes/detail.html', {'object': recipe})

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Django shortcut Funktionen <topics/http/shortcuts/#topics-http-shortcuts>`
