************
Introduction
************

What is Django?
===============

`Django <http://www.djangoproject.com/>`_ is a **Full Stack Framework**
written in `Python <http://python.org/>`_ that focuses on quick
development of **web applications** and clean, pragmatic design. It was
named after the French guitarist and composer `Jean „Django“ Reinhardt
<http://en.wikipedia.org/wiki/Django_Reinhardt>`_ who is known as one of
the greatest guitar players of all time and is the first important
European jazz musician who made major contributions to the development
of the idiom.

Django`s source code and it's `comprehensive documentation
<http://docs.djangoproject.com/>`_ are licensed under the **BSD-
license**. The `Django Software Foundation
<http://www.djangoproject.com/foundation/>`_ takes care of the further
development of Django.

.. index:: Rapid Development

Rapid Development
=================

Django's architecture and tools support a **rapid development** of
websites and new components.

.. index:: Loose Coupling

Loose Coupling
==============

**Loose coupling** means that the components have little or no knowledge
of the definitions of other separate components. This enhances the code
quality and makes it more reusable.

.. index:: Don't Repeat Yourself, DRY
..  _dry:

Don't Repeat Yourself
=====================

The **Don't Repeat Yourself (DRY)** principle is defined as follows:

    *Every piece of knowledge must have a single, unambiguous, authoritative
    representation within a system.*

    -- http://c2.com/cgi/wiki?DontRepeatYourself

**DRY** is one prerequisite for **Loose Coupling** because components
can only be separated from each other if their purpose is clear.

Additionally it makes the day-to-day work easier if the code is not
spread over different parts of the application but can be found where it
would be expected.

.. index:: Model-Template-View, MTV

Model-Template-View
===================

Django is built on the **Model-template-view (MTV)** pattern. **MTV** is
based on the well known `Model-view-controller pattern
<https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ (MVC).

Django includes an **Object-relational mapper** (ORM) which creates
database structures using the **models** and performs all database
operations. It can operate with all major databases. All models are
written in Python.

The **template engine** supports the inheritance pattern and has a
extensive and extendable library of tags and filters.

The **view** fetches the data, for example using the Object-relational
mapper. But it is also possible to use diefferent data sources like web
services, key-value stores or even text files. This data is passed as
**context** to the template.

The **URLconf** controls the routing. The request is passed to the right
view with the of regular expressions.

The **middleware** takes an important position: It can intercept the
processing of the request at different positions. This is used for
session management or caching.

..  _request_response_graph:

..  digraph:: request_response

    label = "Illustration: Schematic Diagram of Django's Request/Response Processing"
    "Browser":w -> "Web server":w [label="HTTP request"];
    {rank=min; "Browser"}
    "Web server":sw -> "URLconf" [label="process_request\n(middleware)"];
    "URLconf" -> "View" [label="process_view\n(middleware)"];
    "View" -> "Model (ORM)" -> "Datenbase"-> "Model (ORM)" -> "View";
    "View" -> "Template" [label="context"];
    "Template" -> "Tags & Filters" -> "Template"
    "Template":ne -> "View":e;
    "View" -> "Web server":e [label="process_template_response\nprocess_response\n(middleware)"];
    "Web server":e -> "Browser":e [label="HTTP response"];

Built-in Development Web Server
===============================

Django comes with a built-in **development web server**. This simplifies
the setup of the development environment because no "real" web server
needs to be installed.

The Admin
=========

Django contains the **Admin**, a `CRUD
<https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_
application which can be created with minimal effort by using the models
