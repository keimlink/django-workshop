Das ``Recipe`` Model um einen Manager erweitern
***********************************************

Jedes Model hat mindestes einen Manager, nämlich ``objects``. Diesen Default
Manager kann man ersetzen oder man kann weitere Manager schreiben, um bestimmte
Gruppen von Models zu erhalten.

Dazu erstellst du in :file:`recipes/models.py` eine neue Klasse
``ActiveRecipeManager``::

    class ActiveRecipeManager(models.Manager):
        def get_query_set(self):
            return super(ActiveRecipeManager, self).get_query_set().filter(is_active=True)

    class Recipe(models.Model):
        ...
        is_active = models.BooleanField(u'Aktiv')

        objects = models.Manager()
        active = ActiveRecipeManager()

        def get_related_recipes(self):
            categories = self.category.all()
            related_recipes = Recipe.active.filter(
                difficulty__exact=self.difficulty, category__in=categories)
            return related_recipes.exclude(pk=self.id).distinct()

Wichtig ist, dass nicht der Name sondern die Position den Default Manager
bestimmt: Der erste Manager, der definiert wird, ist der Default Manager - egal
wie er heisst.

So kann man den neuen Manager in :file:`recipes/views.py` einsetzen::

    class RecipeListView(ListView):
        template_name = 'recipes/index.html'

        def get_queryset(self):
            recipes = Recipe.active.all()
            logger.debug('Anzahl der Rezepte: %d' % recipes.count())
            return recipes


    class RecipeDetailView(DetailView):
        queryset = Recipe.active.all()
        template_name = 'recipes/detail.html'


Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Manager <topics/db/managers/>`
