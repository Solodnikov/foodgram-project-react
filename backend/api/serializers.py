from rest_framework import serializers
from recipes.models import Tag, Ingredient, Favourite, CustomUser, Recipe
from users.models import CustomUser
from users.models import Subscribe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')
        # read_only_fields = ('user')


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('user', 'recipe')


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name',
            'first_name', 'is_subscribed',
        )
        # read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        return Subscribe.objects.filter(
            subscriber=request_user,
            subscribing=obj
        ).exists()


class RecipeSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('__all__')

