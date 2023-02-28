from django.shortcuts import get_object_or_404
from recipes.models import Favourite, Ingredient, Recipe, Shopping_list, Tag
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (FavouriteSerializer, IngredientSerializer,
                          TagSerializer, ShoppingSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class FavouriteViewSet(CreateDestroyViewSet):
    serializer_class = FavouriteSerializer
    queryset = Favourite.objects.all()


class FavouriteApiView(APIView):
    """ Добавление/удаление рецепта из избранного. """

    # permission_classes = [IsAuthenticated, ]
    # pagination_class = CustomPagination

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not Favourite.objects.filter(
           user=request.user, recipe__id=id).exists():
            serializer = FavouriteSerializer(
                data=data, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if Favourite.objects.filter(user=request.user, recipe=recipe).exists():
            Favourite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingApiView(APIView):
    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not Shopping_list.objects.filter(
           user=request.user, recipe__id=id).exists():
            serializer = ShoppingSerializer(
                data=data, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if Shopping_list.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            Shopping_list.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
