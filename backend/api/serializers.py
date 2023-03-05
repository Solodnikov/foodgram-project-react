from recipes.models import (Favourite, Ingredient, IngredientsinRecipt, Recipe,
                            Shopping_list, Tag)
from rest_framework import serializers
# from users.models import CustomUser, Subscribe
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsinReciptSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsinRecipt
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_list
        fields = ('user', 'recipe')


class RecipeSerialiser(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True, required=False)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
            'id',
            'ingredients'
        )

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user
        return Favourite.objects.filter(
            user=request_user.id,
            recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        return Shopping_list.objects.filter(
            user=request_user.id,
            recipe=obj.id
        ).exists()

    def get_ingredients(self, obj):
        ingredients = IngredientsinRecipt.objects.filter(recipe=obj)
        return IngredientsinReciptSerializer(ingredients, many=True).data
