***************
Django Workshop
***************

Django Workshop is a free `Django <https://www.djangoproject.com/>`_
tutorial. The latest stable release is hosted at
http://www.django-workshop.de/.

The goal of the tutorial is to help beginners to learn the basics of the
Python Web Application Framework Django. It can also help people with
basic Django experience to improve their skills.

The workshop has been created as material for Django trainings but can
also be used for self-study.

Currently there is only a German version available. An English
translation is in progress.

Creating a Virtual Machine using Vagrant
========================================

The repository contains a configuration for a Virtual Machine. This
configuration will install all necessary software during setup. It's a
`Debian 7.2 <http://www.debian.org/releases/wheezy/>`_ system. The
following packages will be installed using `Salt
<http://www.saltstack.com/community/>`_:

* Sqlite
* tree
* Vim

To setup the Virtual Machine you have to `install Vagrant
<http://docs.vagrantup.com/v2/installation/index.html>`_ at first. Then
simply start the Virtual Machine using::

    $ vagrant up

Now you can connect to the Virtual Machine using Vagrant`s ``ssh`` command::

    $ vagrant ssh

.. TODO Add MySQL and PostgreSQL to the Salt setup
.. After that you can connect to the MySQL and PostgreSQL. Use the password
.. "django" to authenticate::

..     $ mysql -p -u root
..     $ psql -h localhost -U postgres

Contributions and Bugs
======================

Feel free to improve Django Workshop or create translations. `Pull
requests are welcome! <https://github.com/keimlink/django-workshop>`_

Please report problems to our `issue tracker
<https://github.com/keimlink/django-workshop/issues>`_.

Documentation License
=====================

This work is licensed under the Creative Commons Attribution-ShareAlike
3.0 Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
Creative Commons, 444 Castro Street, Suite 900, Mountain View,
California, 94041, USA.


Source Code License
===================

Copyright (c) 2010-2012, Markus Zapke-Gründemann
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.
    * Neither the names of the authors nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

