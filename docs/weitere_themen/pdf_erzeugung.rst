PDF-Erzeugung
*************

Für die Erzeugung von PDF-Dokumenten gibt es verschiedene Möglichkeiten. Wir
wollen die Bibliothek pisa_ nutzen, die ein html2pdf Konverter ist.

.. _pisa: http://pypi.python.org/pypi/pisa

Installation der nötigen Pakete
===============================

Zuerst müssen alle nötigen Pakete installiert werden::

    $ pip install pisa PIL html5lib httplib2 pyPdf reportlab

Ein generischer View für PDFs
=============================

Dann schreibst du in :file:`cookbook/views.py`: einen generischen View zum
Erzeugen von PDF Dateien:

..  literalinclude:: ../../src/cookbook/utils.py

Das PDF erzeugen
================

Jetzt fügst du den URL ``recipes_recipe_detail_pdf`` zu :file:`recipes/urls.py` hinzu::

    urlpatterns += patterns('',
        url(r'^rezept/(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(),
            name='recipes_recipe_detail'),
        url(r'^rezept/(?P<slug>[-\w]+)/pdf/$', RecipePDFView.as_view(),
            name='recipes_recipe_detail_pdf'),
        url(r'^$', RecipeListView.as_view(), name='recipes_recipe_index'),
    )

Und nun erstellst mit Hilfe des generischen PDF Views eine View für die PDFs
der Rezepte in :file:`recipes/views.py`::

    from utils import PDFView


    class RecipePDFView(PDFView):
        model = Recipe
        template_name = 'recipes/detail_pdf.html'

Jetzt fehlt noch das HTML Template, dass die Vorlage für das PDF ist. Erstelle
er hier :file:`recipes/templates/recipes/detail_pdf.html`:

..  literalinclude:: ../../src/cookbook/recipes/templates/recipes/detail_pdf.html

Und füge als letzten Schritt eine Link zum PDF in das Template für ein Rezept
ein :file:`recipes/templates/recipes/detail.html`::

    <a href="{% url recipes_recipe_detail_pdf object.slug %}">Rezept als PDF herunterladen</a>

Jetzt kannst du das Rezept auch als PDF ansehen.
