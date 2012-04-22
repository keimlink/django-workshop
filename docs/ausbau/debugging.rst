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
        return render_to_response('recipes/index.html', {'object_list': recipes},
            context_instance=RequestContext(request))

Man kann den optionalen zweiten Parameter von ``assert`` zur Ausgabe
von zusätzlichen Informationen nutzen::

    def index(request):
        recipes = Recipe.objects.all()
        assert False, 'Anzahl der Rezepte: %d' % recipes.count()
        return render_to_response('recipes/index.html', {'object_list': recipes},
            context_instance=RequestContext(request))

..  _logging_framework:

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
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(asctime)s %(pathname)s %(message)s'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
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

Jetzt muss noch am Ende der Datei (nach dem Importieren von ``local_settings``)
der folgende Code einfügt werden, um den ``logger`` zu registrieren. Allerdings
soll dieser nur ausgeführt werden wenn ``DEBUG`` den Wert ``True`` hat::

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

Die Einträge in der Logdatei kann man auch im Bereich "Logging" des Django
Debug Toolbar sehen. So spart man sich das Öffnen der Datei, um die Einträge
anzusehen.

..  _python_debugger:

Mit dem Python-Debugger arbeiten
================================

Python enthält einen einfachen, aber sehr mächtigen interaktiven Debugger:
`pdb <http://docs.python.org/library/pdb.html>`_.

Den Debugger aktiviert man am einfachsten durch den Aufruf von ``import pdb;
pdb.set_trace()``::

    def detail(request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        import pdb; pdb.set_trace()
        return render_to_response('recipes/detail.html', {'object': recipe})

Nach dem Aufruf eines beliebigen ``detail``-Views startet der Debugger in der
Konsole:

..  code-block:: bash

    > /vagrant/src/ausbau/cookbook/recipes/views.py(16)detail()
    -> return render_to_response('recipes/detail.html', {'object': recipe},
    (Pdb) l
     11
     12
     13     def detail(request, slug):
     14         recipe = get_object_or_404(Recipe, slug=slug)
     15         import pdb; pdb.set_trace()
     16  ->     return render_to_response('recipes/detail.html', {'object': recipe},
     17             context_instance=RequestContext(request))
    [EOF]
    (Pdb) slug
    u'kohleintopf-mit-tortellini'
    (Pdb) recipe.id
    2
    (Pdb) j 13
    > /vagrant/src/ausbau/cookbook/recipes/views.py(13)detail()
    -> def detail(request, slug):
    (Pdb) s
    --Call--
    > /home/vagrant/.virtualenvs/django-workshop/lib/python2.6/site-packages/django/shortcuts/__init__.py(100)get_object_or_404()
    -> def get_object_or_404(klass, *args, **kwargs):
    (Pdb) args
    klass = <class 'recipes.models.Recipe'>
    args = ()
    kwargs = {'slug': u'kohleintopf-mit-tortellini'}
    (Pdb) del(kwargs['slug'])
    (Pdb) kwargs['id'] = 1
    (Pdb) args
    klass = <class 'recipes.models.Recipe'>
    args = ()
    kwargs = {'id': 1}
    (Pdb) c
    > /vagrant/src/ausbau/cookbook/recipes/views.py(16)detail()
    -> return render_to_response('recipes/detail.html', {'object': recipe},
    (Pdb) recipe.id
    1
    (Pdb) c

Hier wird der Schlüssel ``slug`` aus ``kwargs`` entfernt und mit dem Schlüssel
``id==1`` ersetzt. Dadurch wird nicht mehr der gewünscht Eintrag mit der
``id==2`` aus der Datenbank geladen, sondern der Datensatz mit ``id==1``.

Eine Liste aller Befehle des Debuggers `findest du in der Dokumentation
<http://docs.python.org/library/pdb.html#debugger-commands>`_.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Das Logging-Framework <topics/logging/>`
