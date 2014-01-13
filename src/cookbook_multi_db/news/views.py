from django.views.generic import DetailView, ListView

from news.models import Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
