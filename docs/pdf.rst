************
PDF Creation
************

For the generation of PDF documents, there are various possibilities. We want
to use `wkhtmltopdf <http://wkhtmltopdf.org/>`_, which renders HTML into PDF
using the Qt WebKit rendering engine. WebKit is also used by Google Chrome,
Opera and Safari. It runs entirely "headless" and does not require a display or
display service.

Installing wkhtmltopdf
======================

You just have to `download <http://wkhtmltopdf.org/downloads.html>`_ and
install one of the precompiled binaries available for FreeBSD, Linux (CentOS,
Debian, Ubuntu) and Windows. Easy, isn't it?

You also have to install `django-wkhtmltopdf
<https://github.com/incuna/django-wkhtmltopdf>`_, which provides a Django view
to wrap the HTML to PDF conversion. But that's also just a single command:

::

    $ pip install django-wkhtmltopdf

Finally add ``wkhtmltopdf`` to ``INSTALLED_APPS`` in :file:`settings.py`.

A generic view for PDFs
=======================

As mentoined before django-wkhtmltopdf provides a view to convert HTML to PDF.
We need to extend this view so that it can render a recipe. Add the following
view to :file:`recipes/views.py`:

::

    from django.views.generic.detail import BaseDetailView

    from wkhtmltopdf.views import PDFTemplateView


    class RecipePDFView(BaseDetailView, PDFTemplateView):
        model = Recipe
        template_name = 'recipes/pdf.html'

        @property
        def filename(self):
            """Returns the filename of the PDF."""
            return '{}.pdf'.format(self.object.slug)

Creating the PDF
================

Now add the URL ``recipes_recipe_pdf`` to :file:`recipes/urls.py`:

::

    from . import views

    urlpatterns = [
        url(r'^recipe/(?P<slug>[-\w]+)/$', 'recipes.views.detail',
            name='recipes_recipe_detail'),
        url(r'^recipe/(?P<slug>[-\w]+)/pdf/$', views.RecipePDFView.as_view(),
            name='recipes_recipe_pdf'),
        url(r'^create/$', views.RecipeCreateView.as_view(), name='recipes_recipe_add_class'),
        url(r'^edit/(?P<recipe_id>\d+)/$', 'recipes.views.edit',
            name='recipes_recipe_edit'),
        url(r'^$', views.RecipeListView.as_view(), name='recipes_recipe_list'),
    ]

Now you just need the HTML template that will be the template for the PDF.
Create it in :file:`recipes/templates/recipes/pdf.html`:

.. code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - {{ object.title }}{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <h2>{{ object.title }}</h2>
    <p>Difficulty: {{ object.get_difficulty_display }}</p>
    <p>Makes {{ object.number_of_portions }} serving{{ object.number_of_portions|pluralize }}.</p>
    <h3>Ingredients</h3>
    {{ object.ingredients|linebreaks }}
    <h3>Preparation</h3>
    {{ object.preparation|linebreaks }}
    <p>Time for preparation: {{ object.time_for_preparation }} minutes</p>
    <p>Author: {{ object.author }}</p>
    <h4>Categorie{{ object.category.count|pluralize }}</h4>
    <ul>
        {% for category in object.category.all %}
            <li>{{ category.name }}</li>
        {% endfor %}
    </ul>
    {% endblock %}

Now add, as the last step, a link to download the PDF in the template for a recipe :file:`recipes/templates/recipes/detail.html`:

.. code-block:: html+django

    <a href="{% url 'recipes_recipe_pdf' object.slug %}">Download recipe as PDF</a>

Now you can download the recipe as a PDF!
