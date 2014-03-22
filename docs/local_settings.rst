*********************
A local configuration
*********************

Some settings in the configuration file :file:`settings.py` are only
useful for development. For example, ``DEBUG`` should have the value
``True`` during development, but on the production system the value
``False``.

To leave the configuration unchanged for the production system, the
following procedure is useful.

The following code is added at the end of the file :file:`settings.py`:

.. literalinclude:: ../src/cookbook_improved/cookbook/settings.py
    :lines: 166-169

This code loads all the settings from the file :file:`local_settings.py`
if it exists. If this file does not exist, nothing happens. So you can
define in the file :file:`local_settings.py` certain values and
overwrite the values defined in :file:`settings.py`.

So upgrade your :file:`settings.py` file at the end as stated above.

Now you put in the same directory in which the file
:file:`settings.py` is the file :file:`local_settings.py` with
the following content (you can copy from :file:`settings.py`):

.. literalinclude:: ../src/cookbook_improved/cookbook/local_settings.py

After that you adjust the following values in :file:`settings.py`:

.. literalinclude:: ../src/cookbook_improved/cookbook/settings.py
    :lines: 6-8, 15-25

.. note::

    Of course you can also enter the data for the production system in
    the database configuration (except the password!).

As long as the file :file:`local_settings.py` is available, you work
with a configuration for development. If this file is missing, you use
the settings from :file:`settings.py`, which are optimized for
production.

Of course you can divide a configuration even more with this approach
and thus use quite different scenarios, for example a
development/staging/production setup. A Django app that makes this
easier is `django-configurations <https://github.com/jezdez/django-configurations>`_.
