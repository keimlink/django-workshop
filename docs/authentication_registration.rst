*******************************
Authentication and Registration
*******************************

For various reasons authentication in the front end makes sense. For example
users should be able to create their own content.

Django provides in ``django.contrib.auth`` an application for
authentication. This is, for example, used in the admin.

Create another application
==========================

To extend ``django.contrib.auth`` we create at first a separate application
called ``userauth``:

::

    $ python manage.py startapp userauth

Configure the project
=====================

Now you need to configure the project so that your new application is used. For
this you expand the file first :file:`settings.py`:

::

    INSTALLED_APPS = (
        ...
        'userauth',
    )

    LOGIN_URL = 'userauth_login'
    LOGOUT_URL = 'userauth_logout'
    LOGIN_REDIRECT_URL = 'recipes_recipe_index'

The three new configuration values have the following tasks:

:``LOGIN_URL``:
    This URL is invoked when a login is required.
:``LOGOUT_URL``:
    The opposite of ``LOGIN_URL``.
:``LOGIN_REDIRECT_URL``:
    If no URL to redirect to is specified after a successful login this URL
    will be used for redirection.

In addition, we may already include the URLs that we will create later for our
new application. For this you expand the project's URLconf :file:`urls.py` with
the following line:

::

    url(r'^user/', include('userauth.urls')),

Authentication with the application ``user auth``
=================================================

Create URLconf
--------------

Now we create the file :file:`urls.py` in directory :file:`userauth`:

::

    from django.conf.urls import include, url
    from django.core.urlresolvers import reverse_lazy


    urlpatterns = [
        url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'userauth/login.html'}, name='userauth_login'),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {
                'next_page': reverse_lazy('recipes_recipe_index'),
            },
            name='userauth_logout'),
        url(r'^password-change/$', 'django.contrib.auth.views.password_change',
            {'template_name': 'userauth/password_change_form.html'},
            name='userauth_password_change'),
        url(r'^passwor-change-done/$', 'django.contrib.auth.views.password_change_done',
            {'template_name': 'userauth/password_change_done.html'},
            name='userauth_password_change_done'),
    ]

It contains the URLs for login and logout as well as changing the password. The
views are used from ``django.contrib.auth.views``, but will be rendered with
their own templates.


.. _toggle_login:

Creating templates
------------------

For the forms we are using the Django app `django-crispy-forms
<http://django-crispy-forms.readthedocs.org/en/latest/>`_. It
can easily be installed using :program:`pip`:

::

    $ pip install django-crispy-forms

We also need to add ``crispy forms`` to the ``INSTALLED_APPS`` and configure it
to use the Bootstrap 3 template pack:

::

    INSTALLED_APPS = (
        ...
        'userauth',
        'crispy_forms',
    )

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

