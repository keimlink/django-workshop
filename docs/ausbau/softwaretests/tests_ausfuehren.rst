Tests ausführen
***************

In Django ist bereits ein Framework für Softwaretests integriert - das "Python unit testing framework".

Der Test Runner erstellt bei jeden Start eine SQLite Datenbank für die Tests und lässt alle Tests voneinander abgekapselt in Transaktionen laufen. Bei der Auswahl des Datenbanksystems richtet sich der Test Runner nach dem Backend, der in der ``settings.py`` konfiguriert wurde.

Tests für alle Applikationen durchführen
========================================

Mit dem Befehl ``python manage.py test`` werden alle für das Projekt installierten Applikationen getestet::

    $ python manage.py test
    Creating test database 'default'...
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
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for recipes.Recipe_category model
    Installing index for recipes.Recipe model
    No fixtures found.
    ..........................................................................
    ..........................................................................
    ..........
    ----------------------------------------------------------------------
    Ran 158 tests in 3.406s

    OK
    Destroying test database 'default'...

Tests für eine Applikation durchführen
======================================

Man kann auch gezielt eine Applikation testen::

    $ python manage.py test recipes
    Creating test database 'default'...
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
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    Installing index for recipes.Recipe_category model
    Installing index for recipes.Recipe model
    No fixtures found.
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.097s

    OK
    Destroying test database 'default'...

Ausgabe der Tests verändern
===========================

Mit dem Parameter ``-v 0`` wird der Großteil der Ausgaben des Test Runners unterdrückt::

    $ python manage.py test recipes -v 0
    ----------------------------------------------------------------------
    Ran 2 tests in 0.007s

    OK

Umgekehrt kannst du mit dem Parameter ``-v 2`` alle Details beim Ablaufen der Tests beobachten::

    $ python manage.py test recipes -v 2
    Creating test database 'default'...
    Processing auth.Permission model
    Creating table auth_permission
    ...
    Running post-sync handlers for application auth
    Adding permission 'auth | permission | Can add permission'
    Adding permission 'auth | permission | Can change permission'
    Adding permission 'auth | permission | Can delete permission'
    ...
    No custom SQL for auth.Permission model
    ...
    Installing index for auth.Permission model
    ...
    Loading 'initial_data' fixtures...
    ...
    No fixtures found.
    test_basic_addition (recipes.tests.SimpleTest) ... ok
    Doctest: recipes.tests.__test__.doctest ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.008s

    OK
    Destroying test database 'default'...