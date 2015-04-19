**************
Error Handling
**************

HTTP status code 404 (Not Found)
================================

Each time an URL is accessed, which can't be processed by the URLconf or when a
view raises an ``Http404`` exception, the view defined in ``handler404`` is
called.

This happens only if ``DEBUG`` is set to ``False``. If ``DEBUG`` has the value
``True`` the view defined in ``handler404`` will not be called, but a notice
page appears with more information.

The ``handler404`` is by default ``django.views.defaults.page_not_found``. This
view expects that in the root of your template directory a template called
:file:`404.html` exists to render it.

The view passes the variable ``request_path`` to the template, which contains
the URL that generated the 404 error. In addition, the context can be used to
access variables such as ``MEDIA_URL``.

If this file does not exist, as a ``Http500`` exception is thrown.

HTTP status code 500 (Internal Server Error)
============================================

A ``Http500`` exception is triggered when you run code that errors. If
``DEBUG`` is set to ``True``, the traceback and other debugging information are
shown.

But if ``DEBUG`` is set to ``False`` the view defined in ``handler500`` is
invoked, which is ``django.views.defaults.server_error`` by default. This
renders the template :file:`500.html` that is expected in the root of the
template directory.

The template :file:`500.html` has an empty context and there are no variables
set.

Create templates for error handling
===================================

You can test these templates by setting ``DEBUG`` to ``False`` in
:file:`local_settings.py` and call an URL that does not exist.

Without the two templates you see the message "A server error occurred. Please
contact the administrator.". Exception and stack trace you see on the terminal.

If you create the file :file:`500.html` in the template directory inside the
project directory, this template is rendered and the stack trace disappears on
the terminal.

The `HTML5 Boilerplate <http://de.html5boilerplate.com/>`_ that you've used in
the chapter :ref:`staticfiles` also contains a ready-to-use 404 page. To use
this page you copy the file :file:`404.html` from the HTML5 Boilerplate
directory in the template directory in the project directory. If you are now
call a not existing URL, you see this page instead.

Further links to the Django documentation
=========================================

* :djangodocs:`Customizing error views <topics/http/views/#customizing-error-views>`
