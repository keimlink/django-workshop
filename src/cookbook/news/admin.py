from django.contrib import admin

from news.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'date_created', 'date_updated')


admin.site.register(Article, ArticleAdmin)
