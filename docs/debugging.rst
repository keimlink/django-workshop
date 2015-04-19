****************
Django Debugging
****************

In addition to the debugging of the front end with the :ref:`debug_toolbar` you
can also do "classic" debugging of the source code of Django applications.

Call up the error page specifically
===================================

Since the error page prepares a lot of information, it is sometimes useful to
call it specifically. This can be done by using the ``assert`` statement.

Provoke an ``AssertionError`` in the ``index`` view:

::

    def index(request):
        recipes = Recipe.objects.all()
        assert False
        return render_to_response('recipes/index.html', {'object_list': recipes},
            context_instance=RequestContext(request))

You can use the optional second parameter of ``assert`` to issue additional
information:

::

    def index(request):
        recipes = Recipe.objects.all()
        assert False, 'Recipe count: %d' % recipes.count()
        return render_to_response('recipes/index.html', {'object_list': recipes},
            context_instance=RequestContext(request))

..  _logging_framework:

Write to a log file
===================

While it is possible to use ``print()`` in the terminal of the development web
server for debugging this soon gets confusing. Especially because there is no
way to format and control the output of the ``print()`` calls. For this reason
it's better to use the logging framework which is included in Django since
version 1.3.

The default configuration of the logging framework sends an email to the site
admins on every HTTP 500 error. We can extend this configuration for our own
purposes.

Therefore we add a constant ``LOGGING`` to the file :file:`settings.py`. It's
value is a dict with four keys:

:``version``:

    A integer representing the schema version.

:``disable_existing_loggers``:

    If specified as ``False``, loggers which exist are left enabled.

:``formatters``:

    A dict in which each key is a formatter id and each value is a dict
    describing how to configure the corresponding `Formatter
    <https://docs.python.org/2/library/logging.html#logging.Formatter>`_
    instance.

:``handlers``:

    A dict in which each key is a handler id and each value is a dict
    describing how to configure the corresponding `Handler
    <https://docs.python.org/2/library/logging.html#handler-objects>`_
    instance.

The new formatter called ``simple`` controls which values are written into the
log. The new handler called ``debuglog`` writes to a file that is automatically
rotated when it reaches a certain size:

::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(asctime)s %(pathname)s %(message)s'
            },
        },
        'handlers': {
            'debuglog': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'debug.log'),
                'maxBytes': 50000,
                'backupCount': 1,
                'formatter': 'simple'
            },
        },
    }

Now you have to add the following code at the end of the file (after importing
``local_settings``) to register the new ``logger``. Though this should be
performed only if ``DEBUG`` is ``True``:

::

    if DEBUG:
        LOGGING['loggers'] = {
            'recipes': {
                'handlers': ['debuglog'],
                'level': 'DEBUG'
            }
        }

Now you can write to the log in the view:

::

    import logging

    logger = logging.getLogger(__name__)

    def index(request):
        recipes = Recipe.objects.all()
        logger.debug('Recipe count: %d' % recipes.count())
        return render_to_response('recipes/index.html', {'object_list': recipes})

You can also see the entries in the log file in the "Logging" section of the
Django debug toolbar. This saves you from having to open the log file to look
at the entries.

..  _python_debugger:

Using the Python debugger
=========================

Python provides a simple, but very powerful interactive debugger: `pdb
<http://docs.python.org/library/pdb.html>`_.

The debugger is activated most easily by calling ``import pdb; pdb.set_trace()``:

::

    def detail(request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        import pdb; pdb.set_trace()
        return render_to_response('recipes/detail.html', {'object': recipe},
            context_instance=RequestContext(request))

After the start of the ``detail`` view of the debugger starts in the terminal:

::

    > /vagrant/src/cookbook/recipes/views.py(16)detail()
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
    > /vagrant/src/cookbook/recipes/views.py(13)detail()
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
    > /vagrant/src/cookbook/recipes/views.py(16)detail()
    -> return render_to_response('recipes/detail.html', {'object': recipe},
    (Pdb) recipe.id
    1
    (Pdb) c

Here is the key ``slug`` removed from ``kwargs`` and gets replaced by the key
``id == 1``. Thus no longer the desired entry with the ``id == 2`` is loaded
from the database, but the record with ``id == 1``.

You can find a list of all debugger commands in the `pdb documentation
<http://docs.python.org/library/pdb.html#debugger-commands>`_.

If want to use a more powerful debugger you can replace pdb with `pdb++
<https://bitbucket.org/antocuni/pdb/src>`_, a drop-in replacement for pdb.

Further links to the Django and Python documentation
====================================================

* :djangodocs:`Django's logging framework <topics/logging/>`
* `logging - Logging facility for Python <http://docs.python.org/library/logging.html>`_
* `logging.config - Logging configuration <http://docs.python.org/library/logging.config.html>`_
* `logging.handlers - Logging handlers <http://docs.python.org/library/logging.handlers.html>`_
