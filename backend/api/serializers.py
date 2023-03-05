from recipes.models import (CustomUser, Favourite, Ingredient,
                            IngredientsinRecipt, Recipe, Shopping_list, Tag)
from rest_framework import serializers
from users.models import CustomUser, Subscribe
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
    # amount = IngredientsinRecipt(read_only=True)
    # amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit', 'recipes'
            # 'amount',
        )
    # def get_amount(self,obg):


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')
        # read_only_fields = ('user')


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_list
        fields = ('user', 'recipe')


# class CustomUserSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = (
#             'email', 'username', 'first_name',
#             'first_name', 'is_subscribed',
#         )
        # read_only_fields = ('id',)

    # def get_is_subscribed(self, obj):
    #     request_user = self.context.get('request').user
    #     return Subscribe.objects.filter(
    #         subscriber=request_user,
    #         subscribing=obj
    #     ).exists()


class RecipeSerialiser(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True, required=False)
        # "id": 28839286,
        # "name": "Завтрак",
        # "color": "#E26C2D",
        # "slug": "breakfast"
    author = CustomUserSerializer(read_only=True)
        # "username": "Pn1Wz",
        # "email": "2nvuYmL-1AS@JzG.qci",
        # "id": 1985130,
        # "first_name": "Вася",
        # "last_name": "Пупкин",
        # "is_subscribed": false
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # ingredients = serializers.StringRelatedField(many=True, read_only=True)
    # ingredients = IngredientSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    
    # ingredients = IngredientsinReciptSerializer(
    #     source='ingredientsinrecipt_set',
    #     many=True,
    #     read_only=True,
    # )
    #   "name": "Картофель отварной",
    #   "measurement_unit": "г",
    #   "id": -55850568,
    #   "amount": 3507066


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
