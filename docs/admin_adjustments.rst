*******************
Adjusting the admin
*******************

Enable admin documentation
==========================

The admin can also show the documentation of the apps. This, however,
must first be activated.


#. Activate the app ``django.contrib.admindocs`` in ``INSTALLED_APPS``.
#. Activate the URL ``(r'^admin/doc/', include('django.contrib.admindocs.urls'))`` in ``cookbook/urls.py``. Make sure that it's positioned **before** the URL ``r'^admin/'``!
#. Install the `docutils <http://docutils.sf.net/>`_ package::

    $ pip install docutils

Now a new navigation point "documentation" is available at the top right
of the admin.

Customize behavior of admin
===========================

The behavior of the admin can be adapted extensively. If you want to
make sure that users edit only their own recipes if they are not in the
administrators group, you can do this with the the following code in
:file:`recipes/admin.py`::

    class RecipeAdmin(admin.ModelAdmin):
        def queryset(self, request):
            qs = super(RecipeAdmin, self).queryset(request)
            if request.user.is_superuser:
                return qs
            return qs.filter(author=request.user)

Further links to the Django documentation
=========================================

* :djangodocs:`The Django admin documentation generator </ref/contrib/admin/admindocs/>`
* :djangodocs:`The Django admin site </ref/contrib/admin/>`
