from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from recipes.forms import RecipeForm
from recipes.models import Recipe

def index(request):
    recipes = Recipe.objects.all()
    return render_to_response('recipes/index.html', {'object_list': recipes},
        context_instance=RequestContext(request))

def detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render_to_response('recipes/detail.html', {'object': recipe},
        context_instance=RequestContext(request))

@login_required
def add(request):
    if request.method == 'POST':
        form = RecipeForm(user=request.user, data=request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render_to_response('recipes/form.html',
        {'form': form, 'add': True},
        context_instance=RequestContext(request))

@login_required
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = RecipeForm(instance=recipe, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm(instance=recipe)
    return render_to_response('recipes/form.html',
        {'form': form, 'add': False, 'object': recipe},
        context_instance=RequestContext(request))
