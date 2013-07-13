Datenbank und Entwicklungs-Webserver
************************************

Nun können wir die Datenbank füllen und danach den Entwicklungs-Webserver auf
rufen, um die Admin-Applikation zu benutzen.

Datenmodel überprüfen
=====================

Als erstes solltest du dein Datenmodel mit folgendem Kommando überprüfen:

..  code-block:: bash

    $ python manage.py validate

Django überprüft das Datenmodel automatisch bei allen Operationen, die Models
benutzten. Mit Hilfe dieses Befehls kannst du die Prüfung auch gezielt
durchführen.

Datenbank synchronisieren
=========================

Aus den Models müssen nun SQL Queries erzeugt werden, um die Datenbank zu
füllen.

Mit dem folgenden Kommando kannst du dir die Queries ausgeben lassen:

..  code-block:: bash

    $ python manage.py sqlall recipes

..  code-block:: sql

    BEGIN;
    CREATE TABLE "recipes_category" (
        "id" integer NOT NULL PRIMARY KEY,
        "name" varchar(100) NOT NULL,
        "slug" varchar(50) NOT NULL UNIQUE,
        "description" text NOT NULL
    )
    ;
    CREATE TABLE "recipes_recipe_category" (
        "id" integer NOT NULL PRIMARY KEY,
        "recipe_id" integer NOT NULL,
        "category_id" integer NOT NULL REFERENCES "recipes_category" ("id"),
        UNIQUE ("recipe_id", "category_id")
    )
    ;
    CREATE TABLE "recipes_recipe" (
        "id" integer NOT NULL PRIMARY KEY,
        "title" varchar(255) NOT NULL,
        "slug" varchar(50) NOT NULL UNIQUE,
        "ingredients" text NOT NULL,
        "preparation" text NOT NULL,
        "time_for_preparation" integer,
        "number_of_portions" integer NOT NULL,
        "difficulty" smallint NOT NULL,
        "author_id" integer NOT NULL REFERENCES "auth_user" ("id"),
        "date_created" datetime NOT NULL,
        "date_updated" datetime NOT NULL
    )
    ;
    CREATE INDEX "recipes_recipe_cc846901" ON "recipes_recipe" ("author_id");
    COMMIT;

Um diese Queries direkt auszuführen und so die Tabellen und Indizes anzulegen
musst du folgendes Kommando ausführen::

    $ python manage.py syncdb
    Creating tables ...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table recipes_category
    Creating table recipes_recipe_category
    Creating table recipes_recipe

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (leave blank to use 'vagrant'): admin
    E-mail address: admin@example.com
    Password:
    Password (again):
    Superuser created successfully.
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

..  note::

    Weil die in Django enthaltene App zur Authentifizierung zum ersten mal
    installiert wird, wird auch ein neuer Superuser angelegt.

Entwicklungs-Webserver starten
==============================

Nachdem die Datenbank erstellt wurde kannst du den Entwicklungs-Webserver
starten:

..  code-block:: bash

    $ python manage.py runserver
    Validating models...

    0 errors found
    Django version 1.5.1, using settings 'cookbook.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Unter der URL http://127.0.0.1:8000/admin/ kannst du nun die Admin-Applikation
aufrufen, dich mit dem eben erstellten Superuser anmelden und ein paar Rezepte
anlegen.

Export und Import von Daten mit Hilfe von JSON
==============================================

Damit man Daten zwischen verschiedenen Systemen austauschen kann gibt es in
Django eingebaute Export- und Importfunktionen. Mit dem Kommando
:program:`dumpdata` kannst du die eben erstellten Models aus der Applikation
``recipes`` exportieren::

    $ mkdir recipes/fixtures
    $ python manage.py dumpdata --indent 4 recipes > recipes/fixtures/initial_data.json

Django lädt die Fixtures aus einer Datei mit dem Namen
:file:`initial_data.json` jedes mal wenn du :program:`syncdb` ausführst. Die
gerade gespeicherten Daten werden also automatisch geladen wenn du die Models
löscht und neu anlegst.

Außerdem kannst du die Daten auch manuell mit dem Befehl :program:`loaddata` laden::

    $ python manage.py loaddata recipes/fixtures/initial_data.json
    Installed 4 object(s) from 1 fixture(s)

.. note::

    Um Daten aus anderen Quellen in Django zu importieren eignet sich
    :program:`loaddata` nur bedingt, da in den Fixtures auch immer die
    Primärschlüssel definiert sind. Es gibt andere Apps, wie zum Beispiel `CSV
    importer`_, die besser zum regelmäßigen Import von neuen Daten geeignet
    sind.

.. _CSV importer: http://django-csv-importer.readthedocs.org/

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Informationen zu django-admin.py and manage.py <ref/django-admin/#ref-django-admin>`
* :djangodocs:`Daten für die Erstellung der Models bereit stellen <howto/initial-data/>`
