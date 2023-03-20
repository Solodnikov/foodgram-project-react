from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    """ Фильтр для ингредиентов. """
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_favorited = filters.NumberFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favourites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset
