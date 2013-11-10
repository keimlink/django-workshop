***********
Preparation
***********

We'll use Django Version |djangoversion|. To get started we need to do
a little preparation.

.. index:: Install Python

Python
======

Django is written completely in `Python <http://python.org/>`_.
Therefore Python needs to be installed first.

.. note::

    Django |djangoversion| supports Python from version 2.6.5. It's
    recommended to use Python version 2.7.3 or higher. If you have an
    older version of Python, you should update it.

    Since version 1.5, Django has experimental support for Python 3.2
    and later. Django 1.6. will have stable support for Python 3.

You can find out which version of Python you're running by using the
command line option :option:`-V`:

.. command-output:: python -V

.. note::

    If you are using Python 3 please make sure you have Python 3.3.2 or
    greater installed. Otherwise there will be problems.

    Also consider adding the following future-import on top of every
    Python file you are going to edit to ensure Python 2 and 3
    compatibility::

        from __future__ import unicode_literals

    This way all regular strings will be unicode string literals.

    If you want to learn more read the :djangodocs:`Python 3
    <topics/python3/>` part of the Django documentation.

If you've already got the right version of Python installed, you can
skip ahead to :ref:`Python Package Managers <python-package-manager>`.

Linux
-----

Many Linux distributions come with Python already installed. If you
haven't got a version of Python installed, you can normally use your
package manager to download and install it.

Alternatively, you can get the `Python Sources
<http://python.org/download/>`_ from the website and compile it
yourself.

Mac OS X
--------

Python comes pre-installed on Mac OS X. You can however use `Homebrew
<http://brew.sh/>`_ to install your own copy of Python.

Windows
-------

Download the `Installer <http://python.org/download/>`_ from the Python
Website and install it.

So that Python works under Windows as expected, you need to change the
environment variable :envvar:`%PATH%`. In the examples, we'll assume
that your Python is installed in :file:`C:\\Python27\\`.

Windows 7
^^^^^^^^^

#. :menuselection:`Start`, then right click on :menuselection:`Computer`
#. Now click the context menu option :guilabel:`Properties`
#. Next, in the window that just opened, click on the
   :guilabel:`Advanced System Settings`
#. A further window will open, click the
   :guilabel:`Environment Variables`
#. Under `System Variables`, select the :option:`PATH`
#. Now click on :guilabel:`Edit` and add the required directory:
   ``;C:\Python27\;C:\Python27\Scripts;``. (The semi-colon at the
   beginning is required!)
#. Now close the windows :guilabel:`Environment Variables` and
   :guilabel:`System Properties` by clicking on `OK`.

Windows XP
^^^^^^^^^^

#. :menuselection:`Start --> Control Panel --> System --> Advanced`
#. Click on the :guilabel:`Environment Variables`, then a new window
   will open. Under "System Variables" select :option:`Path`
#. Now click on :guilabel:`Edit` and add the required directory:
   ``;C:\Python27\;C:\Python27\Scripts;``. (The semi-colon at the
   beginning is required!)
#. Now close the windows :guilabel:`Environment Variables` and
   :guilabel:`System Properties` by clicking on `OK`.

.. index:: Install Python Package Manager
.. _python-package-manager:

Python Package Manager
======================

Python uses its own `package system <https://pypi.python.org/pypi>`_ to
manage distribution and installation of Python packages. Because we will
need to install several packages, we must first install the package
manager.

.. index:: setuptools

setuptools
----------

First `setuptools <http://pythonhosted.org/setuptools/>`_ needs to be
installed. Some systems install it by default, this can be verfied by
executing::

    $ python -c "import setuptools"

If the execution results in an ``ImportError`` setuptools is not
installed and you have to follow the commands below. Otherwise continue
with the installation of :ref:`install-pip`.

It's installed with the help of a bootstrap script which can be
downloaded `here <https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py>`_.
If installed, you can use :program:`curl` to download it at the command
line. Otherwise just use the browser.

::

    $ curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py

When the bootstrap script has been downloaded execute it to install
:program:`setuptools`::

    $ python ez_setup.py

.. note:: Under Linux and Mac OS X root privileges may be required.

You can delete the bootstrap script when the installation has been finished.

.. index:: pip
.. _install-pip:

pip
---

We will use `pip <http://www.pip-installer.org/>`_ to install the
packages. :program:`pip` was originally written as `an improvement
<http://www.pip-installer.org/en/latest/other-tools.html#easy-install>`_
of :program:`easy_install`. :program:`pip` can be installed with the
help from a bootstrap script which can be downloaded from
`GitHub <https://raw.github.com/pypa/pip/master/contrib/get-pip.py>`_.
If installed, you can use :program:`curl` to download it at the command
line. Otherwise just use the browser.

::

    $ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py

When the bootstrap script has been downloaded execute it to install
:program:`pip`::

    $ python get-pip.py

.. note:: Under Linux and Mac OS X root privileges may be required.

You can delete the bootstrap script when the installation has been finished.

After installation, you can test :program:`pip` as follows:

.. command-output:: pip --version

.. index:: virtualenv, virtualenvwrapper, virtualenvwrapper-win

virtualenv and virtualenvwrapper
================================

What is a virtualenv?
---------------------

As soon as you work with more than one project you will sooner or later
have collisions between Python packages. Maybe an old project still
needs an older version of a package while you want to use the latest
version for your new project. This is where `virtualenv
<http://www.virtualenv.org/>`_ can help.

:program:`virtualenv` provides a "container" for each of your projects.
Each virtualenv can be separated from the system Python installation and
from other virtualens. Furthermore each virtualenv can be associated to
a different Python version. Finally virtualens can be used in production
to separate different projects on a single host.

Installation
------------

Install :program:`virtualenv` using :program:`pip`::

    $ pip install virtualenv

.. note:: Under Linux and Mac OS X root privileges may be required.

After the installation create a directory where you will create all your
virtualenvs, for example in your home directory::

    $ mkdir .virtualenvs

.. note:: If you are using Windows use :file:`Envs` instead of :file:`.virtualens`.

Working easier and faster with virtualenvwrapper
------------------------------------------------

`virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
makes the creation and every day work with virtualenvs much easier by
providing a lot of additional helpers.

Linux and Mac OS X
^^^^^^^^^^^^^^^^^^

Install :program:`virtualenvwrapper` using :program:`pip`::

    $ pip install virtualenvwrapper

.. note:: Under Linux and Mac OS X root privileges may be required.

After the installation add the following two lines to your
:file:`.bashrc` or :file:`.profile`:

..  code-block:: bash

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

``WORKON_HOME`` defines where all virtualenvs are located. The script
:program:`virtualenvwrapper.sh` loads the helpers.

Reload your shell configuration to be able to use :program:`virtualenvwrapper`::

    $ source .bashrc

Windows
^^^^^^^

Windows users can install `virtualenvwrapper-win
<https://pypi.python.org/pypi/virtualenvwrapper-win>`_ instead of
:program:`virtualenvwrapper`::

    $ pip install virtualenvwrapper-win

.. note::

    :program:`virtualenvwrapper-win` does not work with PowerShell, use
    the Command Prompt (:program:`cmd.exe`) instead.
