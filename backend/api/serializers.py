from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (AmountOfIngredient, Favourite, Ingredient, Recipe,
                            ShoppingList, Tag)
from rest_framework import serializers
from users.models import Subscribe, User


class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для предоставлении сведений о пользователе. """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return request_user.subscriber.filter(subscribing=obj).exists()


class UserCreateSerializer(UserCreateSerializer):
    """ Сериализатор создания пользователя """

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')


class SubscribeSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки подписки """

    class Meta:
        model = Subscribe
        fields = ('subscriber', 'subscribing')

    def to_representation(self, instance):
        return ShowSubscribeSerializer(
            instance.subscribing,
            context={'request': self.context.get('request')}
        ).data


class ShowSubscribeSerializer(CustomUserSerializer):
    """ Сериалайзер для отображения подписки. """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params.get('recipes_limit')
        if limit and isinstance(limit, int):
            recipes = recipes[:int(limit)]
        return ShortRecipeSerialiser(
            recipes,
            many=True,
            context={'request': request}).data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()


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
        model = AmountOfIngredient
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
        model = ShoppingList
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
        if request_user.is_anonymous:
            return False
        return request_user.favourites.filter(recipe=obj).exists()

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return request_user.subscriber.filter(subscribing=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return request_user.shopping_list.filter(recipe=obj).exists()

    def get_ingredients(self, obj):
        ingredients = AmountOfIngredient.objects.filter(recipes=obj)
        return IngredientsinReciptSerializer(ingredients, many=True).data


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления ингредиента в рецепт. """

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = AmountOfIngredient
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
    cooking_time = serializers.IntegerField()

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

    def create_ingredients_and_tags(self, instance, validated_data):
        ingredients, tags = (
            validated_data.pop('ingredients'), validated_data.pop('tags')
        )
        for ingredient in ingredients:
            amount_of_ingredient, flag = (
                AmountOfIngredient.objects.get_or_create(
                    ingredient=get_object_or_404(
                        Ingredient,
                        pk=ingredient['id']
                    ),
                    amount=ingredient['amount'],
                )
            )
            instance.ingredients.add(amount_of_ingredient)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def create(self, validated_data):
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        return self.create_ingredients_and_tags(recipe, saved)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.create_ingredients_and_tags(instance, validated_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerialiser(instance, context={
            'request': self.context.get('request')
        }).data


class ShortRecipeSerialiser(serializers.ModelSerializer):
    """
    Сериалайзер для представления кратких сведений рецепта.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
