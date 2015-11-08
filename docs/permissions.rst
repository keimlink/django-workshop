***********
Permissions
***********

Django comes with a simple permissions system which provides a way to assign
permissions to specific users and groups of users. It’s used by the admin, but
you can also use it in your own code.

The following three permissions are the default permissions created for each
Django model if ``django.contrib.auth`` is in ``INSTALLED_APPS``:

* add: Users with the “add” permission are allowed to add new objects
* change: Users with the “change” permission are allowed to edit existing objects
* delete: Users with the "delete" permission can delete objects

These permissions can be directly assigned to a user. To make the management of
permissions easier Django also provides groups which can be used to categorize
users. All permissions assigned to a group are automatically assigned to all
users which are members of the group. A user can belong to any number of
groups, but a group can't belong to another group.

Working with the permissions using the ORM
==========================================

Let's check out how permissions and groups can be accessed and how permissions
can be tested. First start a Python interactive interpreter by using the
:command:`python manage.py shell` command. Then load the first user which
should be the admin and play with it:

::

    >>> from django.contrib.auth.models import User
    >>> admin = User.objects.first()
    >>> admin
    <User: admin>
    >>> admin.user_permissions.all()
    []
    >>> admin.groups.all()
    []
    >>> admin.has_perm('recipes.add_recipe')
    True
    >>> admin.has_perm('recipes.add_category')
    True
    >>> admin.has_perm('recipes.change_recipe')
    True
    >>> admin.has_perm('recipes.delete_recipe')
    True
    >>> admin.is_superuser
    True

You can notice the following things:

* Every user has a relation ``user_permission`` which contains all related ``Permission`` objects.
* Every user has a relation ``groups`` which contains all related ``Group`` objects.
* The admin user has neither permissions nor groups.
* Every user has a ``has_perm`` method which can be used to check if the user has the required permissions, the permission format is ``"<app label>.<permission codename>"``. If a user is inactive, this method will always return ``False``.
* A user with ``is_superuser`` set to ``True`` has all permissions without explicitly assigning them.

Now perform the following tasks:

#. Create a new user, do not make the user a superuser
#. Create a new group
#. Assign some permissions directly to the user and some to the group
#. Make the user a member of the new group
#. Use the Python interactive interpreter to check the permissions and groups of the new user

Stay in the Python interactive interpreter and continue to work with the new user object:

#. Call the ``User.groups.clear()`` method for the new user to delete all group relations
#. Check if this has an effect on the permissions of the user, you can also call ``User.get_group_permissions()`` to see just the group permissions
#. Reload the user object by calling ``User.objects.get(username=<username>)`` again (or use the command you used to load the user object)
#. Check the permissions again, now the user object should have lost the permissions assigned through the group

.. note::

    Because the permissions on the user object are cached after the first time
    they need to be fetched for a permissions check, you have to reload them
    after you changed them.

Permissions of anonymous users
==============================

User that are not authenticated are a
``django.contrib.auth.models.AnonymousUser`` object. The ``groups`` and
``user_permissions`` for these objects are always empty.

Checking permissions with a view decorator
==========================================

To require a particular permission to call a view the ``permission_required``
decorator can be used:

::

    from django.contrib.auth.decorators import permission_required

    @permission_required('recipes.add_recipe')
    def add(request):
        ...

Instead of a single permission a list of permissions can be passed as first
argument. The decorator takes an optional ``login_url`` parameter which
defaults to ``settings.LOGIN_URL``. If the optional ``raise_exception``
parameter is set to ``True``, the decorator will raise ``PermissionDenied``,
prompting the 403 (HTTP Forbidden) view instead of redirecting to the login
page.

.. note::

    Adding the ``permission_required`` decorator makes using the
    ``login_required`` decorator obsolete.

Using permissions in templates
==============================

The currently logged-in user’s permissions are stored in the template variable
``{{ perms }}``. This is an instance of
``django.contrib.auth.context_processors.PermWrapper``, which is a template-
friendly proxy of permissions.

The ``{{ perms }}`` can be used like this:

..  code-block:: html+django

    {% if perms.recipes %}
        <p>You have permission to do something in the recipes app.</p>
        {% if perms.recipes.add_recipe %}
            <p>You can add a recipe!</p>
        {% endif %}
        {% if perms.recipes.delete_recipe %}
            <p>You can delete a recipe!</p>
        {% endif %}
    {% else %}
        <p>You don't have permission to do anything in the recipes app.</p>
    {% endif %}

It is possible to also look permissions up by ``{% if in %}`` statements:

..  code-block:: html+django

    {% if 'recipes' in perms %}
        {% if 'recipes.add_recipe' in perms %}
            <p>You can add a recipe!</p>
        {% endif %}
    {% endif %}

Adding new permissions to a model
=================================

Extra permissions to enter into the permissions table when creating a model can
be added using ``Meta.permissions``:

::

    class Recipe(models.Model):
        ...

        class Meta:
            permissions = (('can_promote', 'Can promote a recipe'),)

.. note::

    If you add permissions after the model has been created in the database you
    to create a migration for that.

You can also customize the default permissions using ``Meta.default_permissions``:

..  code-block:: python

    class Recipe(models.Model):
        ...

        class Meta:
            default_permissions = (,)

The default is ``('add', 'change', 'delete')``. This example would create a
model with no default permissions. You have to specify it on the model before
it is created by :command:`migrate` in order to prevent any omitted permissions
from being created.

Third party apps for permission management
==========================================

There are several third party apps for permission management. The following two
are actively maintained and provide two different approaches.

* `django-rulez <https://github.com/chrisglass/django-rulez>`_ is a fast rules-based permissions system which also has a role concept and works without additional database queries
* `django-guardian <https://github.com/django-guardian/django-guardian>`_ provides per object permissions which are stored in the database

Further links to the Django documentation
=========================================

* :djangodocs:`Permissions and Authorization <topics/auth/default/#permissions-and-authorization>`
* :djangodocs:`Authorization for anonymous users <topics/auth/customizing/#authorization-for-anonymous-users>`
* :djangodocs:`Limiting access to logged-in users that pass a test <topics/auth/default/#limiting-access-to-logged-in-users-that-pass-a-test>`
* :djangodocs:`Permissions in templates <topics/auth/default/#permissions>`
* :djangodocs:`Model Meta options: permissions <ref/models/options/#permissions>`
