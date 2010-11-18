Django Debugging
****************

Neben dem Debugging des Frontends mit dem :ref:`debug_toolbar` kann man auch
ganz "klassisch" den Quellcode von Django Applikationen debuggen.

Die Fehlerseite gezielt aufrufen
================================

Da die Fehlerseite eine Menge Informationen aufbereitet ist es manchmal
sinnvoll diese gezielt aufzurufen. Dazu kann man das Statement ``assert``
verwenden.

Provozieren eines ``AssertionError`` im View ``index``::

    def index(request):
        recipes = Recipe.objects.all()
        assert False
        return render_to_response('recipes/index.html', {'object_list': recipes})

Man kann den optionalen zweiten Parameter von ``assert`` zur Ausgabe von
zusätzlichen Informationen nutzen::

    def index(request):
        recipes = Recipe.objects.all()
        assert False, 'Anzahl der Rezepte: %d' % recipes.count()
        return render_to_response('recipes/index.html', {'object_list': recipes})

Ein Logfile nutzen
==================

Es ist zwar möglich mit ``print`` in die Konsole des Entwicklungs-Webservers
zu schreiben. Aber das nicht übersichtlich und kann beim Deployment zu
Problemen führen.

Besser ist die Nutzung eines Logfiles. Dazu kannst du das `logging Modul
<http://docs.python.org/library/logging.html>`_ nutzen.

Zum Beispiel kann man den folgenden Code in die ``local_settings.py``
einfügen::

    if DEBUG:
        import logging
        logging.basicConfig(
            level = logging.DEBUG,
            format = '%(asctime)s %(levelname)s %(message)s', 
            filename = '/tmp/debug.log',
            filemode = 'w'
        )

Nun kann man im View in das Log schreiben::

    def index(request):
        recipes = Recipe.objects.all()
        import logging
        logging.debug('Anzahl der Rezepte: %d' % recipes.count())
        return render_to_response('recipes/index.html', {'object_list': recipes})

Die Ausgabe wird in die Datei ``debug.log`` im Verzeichnis ``/tmp``
geschrieben.

Da der Code in ``local_settings.py`` nur ausgeführt wird wenn ``DEBUG`` den
Wert ``True`` hat, findet kein Logging statt wenn ``DEBUG = False`` benutzt
wird.

Mit dem Python-Debugger arbeiten
================================

Python enthält einen einfachen, aber sehr mächtigen interaktiven Debugger:
`pdb <http://docs.python.org/library/pdb.html>`_.

Den Debugger aktiviert man am einfachsten durch den Aufruf von ``import pdb;
pdb.set_trace()``::

    def detail(render, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        import pdb; pdb.set_trace()
        return render_to_response('recipes/detail.html', {'object': recipe})

Nach dem Aufruf eines beliebigen ``detail``-Views startet der Debugger in der
Konsole:

..  code-block:: bash

    > /Users/zappi/Projekte/Python/django-workshop/src/cookbook/recipes/views.py(12)detail()
    -> return render_to_response('recipes/detail.html', {'object': recipe})
    (Pdb) l
      7         return render_to_response('recipes/index.html', {'object_list': recipes})
      8  
      9     def detail(render, slug):
     10         recipe = get_object_or_404(Recipe, slug=slug)
     11         import pdb; pdb.set_trace()
     12  ->     return render_to_response('recipes/detail.html', {'object': recipe})
    [EOF]
    (Pdb) recipe.id
    3
    (Pdb) j 9
    > /Users/zappi/Projekte/Python/django-workshop/src/cookbook/recipes/views.py(9)detail()
    -> def detail(render, slug):
    (Pdb) s
    --Call--
    > /Users/zappi/.virtualenvs/django-workshop/lib/python2.6/site-packages/django/shortcuts/__init__.py(75)get_object_or_404()
    -> def get_object_or_404(klass, *args, **kwargs):
    (Pdb) locals()
    {'args': (), 'klass': <class 'recipes.models.Recipe'>, 'kwargs': {'slug': u'omas-beste-frikadellen'}}
    (Pdb) del(kwargs['slug'])
    (Pdb) kwargs['id']=1
    (Pdb) locals()
    {'args': (), 'klass': <class 'recipes.models.Recipe'>, 'kwargs': {'id': 1}}
    (Pdb) c
    > /Users/zappi/Projekte/Python/django-workshop/src/cookbook/recipes/views.py(12)detail()
    -> return render_to_response('recipes/detail.html', {'object': recipe})
    (Pdb) recipe.id
    1
    (Pdb) c

Hier wird der Schlüssel ``slug`` aus ``kwargs`` entfernt und mit dem Schlüssel
``id==1`` ersetzt. Dadurch wird nicht mehr der gewünscht Eintrag mit der
``id==3`` aus der Datenbank geholt sondern der Datensatz mit ``id==1``.

Eine Liste aller Befehle des Debuggers `findest du in der Dokumentation
<http://docs.python.org/library/pdb.html#debugger-commands>`_.
