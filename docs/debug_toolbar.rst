..  _debug_toolbar:

********************
Django Debug Toolbar
********************

The `Django Debug Toolbar
<https://github.com/django-debug-toolbar/django-debug-toolbar>`_
can be a great help during the development of a project with Django. The
following panels can be displayed in the browser:

- Versions of Python, Django, and installed apps
- Request timer
- A list of settings in settings.py
- HTTP request and response headers
- GET/POST/cookie/session variables
- SQL queries including execution time
- Templates and context used
- Used static files and their locations
- Cache queries
- List of signals
- Logging output via Python’s built-in logging module

Django Debug Toolbar also contains a panel to intercept redirects. An
additional panel to profile the view function can be enabled.

Moreover, the command :command:`debugsqlshell` is added to
:file:`manage.py` to output the SQL queries while working with the
:ref:`database API <database-api>` in the Python interpreter.

Installation
============

Use :command:`pip` to install Django Debug Toolbar:

::

    $ pip install django-debug-toolbar

Make sure that ``django.contrib.staticfiles`` is :djangodocs:`set up
properly <howto/static-files/>` and add ``debug_toolbar`` to your
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        'django.contrib.staticfiles',
        # ...
        'debug_toolbar',
    )

    STATIC_URL = '/static/'

After that the Debug Toolbar is displayed at the right side of your
browser window.

Third-party Panels
==================

There are also several additional third-party panels available:

- `Django Debug Logging <https://github.com/lincolnloop/django-debug-logging>`_ - Log the debug toolbar statistics to the database during a site crawl
- `Django Debug Panel <https://github.com/recamshak/django-debug-panel>`_ - Django Debug Toolbar inside WebKit DevTools, works fine with background AJAX requests and non-HTML responses
- `django-debug-toolbar-autoreload <https://github.com/gregmuellegger/django-debug-toolbar-autoreload>`_ - Automatically reload the page if a template is changed
- `Haystack <https://github.com/streeter/django-haystack-panel>`_ - See queries made by your Haystack backends
- `HTML Tidy/Validator <https://github.com/joymax/django-dtpanel-htmltidy>`_ - HTML Tidy or HTML Validator is a custom panel
- `Inspector <https://github.com/santiagobasulto/debug-inspector-panel>`_ - Retrieve and display information you specify using the debug statement
- `Line Profiler <https://github.com/dmclain/django-debug-toolbar-line-profiler>`_ - Do line-by-line profiling
- `Memcache <https://github.com/ross/memcache-debug-panel>`_ - Track memcached usage
- `MongoDB <https://github.com/hmarr/django-debug-toolbar-mongo>`_ - Display MongoDB debugging information
- `Neo4j <https://github.com/robinedwards/django-debug-toolbar-neo4j-panel>`_ - Trace neo4j rest API calls
- `Sites <https://github.com/elvard/django-sites-toolbar>`_ - Browse Sites and switch between them
- `Template Timings <https://github.com/orf/django-debug-toolbar-template-timings>`_ - Display template rendering times
- `User <https://github.com/playfire/django-debug-toolbar-user-panel>`_ - Easily switch between logged in users and see properties of current user
