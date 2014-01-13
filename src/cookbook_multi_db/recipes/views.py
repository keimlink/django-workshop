from django.http import Http404
from django.http import HttpResponse
from django.template import Context, loader

from .models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    t = loader.get_template('recipes/index.html')
    c = Context({'object_list': recipes})
    return HttpResponse(t.render(c))


def detail(request, slug):
    try:
        recipe = Recipe.objects.get(slug=slug)
    except Recipe.DoesNotExist:
        raise Http404
    t = loader.get_template('recipes/detail.html')
    c = Context({'object': recipe})
    return HttpResponse(t.render(c))
