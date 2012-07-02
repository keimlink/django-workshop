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

#. Lade das **Boilerplate "Stripped"** herunter und entpacke es.
#. Lege ein Verzeichnis :file:`static` im Projektverzeichnis an.
#. Konfiguriere ``STATICFILES_DIRS`` in :file:`settings.py`::

    STATICFILES_DIRS = (
        os.path.join(SITE_ROOT, '..', 'static'),
    )
#. Kopiere die Verzeichnisse :file:`css` und :file:`js` aus dem HTML5 Boilerplate Verzeichnis in das :file:`static` Verzeichnis.
#. Führe die Datei :file:`index.html` des HTML5 Boilerplates mit dem Template :file:`base.html` zusammen. Dabei musst du ``STATIC_URL`` benutzen, um die CSS und JavaScript Dateien auch laden zu können::

    <!doctype html>
    <!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
    <!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
    <!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
    <!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
    <head>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
      <title>{% block title %}Kochbuch{% endblock %}</title>
      <meta name="description" content="">
      <meta name="viewport" content="width=device-width">
      <link rel="stylesheet" href="{{ STATIC_URL }}css/style.css">
      <script src="{{ STATIC_URL }}js/libs/modernizr-2.5.3.min.js"></script>
    </head>
    <body>
      <!--[if lt IE 7]><p class=chromeframe>Your browser is <em>ancient!</em> <a href="http://browsehappy.com/">Upgrade to a different browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">install Google Chrome Frame</a> to experience this site.</p><![endif]-->
      <header>
        <h1>Kochbuch</h1>
      </header>
      <div role="main">
        {% block content %}{% endblock %}
      </div>
      <footer>

      </footer>
      <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
      <script>window.jQuery || document.write('<script src="{{ STATIC_URL }}js/libs/jquery-1.7.1.min.js"><\/script>')</script>
      <script src="{{ STATIC_URL }}js/plugins.js"></script>
      <script src="{{ STATIC_URL }}js/script.js"></script>
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
    muss der entsprechende Import in :file:``recipes/views.py`` hinzugefügt
    werden::

        from django.template import RequestContext

    Dann bekommt jeder Aufruf von ``render_to_response`` das neue Keyword
    Argument ``context_instance=RequestContext(request)``.

    Am Schluss sieht die Datei :file:`recipes/views.py` so aus::

        from django.shortcuts import get_object_or_404, render_to_response
        from django.template import RequestContext

        from recipes.models import Recipe


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
