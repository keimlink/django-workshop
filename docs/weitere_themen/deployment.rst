Deployment
**********

Für das Deployment stehen verschiedene Optionen zur Verfügung:

- :djangodocs:`WSGI <howto/deployment/wsgi/>`
    - :djangodocs:`Apache mit mod_wsgi <howto/deployment/wsgi/modwsgi/>`
    - :djangodocs:`Gunicorn <howto/deployment/wsgi/gunicorn/>`
- :djangodocs:`FastCGI, SCGI, oder AJP <howto/deployment/fastcgi/>`

Gunicorn
========

Gunicorn_ ist sehr einfach zu benutzen::

    $ pip install gunicorn

Dann "gunicorn" in die ``INSTALLED_APPS`` eintragen. Jetzt kann man den Server
mit folgendem Kommando starten::

    $ python manage.py run_gunicorn

Es gibt die Möglichkeit Gunicorn genauer zu `konfigurieren
<http://gunicorn.org/configure.html>`_.

Außerdem stehen `verschiedene Konfigurationen
<http://gunicorn.org/deploy.html>`_ zur Verfügung um Gunicorn zum Beispiel mit
Nginx_ und Supervisor_ zu betreiben.

Sowohl mod_wsgi als auch Gunicorn lassen sich gut mit einem Virtualenv
betreiben.

..  _Gunicorn: http://gunicorn.org/
..  _Nginx: http://www.nginx.org/
..  _Supervisor: http://supervisord.org/
