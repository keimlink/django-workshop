import datetime

from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(u'Name', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(u'Beschreibung', blank=True)

    class Meta:
        pass

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
        blank=True, null=True)
    number_of_portions = models.IntegerField(u'Anzahl der Portionen')
    difficulty = models.SmallIntegerField(u'Schwierigkeitsgrad',
        choices=DIFFICULTIES, default=DIFFICULTY_MEDIUM)
    category = models.ManyToManyField(Category, verbose_name=u'Kategorie')
    author = models.ForeignKey(User, verbose_name=u'Autor')
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.date_created = datetime.datetime.now()
        self.date_updated = datetime.datetime.now()
        super(Recipe, self).save(force_insert, force_update)
