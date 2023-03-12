from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favourite, Ingredient, IngredientsinRecipt, Recipe,
                            Shopping_list, Tag, TaginRecipe)
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для просмотра тегов """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsinReciptSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для представления сведений об игредиентах в рецепте.
    """
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
    """
    Сериалайзер для создания и удаления. Избранные рецепты.
    """

    class Meta:
        model = Favourite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return ShortRecipeSerialiser(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания и удаления. Список покупок.
    """

    class Meta:
        model = Shopping_list
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return ShortRecipeSerialiser(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class RecipeSerialiser(serializers.ModelSerializer):
    """
    Сериалайзер для получения рецепта и списка рецептов.
    """
    tags = TagSerializer(many=True, read_only=True, required=False)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

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


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления ингредиента в рецепт. """

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsinRecipt
        fields = ('id', 'amount')


class RecipeCreateSerialiser(serializers.ModelSerializer):
    """
    Сериалайзер для создания и обновления рецепта.
    """
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create_ingredients(self, ingredients, recipe):
        for i in ingredients:
            ingredient = Ingredient.objects.get(id=i['id'])
            IngredientsinRecipt.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=i['amount'],
            )

    def create_tags(self, tags, recipe):
        for tag in tags:
            TaginRecipe.objects.create(recipe=recipe, tag=tag)

    def create(self, validated_data):
        """
        Создание рецепта.
        Доступно только авторизированному пользователю.
        """

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_ingredients(ingredients, recipe)
        # recipe.tags.set(tags)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        """
        Изменение рецепта.
        Доступно только автору.
        """

        TaginRecipe.objects.filter(recipe=instance).delete()
        IngredientsinRecipt.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients(ingredients, instance)
        self.create_tags(tags, instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image'):
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerialiser(instance, context={
            'request': self.context.get('request')
        }).data


# class ShortRecipeSerialiser(serializers.ModelSerializer):
#     """
#     Сериалайзер для представления кратких сведений рецепта.
#     """
#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')



#       "email"
#       "id"
#       "username"
#       "first_name"
#       "last_name"
#       "is_subscribed"
#       "recipes"

#           "id"
#           "name"
#           "image"
#           "cooking_time"

#     recipes = ShortRecipeSerialiser(many=True, read_only=True, required=False)

