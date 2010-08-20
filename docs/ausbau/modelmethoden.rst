Methoden am Model definieren
****************************

Eine neue Methode für das Model
===============================

..  code-block:: python

    def get_related_recipes(self):
        categories = self.category.all()
        related_recipes = Recipe.objects.all().filter(
            difficulty__exact=self.difficulty, category__in=categories)
        return related_recipes.exclude(pk=self.id).distinct()

Das Template erweitern
======================

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
            raise template.TemplateSyntaxError('%s takes exactly three arguments' % token.contents.split()[0])
        return GetRelatedRecipesNode(recipe, limit, name)

Weiterführende Links zur Django Dokumentation
=============================================

* `QuerySet API Referenz <http://docs.djangoproject.com/en/1.2/ref/models/querysets/#ref-models-querysets>`_
