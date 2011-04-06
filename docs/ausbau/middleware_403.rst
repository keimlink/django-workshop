Middleware für 403 Fehler
*************************

Im vorhergehenden Kapitel haben wir einen 403 Fehler erzeugt wenn ein Benutzer
ein Rezept bearbeiten wollte, dessen Autor er nicht war. Allerdings ist das
Ergebnis eine weiße Seite, was nicht besonders schön ist.

Dieses Problem ist eine gute Gelegenheit eine einfache Middleware zu
schreiben. Lege dazu im Projektverzeichnis die Datei :file:`middleware.py` an
und erstelle darin die folgende Klasse:

..  code-block:: python

    from django.template import loader, RequestContext

    class Http403Middleware(object):
        def process_response(self, request, response):
            if response.status_code == 403 and response.tell() == 0:
                t = loader.get_template('403.html')
                c = RequestContext(request, {'request_path': request.path})
                response.write(t.render(c))
            return response

Es wird der ``process_response``-Hook benutzt, um bei einem 403 Status Code
das Template :file:`403.html` zu rendern. Da es dieses Template noch nicht
gibt muss es jetzt angelegt werden:

..  code-block:: html

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
        "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>Zugriff nicht erlaubt</title>
    </head>
    <body>
        <h2>Zugriff nicht erlaubt</h2>
        <p>Der Zugriff auf die Seite <strong>{{ request_path }}</strong> ist ihnen nicht erlaubt.</p>
    </body>
    </html>

Damit die Middleware auch benutzt wird muss sie in die Liste der Middlewares
in der ``settings.py`` eingefügt werden:

..  code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'middleware.Http403Middleware'
    )

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Middleware benutzen und selbst schreiben <topics/http/middleware/#topics-http-middleware>`
