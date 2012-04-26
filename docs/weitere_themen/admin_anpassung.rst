Anpassung des Admin Backends
****************************

Admin Dokumentation aktivieren
==============================

Der Admin kann auch die Dokumentation der Apps anzeigen. Dies muss aber zuerst
aktiviert werden.

#. Die App ``django.contrib.admindocs`` in den ``INSTALLED_APPS`` aktivieren.
#. Den URL ``(r'^admin/doc/', include('django.contrib.admindocs.urls'))`` in ``cookbook/urls.py`` aktivieren. Dabei darauf achten, dass dieser **vor** dem ``r'^admin/'`` Eintrag steht.
#. Das docutils_ Package installieren::

    $ pip install docutils

Jetzt ist im Admin oben rechts ein neuer Navigationspunkt "Dokumentation" verfügbar.

 .. _docutils: http://docutils.sf.net/

Verhalten des Admin anpassen
============================

Das Verhalten des Admin kann sehr umfangreich angepasst werden. Will man zum
Beispiel, dass Benutzer im Backend nur noch ihre eigenen Rezepte editieren
können wenn sie nicht in der Administratorengruppe sind, kann man dies mit dem
folgendem Code in :file:`recipes/admin.py` erreichen::

    class RecipeAdmin(admin.ModelAdmin):
        def queryset(self, request):
            qs = super(RecipeAdmin, self).queryset(request)
            if request.user.is_superuser:
                return qs
            return qs.filter(author=request.user)

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Dokumentation im Admin aktivieren </ref/contrib/admin/admindocs/>`
* :djangodocs:`Admin site Dokumentation </ref/contrib/admin/>`
