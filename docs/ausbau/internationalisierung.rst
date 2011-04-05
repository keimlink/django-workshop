Internationalisierung
*********************

Um einen Applikation in verschiedenen Sprachen anbieten zu können ist
Internationalisierung (I18N) und Lokalisierung (L10N) notwendig. Django
benutzt dazu das `gettext Modul
<http://docs.python.org/library/gettext.html>`_ von Python.

Standard-Übersetzung
====================

Eine einfache Übersetzung im View würde mit Hilfe von ``ugettext`` wie folgt
durchgeführt werden::

    from django.utils.translation import ugettext as _ 
    
    def my_view(request):
        output = _("Welcome to my site.")
        return HttpResponse(output)

Mehrzahl
========

Um zwischen Einzahl und Mehrzahl zu unterscheiden steht die Funktion
``ungettext`` zur Verfügung::

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

Verzögerung der Übersetzung
===========================

In bestimmten Fällen bietet sich auch eine Verzögerung der Übersetzung mit
``ugettext_lazy`` an, zum Beispiel bei Models::

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

Mit Hilfe von ``string_concat`` lassen sich übersetzte Zeichenketten
zusammenfügen::

    from django.utils.translation import string_concat, ugettext_lazy
    
    car = ugettext_lazy(u'Audi')
    color = ugettext_lazy(u'silber')
    result = string_concat(car, ': ', color)

Templates übersetzen
====================

Natürlich kann man die Übersetzung auch innerhalb der Templateengine nutzen.

Hier für das Basistemplate ``templates/base.html``::

    {% load i18n %}
    <title>{% block title %}{% trans "Cookbook" %}{% endblock %}</title>

Zuerst werden die Templatetags zur Internationalisierung mit dem Befehl ``{%
load i18n %}`` geladen. Dann kann mit dem Tag ``trans`` ein Wort zur
Übersetzung markiert werden.

In einer Detailansicht mit Einzahl und Mehrzahl, wie zum Beispiel im Template
``templates/recipes/detail.html``, sieht es dann so aus::

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

Hier können mit dem Templatetag ``blocktrans`` ganze Blöcke von Text zur
Übersetzung markiert werden, auch unter Berücksichtigung von Singular und
Plural.

Mit einer Konstruktion wie ``{% blocktrans with object.time_for_preparation as
time_for_preparation %}`` ist es möglich einen generierten Wert in eine
Zeichenkette einzusetzen.

Locale Dateien erzeugen
=======================

Um nun die Übersetzung in eine andere Sprache durchführen zu können müssen die
Sprachdateien für Projekt und Applikation erzeugt werden.

Erzeugen der Sprachdateien für das Projekt::

    $ mkdir locale
    $ django-admin.py makemessages -l de

Und für die Applikation ``recipes``::

    $ cd recipes
    $ mkdir locale
    $ django-admin.py makemessages -l de

Dadurch wird die folgende Verzeichnisstruktur generiert::

    locale/
    `-- de
        `-- LC_MESSAGES
            `-- django.po

Die .po-Dateien
---------------

Jetzt kann in den erzeugten .po-Dateien mit der Übersetzung begonnen werden.

``locale/de/LC_MESSAGES/django.po``::

    #: templates/base.html:7 templates/base.html.py:10
    msgid "Cookbook"
    msgstr "Kochbuch"

``recipes/locale/de/LC_MESSAGES/django.po``::

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

Die .mo-Dateien erzeugen
------------------------

Nachdem die Übersetzung in den .po-Dateien durchgeführt worden ist können die
binären .mo-Dateien erzeugt werden. Dies muss auch wieder für das Projekt und
jede Applikation einzeln durchgeführt werden.

Für das Projekt im Projektverzeichnis::

    $ django-admin.py compilemessages

Und für die Applikation ``recipes``::

    $ cd recipes
    $ django-admin.py compilemessages

Die .mo-Datei wird im gleichen Verzeichnis wie die dazu gehörende .po-Datei
abgelegt::

    locale/
    `-- de
        `-- LC_MESSAGES
            |-- django.mo
            `-- django.po

``LocaleMiddleware`` Middleware einbinden
=========================================

Ohne weitere Konfiguration entscheidet Django anhand des Wertes von
``LANGUAGE_CODE`` welche Sprache benutzt wird. So benutzen alle Benutzer die
selbe Sprache.

Damit jeder Benutzer die Sprache selbst bestimmen kann muss eine Middleware
eingebunden werden: ``LocaleMiddleware``.

Dazu muss ``django.middleware.locale.LocaleMiddleware`` zu der Liste der
Middlewares ``MIDDLEWARE_CLASSES`` in der ``settings.py`` hinzugefügt werden.

Dabei ist die Reihenfolge wichtig:

* Nach ``SessionMiddleware`` einbinden, denn ``LocaleMiddleware`` benutzt
  Sessiondaten.
* Falls ``CacheMiddleware`` benutzt wird sollte ``LocaleMiddleware`` danach
  eingebunden werden.

In unser Konfiguration sieht es dann so aus::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'middleware.Http403Middleware'
    )

Wie ``LocaleMiddleware`` die Sprache ermittelt
----------------------------------------------

#. Zuerst wird der Schlüssel ``django_language`` in der Session gesucht.
#. Ist in der Session nichts definiert wird nach einem Cookie gesucht. Dessen Name ist in ``LANGUAGE_COOKIE_NAME`` definiert (Standard ist ``django_language``).
#. Ist der Cookie nicht vorhanden wird der ``Accept-Language`` HTTP Header untersucht. Wird dort eine Sprache gefunden, für die eine Übersetzung existiert, wird diese benutzt.
#. Schlagen alle vorherigen drei Methoden fehl wird ``LANGUAGE_CODE`` benutzt.

Einschränken der Sprachen
-------------------------

Um die Auswahl der Sprachen einzuschränken kann man die Liste der verfügbaren
Sprachen in der ``settings.py`` reduzieren::

    ugettext = lambda s: s
    
    LANGUAGES = (
        (’de’, ugettext(’German’)),
        (’en’, ugettext(’English’)),
    )

Das ``lambda``-Konstrukt ist notwenig, da ``django.utils.translation`` in der
``settings.py`` noch nicht zur Verfügung steht. Es hängt selbst von der
Konfiguration ab.

Damit die Namen der Sprachen auch wirklich übersetzt werden, muss dieser Code
noch einmal an einer Stelle eingesetzt werden, an der er auch wirklich
ausgeführt wird (zum Beispiel in der ``urls.py``).

Ausgewählte Sprache ermitteln
-----------------------------

Die ausgewählte Sprache wird von ``HttpRequest`` als Eigenschaft
``LANGUAGE_CODE`` zur Verfügung gestellt::

    def my_view(request):
        if request.LANGUAGE_CODE == ’de-at’:
            # do something

Weiterführende Links zur Django und Python Dokumentation
========================================================

* :djangodocs:`Internationalisierung und Lokalisierung <topics/i18n/>`
* `Lambdas <http://docs.python.org/reference/expressions.html#lambda>`_
