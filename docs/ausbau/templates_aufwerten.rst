Templates aufwerten
*******************

Das Template zur Darstellung eines Rezepts ist bis jetzt sehr einfach
gehalten. Wir werden einige Eigenschaften des Models hinzufügen und die
Darstellung optimieren.

Anzahl der Portionen
====================

Alter Code:

..  code-block:: html+django

    <p>Ergibt {{ object.number_of_portions }} Portionen.</p>

Neuer Code:

..  code-block:: html+django

    <p>Ergibt {{ object.number_of_portions }} 
        Portion{{ object.number_of_portions|pluralize:"en" }}.</p>

Hier bestimmst du mit dem Filter ``pluralize``, ob das Attribut
``number_of_portions`` den Wert 1 oder höher hat. Ist der Wert höher, werden
die Buchstaben "en" angehängt.

Schwierigkeitsgrad
==================

Den Schwierigkeitsgrad haben wir bis jetzt noch nicht ausgegeben. Versuche es
mit diesem Code:

..  code-block:: html+django

    <p>Schwierigkeitsgrad: {{ object.difficulty }}</p>

Ist das Ergebnis wie erwartet? Nein, natürlich wird eine Zahl ausgegeben. Wir
hatten als Feldtyp auch ``SmallIntegerField`` gewählt.

Also brauchen wir einen Helfer, der uns statt der Zahl das Wort ausgibt.
Glücklicherweise kann jedes Model das zum Wert passende Label ausgeben.

Jedes Feld, dessen Schlüssel-Wert-Paare mit ``choices`` definiert wurden, hat
eine Methode ``get_FIELD_display()``. Diese gibt das Label aus.

Also kannst du folgenden Code im Template nutzen, um den Schwierigkeitsgrad
als Wort auszugeben:

..  code-block:: html+django

    <p>Schwierigkeitsgrad: {{ object.get_difficulty_display }}</p>

Autor
=====

Als nächstes wollen wir den Autor ausgeben, was wieder einfach ist:

..  code-block:: html+django

    <p>Autor: {{ object.author }}</p>

Kategorien
==========

Jetzt fehlen nur noch die Kategorien. Um zu verstehen, wie die Kategorien im
Template ausgegeben werden können müssen wir uns erst das Model ansehen:

..  code-block:: pycon

    $ python manage.py shell
    Python 2.6.1 (r261:67515, Feb 11 2010, 00:51:29) 
    [GCC 4.2.1 (Apple Inc. build 5646)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from recipes.models import Recipe
    >>> r = Recipe.objects.all()[1]
    >>> r.category
    <django.db.models.fields.related.ManyRelatedManager object at 0x1011f8490>
    >>> r.category.all()
    [<Category: Hauptspeise>, <Category: Leckere Salate>]
    >>> r.category.count()
    2

Das Attribut ``category`` einer Instanz von ``Recipe`` ist also ein Manager,
genauer ein spezieller ``ManyRelatedManager``. Dieser verhält sich ähnlich wie
der Standard-Manager ``Recipe.objects`` (siehe Kapitel :ref:`datenbank-api`).
Du kannst so zum Bespiel alle Kategorien oder ihre Anzahl abfragen.

Deshalb können wir den folgenden Code nutzen, um die Kategorien auszugeben:

..  code-block:: html+django

    <h4>Kategorie{{ object.category.count|pluralize:"n" }}</h4>
    <ul>
        {% for category in object.category.all %}
            <li>{{ category.name }}</li>
        {% endfor %}
    </ul>

Weiterführende Links zur Django Dokumentation
=============================================

* `Eingebaute Templatetags und Filter <http://docs.djangoproject.com/en/1.2/ref/templates/builtins/#ref-templates-builtins>`_
* `Zusätzliche Methoden der Model-Instanzen <http://docs.djangoproject.com/en/1.2/ref/models/instances/#extra-instance-methods>`_
* `Manager für "Relations" <http://docs.djangoproject.com/en/1.2/ref/models/relations/#ref-models-relations>`_
