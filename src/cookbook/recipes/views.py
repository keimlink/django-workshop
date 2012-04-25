import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from recipes.forms import RecipeForm
from recipes.models import Recipe
from utils import PDFView


logger = logging.getLogger('cookbook.recipes.views')


class RecipeListView(ListView):
    template_name = 'recipes/index.html'

    def get_queryset(self):
        recipes = Recipe.active.all()
        logger.debug('Anzahl der Rezepte: %d' % recipes.count())
        return recipes


class RecipeDetailView(DetailView):
    queryset = Recipe.active.all()
    template_name = 'recipes/detail.html'


class RecipePDFView(PDFView):
    model = Recipe
    template_name = 'recipes/detail_pdf.html'


@login_required
def add(request):
    if request.method == 'POST':
        form = RecipeForm(user=request.user, data=request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render(request, 'recipes/form.html',
        {'form': form, 'add': True})

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
    return render(request, 'recipes/form.html',
        {'form': form, 'add': False, 'object': recipe})
