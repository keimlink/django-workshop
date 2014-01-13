# encoding: utf-8
from django.db import models

from cookbook.basemodels import DateTimeInfo


class Article(DateTimeInfo):
    headline = models.CharField('Headline', max_length=100)
    body = models.TextField('Content')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_updated']

    def __unicode__(self):
        return self.headline
