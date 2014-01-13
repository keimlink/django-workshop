from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext

from .forms import RecipeForm
from .models import Recipe

import logging
logger = logging.getLogger(__name__)


def index(request):
    """Displays all recipes."""
    recipes = Recipe.objects.all()
    logger.debug('Number of recipes: %d' % recipes.count())
    logger.info('This is the index view')
    return render_to_response('recipes/index.html', {'object_list': recipes},
        context_instance=RequestContext(request))


def detail(request, slug):
    """Displays a single :model:`recipes.Recipe` using :template:`recipes/detail.html`.

    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    return render_to_response('recipes/detail.html', {'object': recipe},
        context_instance=RequestContext(request))


@login_required
def add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render(request, 'recipes/form.html', {'form': form, 'add': True})


@login_required
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/form.html', {'form': form, 'add': False})
