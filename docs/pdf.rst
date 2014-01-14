*************
PDF-Erzeugung
*************

Für die Erzeugung von PDF-Dokumenten gibt es verschiedene Möglichkeiten. Wir
wollen die Bibliothek pisa_ nutzen, die ein html2pdf Konverter ist.

.. _pisa: http://pypi.python.org/pypi/pisa

Installation der nötigen Pakete
===============================

Linux und OS X
--------------

::

    $ pip install pisa html5lib httplib2 pyPdf reportlab

Windows
-------

Für Windows muss ReportLab_ als Binärpaket mit Hilfe von
``easy_install`` installiert werden. Den Downloadlink für ReportLab
findest du auf dem `ReportLab FTP Server`_.

So wird das Paket installiert::

    > easy_install http://www.reportlab.com/ftp/reportlab-2.5.win32-py2.7.exe

.. note::

    Hier wird ReportLab für Python 2.7 installiert. Falls du
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
Erzeugen von PDF Dateien::

    import cStringIO as StringIO

    from django.http import HttpResponse
    from django.views.generic import DetailView
    import ho.pisa as pisa


    class PDFView(DetailView):
        def render_to_pdf(self, html):
            pdf = StringIO.StringIO()
            pisa.CreatePDF(html, pdf, encoding='utf-8')
            pdf.seek(0)
            return pdf

        @property
        def filename(self):
            return getattr(self.get_object(), self.slug_field)

        def render_to_response(self, context, **response_kwargs):
            tpl = super(PDFView, self).render_to_response(context, **response_kwargs)
            tpl.render()
            pdf = self.render_to_pdf(tpl.rendered_content)
            response = HttpResponse(pdf, mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s.pdf' % self.filename
            return response

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
es hier :file:`recipes/templates/recipes/detail_pdf.html`::

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - {{ object.title }}{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    {% load recipes %}
    <h2>{{ object.title }}</h2>
    <p>Schwierigkeitsgrad: {{ object.get_difficulty_display }}</p>
    <p>Ergibt {{ object.number_of_portions }}
        Portion{{ object.number_of_portions|pluralize:"en" }}.</p>
    <h3>Zutaten</h3>
    {{ object.ingredients|linebreaks }}
    <h3>Zubereitung</h3>
    {{ object.preparation|linebreaks }}
    <p>Zubereitungszeit: {{ object.time_for_preparation }} Minuten</p>
    <p>Autor: {{ object.author }}</p>
    <h4>Kategorie{{ object.category.count|pluralize:"n" }}</h4>
    <ul>
        {% for category in object.category.all %}
            <li>{{ category.name }}</li>
        {% endfor %}
    </ul>
    {% get_related_recipes object 5 as related_recipes %}
    {% if related_recipes %}
    <h4>Verwandte Rezepte</h4>
    <ul>
    {% for recipe in related_recipes %}
        <li><a href="{% full_url recipe %}">{{ recipe.title }}</a></li>
    {% endfor %}
    </ul>
    {% endif %}
    {% endblock %}

Und füge als letzten Schritt eine Link zum PDF in das Template für ein Rezept
ein :file:`recipes/templates/recipes/detail.html`::

    <a href="{% url 'recipes_recipe_detail_pdf' object.slug %}">Rezept als PDF herunterladen</a>

Jetzt kannst du das Rezept auch als PDF ansehen.
