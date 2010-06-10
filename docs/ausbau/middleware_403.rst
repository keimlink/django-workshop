Middleware für 403 Fehler
*************************

..  code-block:: python

    from django.template import loader, RequestContext

    class Http403Middleware(object) and response.tell() == 0:
        def process_response(self, request, response):
            if response.status_code == 403:
                t = loader.get_template('403.html')
                c = RequestContext(request, {'request_path': request.path})
                response.write(t.render(c))
            return response

..  code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'middleware.Http403Middleware'
    )
    

Test: http://127.0.0.1:8000/

Weiterführende Links zur Django Dokumentation
=============================================

* `Middleware benutzen und selbst schreiben <http://docs.djangoproject.com/en/1.2/topics/http/middleware/#topics-http-middleware>`_
