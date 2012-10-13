Middleware
**********

Mit einer Middleware kann man an verschiedenen Stellen in die
Verarbeitung des HTTP Requests bzw. das Senden der HTTP Response
eingreifen (siehe :ref:`Grafik: Schematische Darstellung einer Request /
Response Verarbeitung <grafik_request_response>`).

Mit der folgenden Middleware wollen wir bestimmte Browser zurückweisen.
Sie sollen also immer die gleiche Seite angezeigt bekommen, auf der der
Benutzer erklärt bekommt, dass sein Browser zum Besuch der Website nicht
geeignet ist. Lege dazu im Konfigurationsverzeichnis die Datei
:file:`middleware.py` an und erstelle darin die folgende Klasse:

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

Das Template, dass im Falle der Zurückweisung gerendert werden soll,
legst du in :file:`templates/reject.html` an:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Browser nicht unterstützt{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <h2>Browser nicht unterstützt</h2>
    <p>Ihr Browser <em>{{ user_agent }} wird leider nicht unterstützt.</em></p>
    {% endblock %}

Damit die Middleware auch benutzt wird muss sie in die Liste der
Middlewares in der ``settings.py`` eingefügt werden:

..  code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'cookbook.middleware.RejectMiddleware'
    )

Nun kannst du verschiedene Browser ausprobieren. Alle Browser, deren
User Agent auf den regulären Ausdruck passt, bekommen nur die Seite mit
dem Hinweis angezeigt.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Middleware benutzen und selbst schreiben <topics/http/middleware/#topics-http-middleware>`
