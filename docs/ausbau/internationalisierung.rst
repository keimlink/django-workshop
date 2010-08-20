Internationalisierung
*********************

Standard-Übersetzung
====================

::

    from django.utils.translation import ugettext as _ 
    
    def my_view(request):
        output = _("Welcome to my site.")
        return HttpResponse(output)

Mehrzahl
========

::

    from django.utils.translation import ungettext

    count = Report.objects.count()
    if count == 1:
        name = Report._meta.verbose_name
    else:
        name = Report._meta.verbose_name_plural

    text = ungettext(
            'There is %(count)d %(name)s available.',
            'There are %(count)d %(name)s available.',
            count
    ) % {
        'count': count,
        'name': name
    }

Späte Übersetzung
=================

::

    from django.utils.translation import ugettext_lazy as _

    class Recipe(models.Model):
    ...
    ingredients = models.TextField(_('ingredients'),
        help_text=_('Enter one ingredient per line'))
    ...
    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')    

Übersetzte Zeichenketten zusammenfügen
--------------------------------------

::

    from django.utils.translation import string_concat, ugettext_lazy
    
    car = ugettext_lazy(u'Audi')
    color = ugettext_lazy(u'silber')
    result = string_concat(car, ': ', color)

Templates übersetzen
====================

templates/base.html

::

    {% load i18n %}
    <title>{% block title %}{% trans "Cookbook" %}{% endblock %}</title>

templates/recipes/detail.html

::

    {% load i18n %}
    ...
    {% blocktrans count object.number_of_portions as number_of_portions %}
    <p>Ergibt eine Portion.</p>
    {% plural %}
    <p>Ergibt {{ number_of_portions }} Portionen.</p>
    {% endblocktrans %}
    ...
    {% blocktrans with object.time_for_preparation as time_for_preparation %}
    <p>Zubereitungszeit: {{ time_for_preparation }} Minuten</p>
    {% endblocktrans %}

Locale Dateien erzeugen
=======================

Projekt::

    $ mkdir locale
    $ django-admin.py makemessages -l de

App ``recipes``::

    $ cd recipes
    $ mkdir locale
    $ django-admin.py makemessages -l de

Die .po-Dateien
===============

::

    #: templates/base.html:7 templates/base.html.py:10
    msgid "Cookbook"
    msgstr "Kochbuch"

    #: templates/recipes/detail.html:11
    #, python-format
    msgid ""
    "\n"
    "    Gives one portion.\n"
    "    "
    msgid_plural ""
    "\n"
    "    Gives %(number_of_portions)s portions.\n"
    "    "
    msgstr[0] ""
    "\n"
    "    Ergibt eine Portion.\n"
    "    "
    msgstr[1] ""
    "\n"
    "    Ergibt %(number_of_portions)s Portionen.\n"
    "    "

Middleware
==========

``django.middleware.locale.LocaleMiddleware`` nach ``SessionMiddleware`` einbinden.

TODO: Reihenfolge der Auswertung durch die Middleware
