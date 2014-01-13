*************************
Functional and Unit Tests
*************************

Django’s uses the Python standard library module
`unittest <http://docs.python.org/library/unittest.html>`_ for unit
tests.

Running the tests
=================

You can run the tests with the following command:

.. command-output:: python manage.py test
    :cwd: ../src/cookbook

To get a more detailed output use the :option:`-v2` option:

.. command-output:: python manage.py test -v2
    :cwd: ../src/cookbook
    :ellipsis: 10

Use the :option:`-v0` option to hide most of the output:

.. command-output:: python manage.py test -v0
    :cwd: ../src/cookbook

You can also run the tests for a single application:

.. command-output:: python manage.py test recipes
    :cwd: ../src/cookbook

Or just for a single test case:

.. command-output:: python manage.py test messages.SessionTest
    :cwd: ../src/cookbook

And even for a single test method:

.. command-output:: python manage.py test messages.SessionTest.test_add
    :cwd: ../src/cookbook

Doctests
========

`Doctests <http://docs.python.org/library/doctest.html>`_ are also
supported by Django. But for the use with Django they have more
disadvantages than benefits.

Benefits
--------

- Easy to create
- At the same documentation of the code
- Tests are where the source code is

Disadvantages
-------------

* Documentation may be too large (can be bypassed by moving them to the test suite)
* Output of the test execution is not always clear
* Dependencies on the environment (eg interpreter output)
* Database operations are not encapsulated in transactions
* Unicode problems

Therefore we won't write any doctests.

Unit tests
==========

Before we can write the first tests we have to install an additional package::

    $ pip install freezegun

The file :file:`recipes/tests.py` currently contains a sample test:

.. literalinclude:: ../src/cookbook/recipes/tests.py

Replace it with the following code:

.. literalinclude:: ../src/cookbook_tests/recipes/tests.py

And run the tests:

.. command-output:: python manage.py test recipes.RecipeSaveTest
    :cwd: ../src/cookbook_tests

Unit tests have much more benefits than disadvantages:

Benefits
--------

* Output of the test execution is clear
* Each test can be called individually
* Clearly separated from the source code (can also be a disadvantage)
* Fewer dependencies on the environment
* Each method of a test class is automatically called within a transaction
* No Unicode problems
* Individual tests can be subject to conditions

Disadvantages
-------------

* Creating the unit test requires more effort than creating doctests
* Also, a documentation of the source code, but not as obvious as the doctest

Determine test coverage
=======================

Of course it is also important to know for which parts of the
application tests were already written. Here the Python package
`coverage <http://nedbatchelder.com/code/coverage/>`_ can help to
retrieve this information. It is not integrated in Django and
therefore must be manually installed::

    $ pip install coverage

Thus :program:`coverage` only examines our applications and not the
Framework you create the file :file:`.coveragerc` with the following
contents:

.. literalinclude:: ../src/cookbook_tests/.coveragerc
    :language: ini

Now you can create the data for the coverage report of the application
``recipes`` with the following command:

.. command-output:: coverage run manage.py test recipes
    :cwd: ../src/cookbook_tests

Display the coverage data with this command in the shell:

.. command-output:: coverage report -m
    :cwd: ../src/cookbook_tests

You can create a HTML coverage report with this command::

    $ coverage html

The HTML files are located in the directory :file:`htmlcov`.

Organizing tests as a package
=============================

Since the amount of tests is usually so large that a single file for all
test will quickly become confusing, it makes sense to organize the tests
as a Python package.

Create a new directory :file:`tests` inside the :file:`recipes`
directory and inside the new directory a file called :file:`__init__.py`::

    $ cd recipes
    $ mkdir tests
    $ touch tests/__init__.py

Now you move the file :file:`tests.py` in the new directory and
rename it to :file:`model_tests.py`::

    $ mv tests.py tests/model_tests.py

Next, you delete also the bytecode file :file:`tests.py` so this does
not prevent the execution of the code in the :file:`tests` package::

    $ rm tests.pyc

Last you add the following code to the file
:file:`recipes/tests/__init__.py`, so that our tests from the module
:file:`model_tests` are also discovered:

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/__init__.py
    :lines: 1

Functional tests (testing views)
================================

With the built-in Django test client an easy test browser is at your
disposal.

First we need some fixtures so that data in the front end is available
for testing.

Create a directory :file:`fixtures` for the applications :file:`recipes`
and :file:`userauth`::

    $ mkdir recipes/fixtures
    $ mkdir userauth/fixtures

Then you create a JSON file with the models of each application::

    $ python manage.py dumpdata recipes --indent 4 > recipes/fixtures/view_tests_data.json
    $ python manage.py dumpdata auth --indent 4 > userauth/fixtures/test_users.json

With the following command we can load these fixtures in a test server
and look at it in the browser::

    $ python manage.py testserver view_tests_data.json test_users.json

For the front-end tests to be discovered they have to be loaded into
:file:`recipes/tests/__init__.py`:

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/__init__.py
    :emphasize-lines: 2

Now you create the file :file:`recipes/tests/view_tests.py` with the
following content:

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/view_tests.py
    :lines: 1-30

To extend the test suite for the front-end you can add the following
code to the ``RecipeViewsTests`` class. The
``RecipeViewsTests.test_add`` test needs an image. Add a random image to
the :file:`recipes/fixtures` directory and change the filename in the
code to match your file name.

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/view_tests.py
    :lines: 32-

The front-end tests can be called explicitly with this command::

    $ python manage.py test recipes.RecipeViewsTests

Further links to the Django documentation
=========================================

- :djangodocs:`Testing in Django <topics/testing/>`
