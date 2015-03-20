# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Name')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('slug', models.SlugField(unique=True)),
                ('ingredients', models.TextField(help_text=b'One ingredient per line', verbose_name=b'Ingredients')),
                ('preparation', models.TextField(verbose_name=b'Preparation')),
                ('time_for_preparation', models.IntegerField(help_text=b'Time in minutes', null=True, verbose_name=b'Time for preparation', blank=True)),
                ('number_of_portions', models.PositiveIntegerField(verbose_name=b'Number of portions')),
                ('difficulty', models.SmallIntegerField(default=2, verbose_name=b'Difficulty', choices=[(1, b'simple'), (2, b'normal'), (3, b'hard')])),
                ('photo', models.ImageField(upload_to=b'recipes', verbose_name=b'Photo')),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_updated', models.DateTimeField(editable=False)),
                ('author', models.ForeignKey(verbose_name=b'Author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(to='recipes.Category', verbose_name=b'Categories')),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
            bases=(models.Model,),
        ),
    ]
