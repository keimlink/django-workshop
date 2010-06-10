Methoden am Model definieren
****************************

..  code-block:: python

    def get_related_recipes(self):
        categories = self.category.all()
        related_recipes = Recipe.objects.all().filter(
            difficulty__exact=self.difficulty, category__in=categories)
        return related_recipes.exclude(pk=self.id).distinct()

..  code-block:: html+django

    {% if object.get_related_recipes %}
    <h4>Verwandte Rezepte</h4>
    <ul>
    {% for recipe in object.get_related_recipes %}
        <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
    {% endfor %}
    </ul>
    {% endif %}

Weiterführende Links zur Django Dokumentation
=============================================

* `QuerySet API Referenz <http://docs.djangoproject.com/en/1.2/ref/models/querysets/#ref-models-querysets>`_
