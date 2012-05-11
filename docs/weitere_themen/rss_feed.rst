Ein RSS Feed für die "News" App
*******************************

Die im Kapitel :ref:`mehrere_datenbanken` erstellte App "news" hat noch kein
Frontend und soll deshalb einen RSS Feed bekommen.

Den Feed erstellen
==================

Dazu legst du zuerst die Datei :file:`news/feeds.py` an::

    from django.contrib.syndication.views import Feed

    from news.models import Article


    class ArticleFeed(Feed):
        title = 'Neuigkeiten aus dem Kochbuch'
        link = '/'
        description = 'Der RSS Feed der Kochbuch Website'

        def items(self):
            return Article.objects.order_by('-date_created')[:5]

        def item_title(self, item):
            return item.headline

        def item_description(self, item):
            return item.body

Die URLs für den Feed definieren
================================

Dann erstellst du die ``URLConf`` in :file:`news/urls.py`::

    from django.conf.urls import patterns, include, url

    from news.feeds import ArticleFeed
    from news.views import ArticleDetailView, ArticleListView


    urlpatterns = patterns('',
        url(r'^feed/rss/$', ArticleFeed(), name='news_article_feed'),
        url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='news_article_detail'),
        url(r'^$', ArticleListView.as_view(), name='news_article_list'),
    )

Und bindest diese danach in der ``URLConf`` in :file:`cookbook/urls.py` ein::

    urlpatterns = patterns('',
        ...
        url(r'^news/', include('news.urls')),
        url(r'^', include('recipes.urls')),
    )

Außerdem musst du das ``News`` Model in :file:`news/models.py` noch mit einer
``get_absolute_url`` Methode ausstatten::

    @models.permalink
    def get_absolute_url(self):
        return ('news_article_detail', (), {'pk': self.pk})

Die Views schreiben
===================

Jetzt die (sehr einfachen) Views für den Feed in :file:`news/views.py` erstellen::

    from django.views.generic import DetailView, ListView

    from news.models import Article


    class ArticleDetailView(DetailView):
        model = Article


    class ArticleListView(ListView):
        model = Article

Die Templates erstellen
=======================

Und am Ende die Templates anlegen.

Das Template :file:`templates/base.html` um den Eintrag für den Feed erweitern::

    <head>
        <title>{% block title %}Kochbuch{% endblock %}</title>
        <link rel="alternate" type="application/rss+xml"
            title="Neuigkeiten aus dem Kochbuch" href="{% url news_article_feed %}" />
    </head>

Das Template für die Liste der Feed Elemente
:file:`news/templates/news/article_list.html` anlegen::

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - News{% endblock %}

    {% block content %}
    <ul>
    {% for article in article_list %}
        <li>
            <h4><a href="{{ article.get_absolute_url }}">{{ article.headline }}</a></h4>
            <p>{{ article.date_updated }}</p>
            <p>{{ article.body }}</p>
        </li>
    {% endfor %}
    </ul>
    {% endblock %}

Das Template für ein Feed Element
:file:`news/templates/news/article_detail.html` anlegen::

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - {{ article.headline }}{% endblock %}

    {% block content %}
    <h4>{{ article.headline }}</h4>
    <p>{{ article.date_updated }}</p>
    <p>{{ article.body }}</p>
    {% endblock %}

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Das  Feed Framework<ref/contrib/syndication/>`
