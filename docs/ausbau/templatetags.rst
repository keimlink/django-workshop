..  _templatetags:

Templatetags
************

Mit den Templatetags, die Django zur Verfügung stellt, lässt sich gut
arbeiten. Wirklich interessant ist aber die Möglichkeit eigene Templatetags zu
schreiben.

Wir wollen ein Templatetag für unser Projekt schreiben mit dem wir ermitteln
können ob ein Benutzer der Autor eines Rezeptes ist. Außerdem soll es die
Möglichkeit bieten einen alternativen Block zu rendern, wenn dies nicht der
Fall ist.

Das Templatetag dafür soll also so aussehen:

..  code-block:: html+django

    {% is_author user recipe %}
        Der Benutzer ist Autor des Rezepts oder Redakteur.
    {% else %}
        Dieses Rezept darf von diesem Benutzer nicht bearbeitet werden.
    {% endis_author %}

Das Templatetag ist ``is_author``. Das erste Argument ``user`` ist ein User
Objekt. Das zweite Argument ``recipe`` ist eine Recipe Instanz. Ansonsten soll
das Templatetag wie eine ``if``-Bedingung funktionieren.

Die Verzeichnisstruktur für Templatetags
========================================

Templatetags müssen mit einer bestimmten Verzeichnisstruktur angelegt werden.
Im Verzeichnis der Applikation wird ein neues Verzeichnis :file:`templatetags`
erstellt. Darin wird die leere Datei :file:`__init__.py` angelegt, um das
Verzeichnis als Python Package zu markieren. Als letztes legen wir eine Python
Datei an, die das Modul für unsere Templatetags ist. Unser erstes Modul nennen
wir :file:`recipes.py`.

..  code-block:: bash

    recipes/
    `-- templatetags
        |-- __init__.py
        `-- recipes.py

Das Templatetag erstellen
=========================

Ein Templatetag besteht immer aus einer Kompilierungsfunktion und einer Node.
Die Kompilierungsfunktion parst das Tag mit Hilfe eines Parsers. Als Ergebnis
gibt sie eine Instanz der Node zurück. Diese hat eine ``render``-Methode, die
die Ausgabe erzeugt.

Die Kompilierungsfunktion
-------------------------

Zuerst erstellt du die Kompilierungsfunktion in der neu angelegten Datei
:file:`recipes.py`:

..  code-block:: python

    from django import template

    register = template.Library()

    @register.tag(name='is_author')
    def do_is_author(parser, token):
        """The ``{% is_author %}`` tag displays the first section, if the user is
        the author of the recipe or a staff member. Otherwise the second section
        is displayed.

        ::

            {% is_author user recipe %}
                The user is owner of this recipe or a staff member.
            {% else %}
                The user has no permissions to edit this recipe.
            {% endis_author %}
        """
        try:
            tag_name, user, recipe = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                '%s requires a Recipe and an User as arguments' % token.contents.split()[0])
        nodelist_true = parser.parse(('else', 'endis_author'))
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('endis_author',))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()
        return IsAuthorNode(user, recipe, nodelist_true, nodelist_false)

Der Renderer
------------

Danach schreibst du die Node, die die Ausgabe rendert. Dieser Code muss
oberhalb der Funktion ``do_is_author`` stehen, denn sonst steht die Klasse
``IsAuthorNode`` nicht in der Funktion zur Verfügung.

..  code-block:: python

    class IsAuthorNode(template.Node):
        def __init__(self, user, recipe, nodelist_true, nodelist_false):
            self.user = template.Variable(user)
            self.recipe = template.Variable(recipe)
            self.nodelist_true = nodelist_true
            self.nodelist_false = nodelist_false

        def render(self, context):
            try:
                user = self.user.resolve(context)
                recipe = self.recipe.resolve(context)
            except template.VariableDoesNotExist:
                return ''
            if recipe.author.id == user.id or user.is_staff:
                return self.nodelist_true.render(context)
            else:
                return self.nodelist_false.render(context)

Das Templatetag nutzen
======================

Nun kannst du das neue Templatetag nutzen, zum Beispiel im Template
:file:`recipes/templates/recipes/detail.html`.

Dazu muss zuerst unser Templatetag geladen werden. Das machst du am besten im
Kopf des Templates:

..  code-block:: html+django

    {% load recipes %}

..  note::

    Der Bezeichner hinter dem ``load`` Templatetag ist immer der Name des Python
    Moduls, dass die Templatetags enthält, die geladen werden sollen (ohne die
    Endung ".py"). Das Python Modul muss sich im Verzeichnis ``templatetags``
    einer installierten Applikation befinden.

Dann ersetzt du die Zeile:

..  code-block:: html+django

    <a href="{% url 'recipes_recipe_edit' object.pk %}">Rezept bearbeiten</a>

Mit dem neuen Templatetag:

..  code-block:: html+django

    {% is_author user object %}
        <a href="{% url 'recipes_recipe_edit' object.pk %}">Rezept bearbeiten</a>
    {% else %}
        Bitte als Autor des Rezepts oder als Redakteur
        <a href="{% url 'userauth_login' %}">einloggen</a>, um das Rezept zu bearbeiten.
    {% endis_author %}

Django Apps zum einfachen Schreiben von Templatetags
====================================================

Da das Schreiben von Templatetags mit Django Bordmitteln recht umständlich ist,
sind verschiedene Django Apps entstanden, die dies vereinfachen. Eine Übersicht
gibt das `Templatetags Grid`_ auf Django Packages. Zwei der populärsten
Templatetag Apps sind django-classy-tags_ und django-ttag_.

.. _Templatetags Grid: http://www.djangopackages.com/grids/g/templatetags/
.. _django-classy-tags: http://pypi.python.org/pypi/django-classy-tags/
.. _django-ttag: http://pypi.python.org/pypi/django-ttag

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Eigene Templatetags und Filter schreiben <howto/custom-template-tags/#howto-custom-template-tags>`
