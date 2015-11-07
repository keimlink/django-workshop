*************************
Functional and Unit Tests
*************************

Django supports two different test approaches: Doctests and unit tests. We will
look at the advantages and disadvantages of both in this chapter.

Doctests
========

`Doctests <http://docs.python.org/library/doctest.html>`_ are supported by
Django, but they are :djangodocs:`not automatically discovered <releases/1.6/#new-test-runner>`.
In addition the disadvantages outweigh the advantages when you want to write
doctests for Django.

Advantages
----------

* Easy to create
* Augment the code documentation
* Tests are where the source code is

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

Django uses the Python standard library module
`unittest <http://docs.python.org/library/unittest.html>`_ for
`unit tests <https://en.wikipedia.org/wiki/Unit_testing>`_.

Before we can write the first tests we have to install an additional package:

::

    $ pip install freezegun

The file :file:`recipes/tests.py` currently contains only an import of the ``TestCase`` base class:

.. literalinclude:: ../src/cookbook/recipes/tests.py

It extends ``unittest.TestCase`` and provides additional functionality:

* Automatic :djangodocs:`loading of fixtures <topics/testing/tools/#fixture-loading>`
* Wraps each test in a :djangodocs:`transaction <topics/testing/tools/#transactiontestcase>`
* Creates a :djangodocs:`TestClient <topics/testing/tools/#the-test-client>` instance
* :djangodocs:`Django-specific assertions <topics/testing/tools/#assertions>` for testing for things like redirection and form errors

Add the following code:

.. literalinclude:: ../src/cookbook_tests/recipes/tests.py

And run the tests:

.. command-output:: python manage.py test recipes
    :cwd: ../src/cookbook_tests

Unit tests have much more advantages than disadvantages:

Advantages
----------

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

Different ways of running the tests
===================================

To get a more detailed output use the :option:`-v2` option:

.. command-output:: python manage.py test recipes -v2
    :cwd: ../src/cookbook_tests

Use the :option:`-v0` option to hide most of the output, passing no arguments
to the ``test`` command executes all tests:

.. command-output:: python manage.py test -v0
    :cwd: ../src/cookbook_tests

You can also run the tests just for a single test case:

.. command-output:: python manage.py test recipes.tests.RecipeSaveTests
    :cwd: ../src/cookbook_tests

And even for a single test method:

.. command-output:: python manage.py test recipes.tests.RecipeSaveTests.test_slug_is_unique
    :cwd: ../src/cookbook_tests

You can also provide a path to a directory to discover tests below that directory:

.. command-output:: python manage.py test recipes/
    :cwd: ../src/cookbook_tests

You can specify a custom filename pattern match using the :option:`-p` (or :option:`--pattern`)
option, if your test files are named differently from the :file:`test*.py` pattern:

::

    $ ./manage.py test --pattern="tests_*.py"

Determining test coverage
=========================

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

.. command-output:: coverage report
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
rename it to :file:`test_models.py`::

    $ mv tests.py tests/test_models.py

Next, you delete also the bytecode file :file:`tests.py` so this does
not prevent the execution of the code in the :file:`tests` package::

    $ rm tests.pyc

Finally run the tests:

.. command-output:: python manage.py test recipes.tests.test_models
    :cwd: ../src/cookbook_tests_pkg

Functional tests (testing views)
================================

With the built-in Django test client an easy test browser is at your
disposal.

First we need some fixtures so that data in the front end is available
for testing.

Create a directory :file:`fixtures` in the directory :file:`recipes`:

::

    $ mkdir recipes/fixtures

Then you create a JSON file with the models of the recipes application::

    $ python manage.py dumpdata recipes --indent 4 --natural > recipes/fixtures/test_views_data.json

Now you create the file :file:`recipes/tests/test_views.py` with the
following content:

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/test_views.py
    :lines: 1-37

To extend the test suite for the front-end you can add the following
code to the ``RecipeViewsTests`` class. The
``RecipeViewsTests.test_add`` test needs an image. Add a random image to
the :file:`recipes/fixtures` directory and change the filename in the
code to match your file name.

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/test_views.py
    :lines: 39-

The front-end tests can be called explicitly with this command:

.. command-output:: python manage.py test recipes.tests.test_views
    :cwd: ../src/cookbook_tests_pkg

If you create now another coverage report you can see that the coverage for the views has increased:

.. command-output:: coverage run manage.py test recipes
    :cwd: ../src/cookbook_tests_pkg

Display the coverage data with this command in the shell:

.. command-output:: coverage report
    :cwd: ../src/cookbook_tests_pkg

Further links to the Django documentation
=========================================

* :djangodocs:`Testing in Django <topics/testing/>`
