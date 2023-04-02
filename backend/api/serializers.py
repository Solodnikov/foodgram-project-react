from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (AmountOfIngredient, Favourite, Ingredient, Recipe,
                            ShoppingList, Tag)
from users.models import Subscribe, User


class UserSerializer(serializers.ModelSerializer):
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


class ShowSubscribeSerializer(UserSerializer):
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
        if limit:
            try:
                limit_number = int(limit)
                recipes = recipes[:limit_number]
            except Exception as error:
                raise TypeError(f'параметр "recipes_limit" содержит символы, '
                                f'не являющиеся цифрами. '
                                f'Возникла ошибка - {error}')
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
    author = UserSerializer(read_only=True)
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
        return Favourite.objects.filter(
            user=request_user.id,
            recipe=obj.id
        ).exists()

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return request_user.subscriber.filter(subscribing=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request_user.id,
            recipe=obj.id
        ).exists()

    def get_ingredients(self, obj):
        ingredients = AmountOfIngredient.objects.filter(recipe=obj)
        return IngredientsinReciptSerializer(ingredients, many=True).data


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления ингредиента в рецепт. """

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if 10000 > value < 0:
            raise serializers.ValidationError(
                'Количество ингредиентов не должно быть 0 и меньше'
                ' и больше 10000.'
            )
        return value

    class Meta:
        model = AmountOfIngredient
        fields = ('id', 'amount')


class RecipeCreateSerialiser(serializers.ModelSerializer):
    """
    Сериалайзер для создания и обновления рецепта.
    """
    author = UserSerializer(read_only=True)
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

    def validate_cooking_time(self, value):
        if 10000 > value < 0:
            raise serializers.ValidationError(
                'Время готовки не должно быть 0 и меньше'
                ' и больше 10000.'
            )
        return value

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise serializers.ValidationError(
                'Нужен хотя бы один ингредиент!'
            )
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise serializers.ValidationError(
                'Нужно выбрать хотя бы один тег!'
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги должны быть уникальными!'
                )
            tags_list.append(tag)
        return value

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
                    recipe=instance
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
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        AmountOfIngredient.objects.filter(recipe_id=instance).delete()
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        self.create_ingredients_and_tags(instance, saved)
        instance.save()
        return instance

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
