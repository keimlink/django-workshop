from django.forms import ModelForm
from django.template.defaultfilters import slugify

from recipes.models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('slug', 'author', 'date_created', 'date_updated')
    
    def __init__(self, **kwargs):
        try:
            self.__user = kwargs.pop('user')
        except KeyError:
            self.__user = None
        super(RecipeForm, self).__init__(**kwargs)
    
    def save(self, commit=True):
        if self.instance.pk is None:
            if self.__user is None:
                raise TypeError("You didn't give an user argument to the constructor.")
            self.instance.slug = slugify(self.instance.title)
            self.instance.author = self.__user
        return super(RecipeForm, self).save(commit)
