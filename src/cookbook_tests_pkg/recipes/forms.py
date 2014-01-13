from django.forms import ModelForm
from django.template.defaultfilters import slugify

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author', 'slug', 'date_created', 'date_updated')

    def __init__(self, *args, **kwargs):
        self.__user = kwargs.pop('user', None)
        super(RecipeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.instance.pk:
            if not self.__user:
                raise TypeError("You didn't give an user argument to the constructor.")
            self.instance.author = self.__user
            self.instance.slug = slugify(self.instance.title)
        return super(RecipeForm, self).save(commit)
