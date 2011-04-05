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
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table recipes_category
    Creating table recipes_recipe_category
    Creating table recipes_recipe

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (Leave blank to use 'zappi'): admin
    E-mail address: admin@example.com
    Password: 
    Password (again): 
    Superuser created successfully.
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for recipes.Recipe_category model
    Installing index for recipes.Recipe model
    No fixtures found.

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

    Django version 1.3, using settings 'cookbook.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Unter der URL http://127.0.0.1:8000/admin/ kannst du nun die Admin-Applikation
aufrufen, dich mit dem eben erstellten Superuser anmelden und ein paar Rezepte
anlegen.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Informationen zu django-admin.py and manage.py <ref/django-admin/#ref-django-admin>`