Next, we'll create a template for the login in
:file:`userauth/templates/userauth/login.html`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% load crispy_forms_tags %}

    {% block title %}{{ block.super }} - Login{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
        <form action="{% url 'userauth_login' %}" method="post" accept-charset="utf-8">
            {{ form|crispy }}
            {% csrf_token %}
            <input type="hidden" name="next" value="{{ next }}" />
            <input type="submit" value="Login"/>
        </form>
    {% endblock %}

The new thing in the template is the form. For forms in Django the ``<form>``
tags and the button to submit it must be defined manually.

The view ``django.contrib.auth.views.login`` provides a form as variable
``form``. In addition the token to protect against a `Cross-Site Request
Forgery (CRSF) <https://en.wikipedia.org/wiki/Cross-site_request_forgery>`_
attack must be added manually.

The hidden field ``next`` can be used to specify an URL that is called after a
successful login.

The second template :file:`password_change_form.html` is used to change the
password. Create it also in the directory :file:`userauth/templates/userauth/`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% load crispy_forms_tags %}

    {% block title %}{{ block.super }} - Change password{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <form action="{% url 'userauth_password_change' %}" method="post" accept-charset="utf-8">
        {{ form|crispy }}
        {% csrf_token %}
        <input type="submit" value="Change password"/>
    </form>
    {% endblock %}

The third template is displayed after successfully changing the password. As
defined in the URLconf it's name is :file:`password_change_done.html`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Password successfully changed{% endblock %}

    {% block content %}
    <p>Your password has been changed successfully.</p>
    {% endblock %}

Also, let's create a template to display login or logout anywhere. This
template you create in :file:`userauth/templates/userauth/toggle_login.html`:

..  code-block:: html+django

    {% if user.is_authenticated %}
    <ul class="nav pull-right">
        <li class="dropdown">
            <a class="dropdown-toggle" id="dropuser" data-toggle="dropdown" href="#">
                {{ user.username }}</a>
            <ul class="dropdown-menu" role="menu" aria-labelledby="dropuser">
                <li><a href="{% url "userauth_password_change" %}">Change password</a></li>
                <li><a href="{% url "userauth_logout" %}">Logout</a></li>
            </ul>
        </li>
    </ul>
    {% else %}
    <form class="navbar-form pull-right" action="{% url "userauth_login" %}" method="post"
        accept-charset="utf-8">
        <input class="span2" type="text" placeholder="Username" name="username">
        <input class="span2" type="password" placeholder="Password" name="password">
        {% csrf_token %}
        <button type="submit" class="btn">Login</button>
    </form>
    {% endif %}

Broaden the base template
-------------------------

The template :file:`cookbook/templates/base.html` originally contains the
following login form in the navigation:

.. code-block:: html

    <form class="navbar-form pull-right">
        <input class="span2" type="text" placeholder="Email">
        <input class="span2" type="password" placeholder="Password">
        <button type="submit" class="btn">Sign in</button>
    </form>

Replace the form with a block, in which you're using the ``include`` tag to
load the template :file:`userauth/templates/userauth/toggle_login.html` you
just created:

..  code-block:: html+django

    {% block toggle_login %}
        {% include "userauth/toggle_login.html" %}
    {% endblock %}

``RequestContext`` also necessary here
--------------------------------------

Thus the context of the response object also has the necessary information
available such as the user object or the ``csrf_token``, ``RequestContext``
must be passed to the rendering function. This is what we have already done in
the :ref:`static files chapter <using_request_context>`. So there is nothing to
do here.

Test the authentication
=======================

That was the first part. Now you should be able to use the authentication in
the frontend. Test it!

Registration with the application ``user auth``
===============================================

Of course should the visitors be able to register themselves in the frontend.
Therefore, we now add a form to register.

Expand URLconf
--------------

First, the URLconf in :file:`userauth/urls.py` needs to be extended with two
URLs:

::

    from django.views.generic import TemplateView

    urlpatterns = [
        # ...
        url(r'^register/$', 'userauth.views.register',
            {'next_page_name': 'userauth_register_done'},
            name='userauth_register'),
        url(r'^welcome/$',
            TemplateView.as_view(template_name='userauth/register_done.html'),
            name='userauth_register_done'),
    ]

The second URL ``userauth_register_done`` uses the generic view
``django.views.generic.TemplateView``
(:djangodocs:`Documentation <topics/class-based-views/#simple-usage-in-your-urlconf>`)
because here we simply want to render only the template without further data.

A view of the form
------------------

Now the view for the first URL ``userauth_register`` must be written. For this
you open the file :file:`userauth/views.py` and create the following function:

::

    from django.contrib.auth.forms import UserCreationForm
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response
    from django.template import RequestContext


    def register(request, template_name='userauth/register.html', next_page_name='/'):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(next_page_name))
        else:
            form = UserCreationForm()
        return render_to_response(template_name, {'form': form},
            context_instance=RequestContext(request))

``django.contrib.auth.forms`` provides the form ``UserCreationForm`` that we
use to create a new user. The view just manages the processing of the data. The
argument ``next_page_name`` offers the possibility to forward to any page after
the registration of the user is completed.

Creating and expanding Templates
--------------------------------

Of course, both URLs still need a template. First you create a template for the
form in :file:`userauth/templates/userauth/register.html`:

..  code-block:: html+django

    {% extends "base.html" %}

    {% load crispy_forms_tags %}

    {% block title %}{{ block.super }} - Register{% endblock %}

    {% block toggle_login %}{% endblock %}

    {% block content %}
    <form action="{% url 'userauth_register' %}" method="post" accept-charset="utf-8">
        {{ form|crispy }}
        {% csrf_token %}
        <input type="submit" value="Register"/>
    </form>
    {% endblock %}

Since we want to display no login on the registration page we simply overwrite
the block ``toggle_login`` with an empty block.

In addition we need a template that is displayed after a user has successfully
registered (:file:`register_done.html`):

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - Registration successful{% endblock %}

    {% block content %}
    <p>You have registered successfully. Have fun with the cookbook!</p>
    {% endblock %}

Thus there is a link to the registration form we add a line with the link to it
in the template :file:`toggle_login.html`:

..  code-block:: html+django

    {% if user.is_authenticated %}
        ...
    {% else %}
        <p><a href="{% url 'userauth_login' %}">Login</a>
        <a href="{% url 'userauth_register' %}">Register</a></p>
    {% endif %}

Test registration
-----------------

Now you can test the registration in the front end.

Django apps for authentication and registration
===============================================

Of course there are reusable open source Django apps that provide solutions for
authentication and registration. The best known and probably most widely used
one is `django-registration <https://bitbucket.org/ubernostrum/django-
registration/wiki/Home>`_. Another reusable app is `django-allauth
<http://www.intenct.nl/projects /django-allauth/>`_ that allows both, local and
social authentication (using OAuth).

Further links to the Django documentation
=========================================

* :djangodocs:`User authentication in Django <topics/auth/>`
