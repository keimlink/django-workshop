Methoden am Model definieren
****************************

Wenn man komplizierte Operationen mit dem ORM durchführt, definiert man dafür
besser eine Methode am Model. So folgt man dem :ref:`dry`-Prinzip und kann
dadurch den Code an verschiedenen Stellen nutzen.

Eine neue Methode für das Model
===============================

Mit der folgenden neuen Methode kannst du alle Rezepte ermitteln, die mit dem
aktuellen Rezept bestimmte Ähnlichkeiten haben. Als Kriterien wurden hier die
gleiche Schwierigkeit und eine übereinstimmende Kategorie gewählt.

Füge also diese Methode dem Model ``Recipe`` in der Datei
:file:`recipes/models.py` hinzu:

..  code-block:: python

    def get_related_recipes(self):
        categories = self.category.all()
        related_recipes = Recipe.objects.all().filter(
            difficulty__exact=self.difficulty, category__in=categories)
        return related_recipes.exclude(pk=self.id).distinct()

Das Template erweitern
======================

Du kannst die neue Methode sofort im Template
:file:`recipes/templates/recipes/detail.html` einsetzen:

..  code-block:: html+django

    {% if object.get_related_recipes %}
    <h4>Verwandte Rezepte</h4>
    <ul>
    {% for recipe in object.get_related_recipes %}
        <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
    {% endfor %}
    </ul>
    {% endif %}

Mehr Flexibilität mit einem Templatetag
=======================================

Im :ref:`vorhergehenden Kapitel <templatetags>` hast du gelernt, dass man mit
Templatetags wesentlich flexibler und effektiver arbeiten kann. Also benutzen
wir doch die neue Methode am Model, um ein neues Templatetag in
:file:`recipes/templatetags/recipes.py` zu erstellen:

..  code-block:: python

    class GetRelatedRecipesNode(template.Node):
        def __init__(self, recipe, limit, name):
            self.recipe = template.Variable(recipe)
            self.limit = limit
            self.name = name

        def render(self, context):
            try:
                recipe = self.recipe.resolve(context)
                context[self.name] = recipe.get_related_recipes()[:self.limit]
            except template.VariableDoesNotExist:
                pass
            return ''
    
    @register.tag(name='get_related_recipes')
    def do_get_related_recipes(parser, token):
        """Gets the defined number of related recipes.

        ::

            <ul>
            {% get_related_recipes recipe 5 as related_recipes %}
            {% for recipe in related_recipes %}
                <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
            {% endfor %}
            </ul>
        """
        try:
            tag_name, recipe, limit, keyword_as, name = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                '%s takes exactly three arguments' % token.contents.split()[0])
        return GetRelatedRecipesNode(recipe, limit, name)

Nun kannst du den Code im Template mit dem Templatetag ersetzen:

..  code-block:: html+django

    {% get_related_recipes object 5 as related_recipes %}
    {% if related_recipes %}
    <h4>Verwandte Rezepte</h4>
    <ul>
    {% for recipe in related_recipes %}
        <li><a href="{{ recipe.get_absolute_url }}">{{ recipe.title }}</a></li>
    {% endfor %}
    </ul>
    {% endif %}

..  note::

    Durch die Verwendung des Templatetags sparst du auch einen SQL Query.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`QuerySet API Referenz <ref/models/querysets/#ref-models-querysets>`
