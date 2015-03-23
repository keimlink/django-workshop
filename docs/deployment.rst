**********
Deployment
**********

Django’s primary deployment platform is `WSGI <http://www.wsgi.org/>`_, which
stands for Web Server Gateway Interface. It's a specification that describes
how a web server communicates with web applications, and how web applications
can be chained together to process a single request. WSGI is a Python standard
described in detail in :pep:`3333`.

The ``startproject`` management command has created a
simple default WSGI configuration for you, which you can direct to any
WSGI-compliant application server to use.

Some of the most popular WSGI servers are:

* `Gunicorn <http://gunicorn.org/>`_ - A Python WSGI HTTP Server for UNIX
* `modwsgi <https://github.com/GrahamDumpleton/mod_wsgi>`_ - A Python WSGI adapter module for Apache
* `uWSGI <http://projects.unbit.it/uwsgi/>`_ - A full stack for building hosting services, including a WSGI plugin

We will use the following technologies to deploy our project:

* `uWSGI <http://projects.unbit.it/uwsgi/>`_
* `nginx <http://nginx.org/>`_
* `PostgreSQL <http://postgresql.org/>`_

We will use `Vagrant <http://vagrantup.com>`_ and
`VirtualBox <www.virtualbox.org>`_ to simulate a `Debian <http://debian.org/>`_
server. All required services will be installed and configured using
`SaltStack <http://saltstack.com/>`_.

.. todo::

    Explain how to use Sentry, maybe using a local installation.
    https://getsentry.com/
    https://github.com/getsentry/sentry

Further links to the Django documentation
=========================================

* :djangodocs:`How to deploy with WSGI <howto/deployment/wsgi/>`
* :djangodocs:`Deploying static files <howto/static-files/deployment/>`
* :djangodocs:`Deployment checklist <howto/deployment/checklist/>`
* :djangodocs:`Error reporting <howto/error-reporting/>`
