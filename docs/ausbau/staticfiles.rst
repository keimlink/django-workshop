.. _staticfiles:

Einbindung von statischen Dateien
*********************************

Eine Website kommt natürlich nicht ohne statische Dateien aus. Statische
Dateien sind alle Dateien, die nicht vom Python Interpreter verarbeitet werden
müssen - also CSS, JavaScript, Bilder usw.

Bis jetzt besteht unser Projekt ja nur aus drei Templates und einigen Python
Dateien. Also machen wir uns daran, dass zu ändern. Dabei kann uns das `HTML5
Boilerplate`_ helfen.

.. _html5_boilerplate:

HTML5 Boilerplate einsetzen
===========================

.. note::

    Damit der Download des HTML5 Boilerplate ZIP Archivs funktioniert
    muss dein Browser die von der Website gesetzten Cookies akzeptieren.

#. Klicke auf der `HTML5 Boilerplate Website <http://html5boilerplate.com/>`_ auf den Button "Get a custom build"
#. Auf der folgenden Seite klickst du auf "Bootstrap"
#. Im Abschnitt "H5BP Optional" wählst du "404 Page" aus
#. Zum Schluss klickst du auf den Button "Download it!"
#. Entpacke das ZIP Archiv
#. Lege ein Verzeichnis :file:`static` im Projektverzeichnis an
#. Konfiguriere ``STATICFILES_DIRS`` in :file:`settings.py`::

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
#. Kopiere die Verzeichnisse :file:`css`, :file:`img` und :file:`js` in das Verzeichnis :file:`cookbook/static`
#. Kopiere die Datei :file:`index.html` in das Verzeichnis :file:`cookbook/templates`
#. Führe die Datei :file:`index.html` des HTML5 Boilerplates mit dem Template :file:`base.html` zusammen. Dabei musst du das Templatetag ``static`` benutzen, um die CSS und JavaScript Dateien auch laden zu können:

    .. code-block:: html+django

        {% load static %}
        <!DOCTYPE html>
        <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
        <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
        <!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
        <!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
                <title>{% block title %}Kochbuch{% endblock %}</title>
                <meta name="description" content="">
                <meta name="viewport" content="width=device-width">

                <link rel="stylesheet" href="{% static "css/bootstrap.min.css" %}">
                <style>
                    body {
                        padding-top: 60px;
                        padding-bottom: 40px;
                    }
                </style>
                <link rel="stylesheet" href="{% static "css/bootstrap-responsive.min.css" %}">
                <link rel="stylesheet" href="{% static "css/main.css" %}">

                <script src="{% static "js/vendor/modernizr-2.6.1-respond-1.1.0.min.js" %}"></script>
            </head>
            <body>
                <!--[if lt IE 7]>
                    <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
                <![endif]-->

                <!-- This code is taken from http://twitter.github.com/bootstrap/examples/hero.html -->

                <div class="navbar navbar-inverse navbar-fixed-top">

                <!-- Hier befindet sich die Navigation -->

                </div>

                <div class="container">

                    <!-- Main hero unit for a primary marketing message or call to action -->
                    <div class="hero-unit">
                        <h1>Kochbuch</h1>
                    </div>

                    <!-- Example row of columns -->
                    <div class="row">
                      {% block content %}{% endblock %}
                    </div>

                    <hr>

                    <footer>
                        <p>&copy; Company 2012</p>
                    </footer>

                </div> <!-- /container -->

                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
                <script>window.jQuery || document.write('<script src="{% static "js/vendor/jquery-1.8.2.min.js" %}"><\/script>')</script>

                <script src="{% static "js/vendor/bootstrap.min.js" %}"></script>

                <script src="{% static "js/main.js" %}"></script>

                <script>
                    var _gaq=[['_setAccount','UA-XXXXX-X'],['_trackPageview']];
                    (function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
                    g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';
                    s.parentNode.insertBefore(g,s)}(document,'script'));
                </script>
            </body>
        </html>

#. Den ``RequestContext`` im View übergeben.

    Dafür müssen beide Views erweitert werden. Jeder View muss einen
    ``RequestContext`` an die ``render_to_response`` Funktion übergeben. Zuerst
    muss der entsprechende Import in :file:`recipes/views.py` hinzugefügt
    werden::

        from django.template import RequestContext

    Dann bekommt jeder Aufruf von ``render_to_response`` das neue Keyword
    Argument ``context_instance=RequestContext(request)``.

    Am Schluss sieht die Datei :file:`recipes/views.py` so aus::

        from django.shortcuts import get_object_or_404, render_to_response
        from django.template import RequestContext

        from .models import Recipe


        def index(request):
            recipes = Recipe.objects.all()
            return render_to_response('recipes/index.html', {'object_list': recipes},
                context_instance=RequestContext(request))


        def detail(request, slug):
            recipe = get_object_or_404(Recipe, slug=slug)
            return render_to_response('recipes/detail.html', {'object': recipe},
                context_instance=RequestContext(request))

Jetzt werden die CSS und JavaScript Dateien geladen.

Statischen Dateien in Apps
==========================

Es ist auch möglich statische Dateien in Apps abzulegen. Dazu einfach ein
Verzeichnis :file:`static` im App-Verzeichnis erstellen. Dieses kann dann genau
wie das :file:`static`-Verzeichnis im Projektverzeichnis genutzt werden.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Die staticfiles App <ref/contrib/staticfiles/>`
* :djangodocs:`RequestContext Dokumentation <ref/templates/api/#django.template.RequestContext>`

.. _HTML5 Boilerplate: http://de.html5boilerplate.com/
