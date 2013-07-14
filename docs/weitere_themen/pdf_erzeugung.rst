PDF-Erzeugung
*************

Für die Erzeugung von PDF-Dokumenten gibt es verschiedene Möglichkeiten. Wir
wollen die Bibliothek pisa_ nutzen, die ein html2pdf Konverter ist.

.. _pisa: http://pypi.python.org/pypi/pisa

Installation der nötigen Pakete
===============================

Linux und OS X
--------------

Zur Vorbereitung der Installation von PIL_ müssen unter Linux die
folgenden Pakete installiert sein:

* libjpeg62
* liblcms1
* python-dev

Für OS X muss man zum Beispiel mit Homebrew_ die Unterstützung für das
JPG Format installieren::

    $ brew install jpeg

Dann können alle nötigen Pakete installiert werden::

    $ pip install pisa PIL html5lib httplib2 pyPdf reportlab

.. _PIL: http://www.pythonware.com/products/pil/
.. _Homebrew: http://mxcl.github.com/homebrew/

Windows
-------

Für Windows müssen PIL_ und ReportLab_ als Binärpaket mit Hilfe von
``easy_install`` installiert werden. Der Downloadlink für PIL findet
sich auf der `PIL Homepage`_. Den Downloadlink für ReportLab findest du
auf dem `ReportLab FTP Server`_.

So werden die beiden Pakete installiert::

    > easy_install http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
    > easy_install http://www.reportlab.com/ftp/reportlab-2.5.win32-py2.7.exe

.. note::

    Hier werden PIL und ReportLab für Python 2.7 installiert. Falls du
    eine andere Python Version benutzt musst du die passenden Links
    unter den oben genannten URLs suchen.

Jetzt können die restlichen Pakete installiert werden::

    $ pip install pisa html5lib httplib2 pyPdf

.. _ReportLab: http://www.reportlab.com/
.. _PIL Homepage: http://www.pythonware.com/products/pil/
.. _ReportLab FTP Server: http://www.reportlab.com/ftp/

Ein generischer View für PDFs
=============================

Dann schreibst du in :file:`cookbook/views.py`: einen generischen View zum
Erzeugen von PDF Dateien:

..  literalinclude:: ../../src/cookbook/utils.py

Das PDF erzeugen
================

Jetzt fügst du den URL ``recipes_recipe_detail_pdf`` zu :file:`recipes/urls.py` hinzu::

    from .views import RecipeDetailView, RecipePDFView

    urlpatterns += patterns('',
        url(r'^rezept/(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(),
            name='recipes_recipe_detail'),
        url(r'^rezept/(?P<slug>[-\w]+)/pdf/$', RecipePDFView.as_view(),
            name='recipes_recipe_detail_pdf'),
        url(r'^$', RecipeListView.as_view(), name='recipes_recipe_index'),
    )

Und nun erstellst mit Hilfe des generischen PDF Views eine View zur
Erzeugung der PDFs der Rezepte in :file:`recipes/views.py`::

    from cookbook.views import PDFView


    class RecipePDFView(PDFView, RecipeDetailView):
        template_name = 'recipes/detail_pdf.html'

Damit die URLs im PDF auch die aktuelle Domain benutzen benötigen wir
noch ein kleines Template Tag. Dieses erstellst du wieder in
``recipes/templatetags/recipes.py``::

    from django.contrib.sites.models import Site


    @register.simple_tag
    def full_url(obj):
        """Returns the absolute URL for a model prefixed with the domain."""
        current_domain = Site.objects.get_current().domain
        return 'http://%s%s' % (current_domain, obj.get_absolute_url())


Jetzt fehlt noch das HTML Template, dass die Vorlage für das PDF ist. Erstelle
es hier :file:`recipes/templates/recipes/detail_pdf.html`:

..  literalinclude:: ../../src/cookbook/recipes/templates/recipes/detail_pdf.html

Und füge als letzten Schritt eine Link zum PDF in das Template für ein Rezept
ein :file:`recipes/templates/recipes/detail.html`::

    <a href="{% url 'recipes_recipe_detail_pdf' object.slug %}">Rezept als PDF herunterladen</a>

Jetzt kannst du das Rezept auch als PDF ansehen.
