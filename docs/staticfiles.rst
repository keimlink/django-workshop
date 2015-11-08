.. _staticfiles:

***************************
Integration of static files
***************************

It is difficult to create a website without any static files. Static files are all files that need not be processed by the Python interpreter - ie CSS, JavaScript, images, etc.

So far, our project only consists of three templates and some Python files. So we set out to change that. HTML5 Boilerplate and `Bootstrap 3 <http://getbootstrap.com/>`_ will help us to do that.

#. Click at the `Initializr Website <http://www.initializr.com/>`_ on "Bootstrap"
#. In the section "H5BP Optional" check the "404 Page" option
#. Finally click on the button "Download it!"
#. Extract the ZIP archive
#. Copy the file :file:`index.html` into the directory
   :file:`cookbook/templates` and rename it to :file:`base.html`
#. Copy the directories :file:`css`, :file:`img` and :file:`js`
   into the directory :file:`cookbook/static`

.. note::

    To make the download of the HTML5 Boilerplate ZIP archive work your
    browser needs to accept the cookies set by the website.

Now you need to adjust the base template :file:`base.html` so that
Django is able to able to use the right path for the static files.
Therefor you will use the :djangodocs:`static <ref/templates/builtins/#static>`
template tag. Template tags are written this way: ``{% tag %}``. Because
the tag ``static`` is provided by an app it needs to be loaded first.
This is done with the help of the :djangodocs:`load <ref/templates/builtins/#load>`
tag in line 1. Customize all highlighted parts in the head of
:file:`base.html` as shown:

.. literalinclude:: ../src/cookbook_staticfiles/templates/base.html
    :language: html+django
    :lines: 1-26
    :emphasize-lines: 1, 14, 21, 22, 24

Now follow the locations where the ``static`` tag needs to be placed at
the end of the template :file:`base.html`:

.. literalinclude:: ../src/cookbook_staticfiles/templates/base.html
    :language: html+django
    :lines: 76-99
    :emphasize-lines: 2, 4, 6

Now replace the ``title`` HTML tag with the highlighted line:

.. literalinclude:: ../src/cookbook_staticfiles/templates/base.html
    :language: html+django
    :lines: 7-12
    :emphasize-lines: 4

Here, the first (empty) block will be defined with the help of the
:djangodocs:`block <ref/templates/builtins/#block>` tag.

The section overwritten with ``<!-- Main jumbotron for a primary
marketing message or call to action -->`` is deleted and two additional
blocks are added to the following div-container; one for the headline
and the other for the contents of the current page. New lines are
highlighted:

.. literalinclude:: ../src/cookbook_staticfiles/templates/base.html
    :language: html+django
    :lines: 65-78
    :emphasize-lines: 3-8

If you want to you can delete the ``div`` containers overwritten with
``<!-- Example row of columns -->``.

.. _using_request_context:

Using ``RequestContext`` in the views
=====================================

Both views need to be expanded to pass the ``RequestContext`` to the
``render_to_response`` functions.  First, the appropriate import needs
to be added to :file:`recipes/views.py`. Then ``RequestContext`` has to
be passed as ``context_instance`` to the ``render_to_response``
function. Your views should look like this afterwards:

.. literalinclude:: ../src/cookbook_staticfiles/recipes/views.py
    :linenos:
    :emphasize-lines: 2, 9-10, 15-16

Further links to the Django documentation
=========================================

- :djangodocs:`The staticfiles app <ref/contrib/staticfiles/>`
- :djangodocs:`RequestContext documentation <ref/templates/api/#django.template.RequestContext>`
