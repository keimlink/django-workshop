**********
Middleware
**********

A middleware can intervene at different points in the processing of a HTTP
request or sending the HTTP response (see :ref:`Illustration: Schematic Diagram
of Django's Request/Response Processing <request_response_graph>`).

The following middleware will reject certain browsers. So the users should
always get displayed the same page which explains that the browser is not
suitable to visit the website. Put the file :file:`middleware.py` in the
configuration directory and create in the following class:

..  code-block:: python

    import re

    from django.shortcuts import render


    RE_REJECTED_AGENTS = re.compile(r'(msie 6\.0|yahoo! slurp)', re.IGNORECASE)


    class RejectMiddleware(object):
        """Middleware to reject specific user agents."""
        def process_request(self, request):
            if 'HTTP_USER_AGENT' in request.META:
                user_agent = request.META['HTTP_USER_AGENT']
                if RE_REJECTED_AGENTS.search(user_agent.lower()):
                    ctx = {'user_agent': user_agent}
                    return render(request, 'reject.html', ctx)
            return None

The template that will be rendered in the event of rejection should be put in
:file:`templates/reject.html`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Browser not supported{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <h2>Browser not supported</h2>
    <p>Unfortunately your Browser <em>{{ user_agent }}</em>
        is not suported by this website. :(</p>
    {% endblock %}

In order for the middleware to be used it must be inserted at the end of the
list of middlewares in the file :file:`settings.py`:

..  code-block:: python

    MIDDLEWARE_CLASSES = (
        # ...
        'cookbook.middleware.RejectMiddleware'
    )

Now you can try different browsers. All browsers whose user agent matches the
regular expression only get the page where the notice appears.

Further links to the Django documentation
=========================================

* :djangodocs:`Middleware <topics/http/middleware/>`
