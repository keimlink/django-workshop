********************
Internationalisation
********************

In order to offer an application in different languages​​,
Internationalization (I18N) and localization (L10N) is necessary. Django
uses Python's `gettext <http://docs.python.org/library/gettext.html>`_
module to do this.

Django needs at least Version 0.15 of
`GNU gettext <https://www.gnu.org/software/gettext/>`_. On Linux and OS
X it can be easily installed using a package manager. The
:djangodocs:`Installation on Windows <topics/i18n/translation/#gettext-on-windows>`
is described in the Django Documentation. The archive containing the
files for Windows can be found
`here <https://bitbucket.org/keimlink/django-workshop/downloads>`_.

Standard translation
====================

A simple translation in a view could be manually performed with the help
of ``ugettext`` as follows::

    from django.utils.translation import ugettext as _

    def my_view(request):
        output = _("Welcome to my site.")
        return HttpResponse(output)

Plural
======

To distinguish between singular and plural the function ``ungettext`` is
available::

    from django.utils.translation import ungettext

    count = Recipe.objects.count()
    if count == 1:
        name = Recipe._meta.verbose_name
    else:
        name = Recipe._meta.verbose_name_plural

    text = ungettext(
            'There is %(count)d %(name)s available.',
            'There are %(count)d %(name)s available.',
            count
    ) % {
        'count': count,
        'name': name
    }

Delayed translation
===================

In certain cases, for example in models, performing a delayed
translation using ``ugettext_lazy`` is helpful::

    from django.utils.translation import ugettext_lazy as _

    class Recipe(models.Model):
    ...
    ingredients = models.TextField(_('ingredients'),
        help_text=_('Enter one ingredient per line'))
    ...
    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

Merge translated strings
------------------------

Using ``string_concat`` translated strings can be put together::

    from django.utils.translation import string_concat, ugettext_lazy

    car = ugettext_lazy(u'Audi')
    color = ugettext_lazy(u'silber')
    result = string_concat(car, ': ', color)

Translating Templates
=====================

Of course you can use the translation within the template engine.

Here we translate the base template :file:`templates/base.html`::

    {% load i18n %}
    <title>{% block title %}{% trans "Cookbook" %}{% endblock %}</title>

First, the template tags for internationalization are loaded with the
command ``{% load i18n %}``. Then the tag ``trans`` can be used to mark
a word for translation.

In a detail view with singular and plural, such as in the template
:file:`templates/recipes/detail.html`, it looks like this::

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

The template tag ``blocktrans`` can be used to mark whole blocks of text
for translation, including consideration of singular and plural.

With a design like ``{% blocktrans with object.time_for_preparation as
time_for_preparationx%}`` it is possible to insert a generated value
into astring.

Generate locale files
=====================

In order to be able to perform the translation into another language, the
language files for project and application must be generated.

First, the location of the language files needs to be set in the
configuration :file:`settings.py`.

::

    LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

Then you can create the message file::

    $ mkdir locale
    $ django-admin.py makemessages -l de

Thus, the following directory structure is generated::

    locale/
    `-- de
        `-- LC_MESSAGES
            `-- django.po

The .po file
------------

Now, start with translating the generated .po file
:file:`locale/de/LC_MESSAGES/django.po`::

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

Create the .mo file
-------------------

After the translation was carried out in the .po file, the
binary .mo file will be generated::

    $ django-admin.py compilemessages

The .mo file will be stored in the same directory as the associated .po
file::

    locale/
    `-- de
        `-- LC_MESSAGES
            |-- django.mo
            `-- django.po

Embed ``LocaleMiddleware`` middleware
=====================================

Without further configuration Django decides on the basis of the value of
``LANGUAGE_CODE`` which language to use. Thus, all users use the
same language.

To enable each user to choose the language for itself, a middleware
needs to be included: ``LocaleMiddleware``.

This requires ``django.middleware.locale.LocaleMiddleware`` to be added
to the list of middlewares ``MIDDLEWARE_CLASSES`` in :file:`settings.py`.

The order is important:

* Integrate after ``SessionMiddleware``, because ``LocaleMiddleware`` uses session data.
* If ``CacheMiddleware`` is used ``LocaleMiddleware`` should be involved afterwards.

In our configuration, it looks like this::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

How ``LocaleMiddleware`` determines the language
------------------------------------------------

#. First, the key ``django_language`` is searched for in the session.
#. If nothing is defined in the session, it looks for a cookie whose name is defined in ``LANGUAGE_COOKIE_NAME`` (default is ``django_language``).
#. Is the cookie is not present that ``Accept-Language`` HTTP header is investigated. If there is a language for which there is a translation, it will be used.
#. If all the previous three methods fail ``LANGUAGE_CODE`` will be used.

Limit the languages
-------------------

In order to restrict the choice of languages ​​you reduce the list of
available languages ​​in :file:`settings.py`::

    ugettext = lambda s: s

    LANGUAGES = (
        (’de’, ugettext(’German’)),
        (’en’, ugettext(’English’)),
    )

The ``lambda`` construct is necessary because
``django.utils.translation`` is not yet available in
:file:`settings.py`. It also depends on the configuration.

Thus the names of the languages ​​are actually translated, that code
must be used again at a position at which it actually is executed (for
example :file:`urls.py`).

Determine the selected Language
-------------------------------

The selected language is available as property ``LANGUAGE_CODE`` on each
instance of ``HttpRequest``::

    def my_view(request):
        if request.LANGUAGE_CODE == ’de-at’:
            # do something

Further links to the Django and Python documentation
====================================================

* :djangodocs:`Internationalization and localization <topics/i18n/>`
* `Lambdas <http://docs.python.org/reference/expressions.html#lambda>`_
