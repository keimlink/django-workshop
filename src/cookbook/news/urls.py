from django.conf.urls.defaults import patterns, include, url

from news.feeds import ArticleFeed
from news.views import ArticleDetailView, ArticleListView


urlpatterns = patterns('',
    url(r'^feed/rss/$', ArticleFeed(), name='news_article_feed'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='news_article_detail'),
    url(r'^$', ArticleListView.as_view(), name='news_article_list'),
)
