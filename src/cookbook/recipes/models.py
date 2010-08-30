import datetime

from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(u'Name', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(u'Beschreibung', blank=True)

    class Meta:
        verbose_name = u'Kategorie'
        verbose_name_plural = u'Kategorien'

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    DIFFICULTIES = (
        (DIFFICULTY_EASY, u'einfach'),
        (DIFFICULTY_MEDIUM, u'normal'),
        (DIFFICULTY_HARD, u'schwer'),
    )
    title = models.CharField(u'Titel', max_length=255)
    slug = models.SlugField(unique=True)
    ingredients = models.TextField(u'Zutaten',
        help_text=u'Eine Zutat pro Zeile angeben')
    preparation = models.TextField(u'Zubereitung')
    time_for_preparation = models.IntegerField(u'Zubereitungszeit',
        help_text=u'Zeit in Minuten angeben', blank=True, null=True)
    number_of_portions = models.IntegerField(u'Anzahl der Portionen')
    difficulty = models.SmallIntegerField(u'Schwierigkeitsgrad',
        choices=DIFFICULTIES, default=DIFFICULTY_MEDIUM)
    category = models.ManyToManyField(Category, verbose_name=u'Kategorie')
    author = models.ForeignKey(User, verbose_name=u'Autor')
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    class Meta:
        verbose_name = u'Rezept'
        verbose_name_plural = u'Rezepte'
        ordering = ['-date_created']

    @models.permalink
    def get_absolute_url(self):
        return ('recipes_recipe_detail', (), {'slug': self.slug})

    def __unicode__(self):
        return self.title
    
    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.datetime.now()
        self.date_updated = datetime.datetime.now()
        super(Recipe, self).save(**kwargs)
    
    def get_related_recipes(self):
        categories = self.category.all()
        related_recipes = Recipe.objects.all().filter(
            difficulty__exact=self.difficulty, category__in=categories)
        return related_recipes.exclude(pk=self.id).distinct()
