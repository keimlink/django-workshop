Doctests schreiben
******************

Doctests sind die einfachste Art Tests zu schreiben. Starte dafür eine Python Shell und führe einige Operationen an der Datenbank durch, ähnlich wie im Kapitel :ref:`datenbank-api`.

..  code-block:: pycon

    $ python manage.py shell
    Python 2.6.1 (r261:67515, Feb 11 2010, 00:51:29) 
    [GCC 4.2.1 (Apple Inc. build 5646)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from recipes.models import Recipe
    >>> title = 'Doctest'
    >>> from django.template.defaultfilters import slugify
    >>> from django.contrib.auth.models import User
    >>> admin = User.objects.get(username='admin')
    >>> r = Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    >>> r.title
    'Doctest'
    >>> r.slug
    u'doctest'
    >>> r.number_of_portions
    4
    >>> r.author
    <User: admin>
    >>> import datetime
    >>> r.date_created.date() == datetime.datetime.now().date()
    True
    >>> r.date_updated.date() == datetime.datetime.now().date()
    True
    >>> r.difficulty == Recipe.DIFFICULTY_MEDIUM
    True

Die gerade durchgeführten Operationen haben ein neues Rezept erstellt und einige Attribute getestet.

Jetzt wollen wir noch einige Fehler provozieren:

..  code-block:: pycon

    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    Traceback (most recent call last):
      ...
    IntegrityError: column slug is not unique
    >>> title = 'Doctest 2'
    >>> Recipe.objects.create(title=title, slug=slugify(title))
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.number_of_portions may not be NULL
    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4)
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.author_id may not be NULL

Damit sind wir mit der Erstellung der Doctests fertig. Du musst den Code aus der Shell jetzt nur noch in die Datei ``recipes/tests.py`` kopieren. Und zwar als Ersatz für den einfachen Beispiel-Doctest::

    __test__ = {"doctest": """
    Another way to test that 1 + 1 is equal to 2.

    >>> 1 + 1 == 2
    True
    """}

Da der Benutzer "admin" in der Testdatenbank nicht existiert musst du ihn manuell während des Tests erstellen. Ersetze dazu die Zeile::

    >>> admin = User.objects.get(username='admin')

mit folgendem Code::

    >>> admin = User.objects.create(username='admin', password='admin')

Die Datei ``recipes/tests.py`` sieht dann so aus::

    """
    This file demonstrates two different styles of tests (one doctest and one
    unittest). These will both pass when you run "manage.py test".

    Replace these with more appropriate tests for your application.
    """

    from django.test import TestCase

    class SimpleTest(TestCase):
        def test_basic_addition(self):
            """
            Tests that 1 + 1 always equals 2.
            """
            self.failUnlessEqual(1 + 1, 2)

    __test__ = {"doctest": """
    >>> from recipes.models import Recipe
    >>> title = 'Doctest'
    >>> from django.template.defaultfilters import slugify
    >>> from django.contrib.auth.models import User
    >>> admin = User.objects.create(username='admin', password='admin')
    >>> r = Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    >>> r.title
    'Doctest'
    >>> r.slug
    u'doctest'
    >>> r.number_of_portions
    4
    >>> r.author
    <User: admin>
    >>> import datetime
    >>> r.date_created.date() == datetime.datetime.now().date()
    True
    >>> r.date_updated.date() == datetime.datetime.now().date()
    True
    >>> r.difficulty == Recipe.DIFFICULTY_MEDIUM
    True
    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4, author=admin)
    Traceback (most recent call last):
      ...
    IntegrityError: column slug is not unique
    >>> title = 'Doctest 2'
    >>> Recipe.objects.create(title=title, slug=slugify(title))
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.number_of_portions may not be NULL
    >>> Recipe.objects.create(title=title, slug=slugify(title), number_of_portions=4)
    Traceback (most recent call last):
      ...
    IntegrityError: recipes_recipe.author_id may not be NULL
    """}

..  note::

    Die Details der Tracebacks werden wirklich durch den String "..." ersetzt.

Jetzt kannst du mit dem Kommando ``python manage.py test recipes -v 2`` die Tests laufen lassen und sehen, dass die Doctests ausgeführt werden. Mit ``python manage.py test recipes.doctest -v 2`` kannst du auch nur die Doctests alleine aufrufen.

Vor- und Nachteile von Doctests
===============================

Vorteile
--------

* Einfach zu Erstellen
* Gleichzeitig Dokumentation des Codes
* Tests sind dort, wo sich auch der Quellcode befindet

Nachteile
---------

* Dokumentation kann zu umfangreich werden (kann durch Verschieben in die Testsuite umgangen werden)
* Ausgabe beim Ausführen der Tests nicht immer eindeutig
* Abhängigkeiten von der Umgebung (zum Beispiel Ausgaben im Interpreter)
* Datenbank-Operationen sind nicht in Transaktionen gekapselt
* Unicode-Probleme