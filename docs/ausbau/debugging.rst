Django Debugging
****************

Neben dem Debugging des Frontends mit dem :ref:`debug_toolbar` kann man auch
ganz "klassisch" den Quellcode von Django Applikationen debuggen.

Die Fehlerseite gezielt aufrufen
================================

Da die Fehlerseite eine Menge Informationen aufbereitet ist es manchmal
sinnvoll diese gezielt aufzurufen. Dazu kann man das Statement
``assert`` verwenden.

Provozieren eines ``AssertionError`` im View ``index``::

    def index(request):
        recipes = Recipe.objects.all()
        assert False
        return render_to_response('recipes/index.html', {'object_list': recipes})

Man kann den optionalen zweiten Parameter von ``assert`` zur Ausgabe
von zusätzlichen Informationen nutzen::

    def index(request):
        recipes = Recipe.objects.all()
        assert False, 'Anzahl der Rezepte: %d' % recipes.count()
        return render_to_response('recipes/index.html', {'object_list': recipes})

In ein Logfile schreiben
========================

Es ist zwar möglich mit ``print`` in die Konsole des Entwicklungs-Webservers
zu schreiben. Das wird aber schell unübersichtlich und kann beim Deployment zu
Problemen führen.

Besser ist die Nutzung des seit Version 1.3 in Django integrierten
Logging-Frameworks.

In der Datei :file:`settings.py` ist schon einen rudimentäre Konfiguration des
Logging-Frameworks vorhanden. Dieser fügen wir ein Dictionary ``formatters``
und einen neuen ``handler`` mit dem Namen ``debuglog``, der den neuen
``formatter`` benutzt, hinzu. Die gesamte Logging Konfiguration sieht dann so
aus::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(asctime)s %(pathname)s %(message)s'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'debuglog': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/tmp/debug.log',
                'maxBytes': 1000,
                'formatter': 'simple'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

Jetzt muss noch am Ende der Datei der folgende Code einfügt werden, um den
``logger`` zu registrieren. Allerdings soll dieser nur ausgeführt werden wenn
``DEBUG`` den Wert ``True`` hat::

    if DEBUG:
        LOGGING['loggers'].update(
            {'cookbook': {
                'handlers': ['debuglog'],
                'level': 'DEBUG'
            }}
        )

Nun kann man im View in das Log schreiben::

    import logging
    
    logger = logging.getLogger('cookbook.recipes.views')
    
    def index(request):
        recipes = Recipe.objects.all()
        logger.debug('Anzahl der Rezepte: %d' % recipes.count())
        return render_to_response('recipes/index.html', {'object_list': recipes})

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

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Das Logging-Framework <topics/logging/>`
