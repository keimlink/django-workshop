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
