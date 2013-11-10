# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Category(models.Model):
    """Category model."""
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('Description', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model."""
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    DIFFICULTIES = (
        (DIFFICULTY_EASY, 'simple'),
        (DIFFICULTY_MEDIUM, 'normal'),
        (DIFFICULTY_HARD, 'hard'),
    )
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField(unique=True)
    ingredients = models.TextField('Ingredients',
        help_text='One ingredient per line')
    preparation = models.TextField('Preparation')
    time_for_preparation = models.IntegerField('Time for preparation',
        help_text='Time in minutes', blank=True, null=True)
    number_of_portions = models.PositiveIntegerField('Number of portions')
    difficulty = models.SmallIntegerField('Difficulty',
        choices=DIFFICULTIES, default=DIFFICULTY_MEDIUM)
    category = models.ManyToManyField(Category, verbose_name='Categories')
    author = models.ForeignKey(User, verbose_name='Author')
    photo = models.ImageField(upload_to='recipes', verbose_name='Photo')
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Recipe, self).save(*args, **kwargs)
