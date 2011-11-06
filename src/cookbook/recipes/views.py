import logging

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.generic.detail import BaseDetailView

from recipes.forms import RecipeForm
from recipes.models import Recipe

logger = logging.getLogger('cookbook.recipes.views')


class RecipeListView(ListView):
    template_name = 'recipes/index.html'

    def get_queryset(self):
        recipes = Recipe.objects.all()
        logger.debug('Anzahl der Rezepte: %d' % recipes.count())
        return recipes


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/detail.html'


class SingleObjectJSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing self.object as payload."
        return self.get_json_response(serializers.serialize('json', [self.object]))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct a JSON `HttpResponse` object."
        return HttpResponse(content, content_type='application/json',
            **httpresponse_kwargs)


class JSONDetailView(SingleObjectJSONResponseMixin, BaseDetailView):
    queryset = Recipe.objects.all()


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
