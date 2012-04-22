from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from recipes.models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    return render_to_response('recipes/index.html', {'object_list': recipes},
        context_instance=RequestContext(request))


def detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render_to_response('recipes/detail.html', {'object': recipe},
        context_instance=RequestContext(request))
