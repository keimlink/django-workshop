Ein RSS Feed für die "News" App
*******************************

Die im Kapitel :ref:`mehrere_datenbanken` erstellte App "news" hat noch kein
Frontend und soll deshalb einen `RSS Feed`_ bekommen.

.. _RSS Feed: https://de.wikipedia.org/wiki/RSS

Den Feed erstellen
==================

Dazu legst du zuerst die Datei :file:`news/feeds.py` an::

    from django.conf import settings
    from django.contrib.syndication.views import Feed

    from .models import Article


    class ArticleFeed(Feed):
        title = 'Neuigkeiten aus dem Kochbuch'
        link = '/'
        description = 'Der RSS Feed der Kochbuch Website'

        def items(self):
            return Article.objects.order_by('-date_created')[:settings.NEWS_FEED_COUNT]

        def item_title(self, item):
            return item.headline

        def item_description(self, item):
            return item.body

Da wir die Anzahl der Elemente im RSS Feed aus der Datei :file:`settings.py`
lesen müssen wir sie auch dort definieren::

    NEWS_FEED_COUNT = 5

Die URLs für den Feed definieren
================================

Dann erstellst du die ``URLConf`` in :file:`news/urls.py`::

    from django.conf.urls import patterns, include, url

    from .feeds import ArticleFeed
    from .views import ArticleDetailView, ArticleListView


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

    from .models import Article


    class ArticleDetailView(DetailView):
        model = Article


    class ArticleListView(ListView):
        model = Article

Die Templates erstellen
=======================

Und am Ende die Templates anlegen bzw. erweitern.

Zuerst das Template :file:`templates/base.html` um den Eintrag für den Feed erweitern:

..  code-block:: html+django

    <head>
        <title>{% block title %}Kochbuch{% endblock %}</title>
        <link rel="alternate" type="application/rss+xml"
            title="Neuigkeiten aus dem Kochbuch" href="{% url news_article_feed %}" />
    </head>

Viele Browser zeigen den Link zum RSS Feed in der Adressleiste nur nach
der Installation von zusätzlichen Erweiterungen an (`RSS-Abonnement für
Chrome`_, `RSS Icon In Awesombar für Firefox`_). Daher kann es sinnvoll
sein den Link zum RSS Feed auch im ``body`` der Seite einzutragen:

..  code-block:: html+django

    <body>
        <header>
            <h1>Kochbuch</h1>
            <p><a href="{% url news_article_feed %}">RSS Feed</a></p>
        </header>
        ...
    </body>

Dann das Template für die Liste der Feed Elemente in
:file:`news/templates/news/article_list.html` anlegen. Der Filter
``truncatewords`` zeigt nur die ersten zehn Worte des Nachrichtentextes
an:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - News{% endblock %}

    {% block content %}
    <ul>
    {% for article in article_list %}
        <li>
            <h4><a href="{{ article.get_absolute_url }}">{{ article.headline }}</a></h4>
            <p>{{ article.date_updated }}</p>
            <p>{{ article.body|truncatewords:10 }}</p>
        </li>
    {% endfor %}
    </ul>
    {% endblock %}

Und zuletzt das Template für ein Feed Element in :file:`news/templates/news/article_detail.html` erstellen:

..  code-block:: html+django

    {% extends "base.html" %}

    {% block title %}{{ block.super }} - {{ article.headline }}{% endblock %}

    {% block content %}
    <h4>{{ article.headline }}</h4>
    <p>{{ article.date_updated }}</p>
    <p>{{ article.body }}</p>
    {% endblock %}

.. _RSS-Abonnement für Chrome: https://chrome.google.com/webstore/detail/rss-subscription-extensio/nlbjncdgjeocebhnmkbbbdekmmmcbfjd
.. _RSS Icon In Awesombar für Firefox: https://addons.mozilla.org/de/firefox/addon/rss-icon-in-awesombar/

Die Site anpassen
=================

Damit die Links im RSS Feed auch funktionieren muss noch die Site im Admin
angepasst werden. Dazu im Admin die Liste der Sites anzeigen und die Site mit
dem Domainnamen ``example.com`` zum Bearbeiten auswählen. Statt ``example.com``
muss als Domainname ``127.0.0.1:8000`` eingetragen werden. Der Anzeigename
muss nicht unbedingt geändert werden - es schadet aber auch nicht.

Weiterführende Links zur Django Dokumentation
=============================================

* :djangodocs:`Das  Feed Framework<ref/contrib/syndication/>`
