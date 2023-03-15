from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .models import CustomUser, Subscribe


class ShortRecipeSerialiser(serializers.ModelSerializer):
    """
    Сериалайзер для представления кратких сведений рецепта.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


# class CustomUserSerializer(UserSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = (
#             'email', 'id', 'username', 'first_name', 'last_name',
#             'is_subscribed')

#     def get_is_subscribed(self, obj):
#         request_user = self.context.get('request').user
#         if request_user.is_anonymous:
#             return False
#         return Subscribe.objects.filter(
#             subscriber=request_user,
#             subscribing=obj
#         ).exists()
    

class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для предоставлении сведений о пользователе. """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
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
        model = CustomUser
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


class ShowSubscribeSerializer(serializers.ModelSerializer):
    """ Сериалайзер для отображения подписки. """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
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

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return request_user.subscriber.filter(subscribing=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return ShortRecipeSerialiser(
            recipes,
            many=True,
            context={'request': request}).data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()
