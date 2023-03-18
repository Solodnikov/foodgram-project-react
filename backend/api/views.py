from api.permissions import AuthorAdminAndReadPermission
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favourite, Ingredient, IngredientsinRecipt, Recipe,
                            ShoppingList, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .serializers import (FavouriteSerializer, IngredientSerializer,
                          RecipeCreateSerialiser, RecipeSerialiser,
                          ShoppingSerializer, TagSerializer)

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Subscribe
from api.pagination import CustomPagination
from api.permissions import CustomUserPermission
from api.serializers import SubscribeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class FavouriteApiView(APIView):
    """ Добавление/удаление рецепта из избранного. """

    permission_classes = (permissions.IsAuthenticated, )

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
    """ Добавление/удаление рецепта из списка покупок. """

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not ShoppingList.objects.filter(
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
        if ShoppingList.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            ShoppingList.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для действий с рецептами.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialiser
    pagination_class = CustomPagination
    permission_classes = (AuthorAdminAndReadPermission, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerialiser
        return RecipeCreateSerialiser

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class DownloadShoppingCartApiView(APIView):
    """ Скачивание ингридиентов из рецептов списка покупок. """

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        request_user = request.user

        ingredients = IngredientsinRecipt.objects.filter(
            recipe__shopping_list__user=request_user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        shopping_list = 'Список покупок \n'

        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])

        filename = f'{request_user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination
    permission_classes = (CustomUserPermission, )


class SubscribeApiView(APIView):
    """ Добавление/удаление подписки на автора. """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, id):
        data = {
            'subscriber': request.user.id,
            'subscribing': id
        }
        if not Subscribe.objects.filter(subscriber=request.user.id,
                                        subscribing=id).exists():
            serializer = SubscribeSerializer(data=data,
                                             context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = request.user.id
        subscribing = id
        if Subscribe.objects.filter(subscriber=user,
                                    subscribing=subscribing).exists():
            subscription = get_object_or_404(
                Subscribe, subscriber=user, subscribing=subscribing)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsApiView(APIView, CustomPagination):
    """ Получение пользователем сведений о своих подписках. """

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user.id
        if not Subscribe.objects.filter(subscriber=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        subscriptions = Subscribe.objects.filter(
            subscriber=user)
        results = self.paginate_queryset(subscriptions, request, view=self)
        serializer = SubscribeSerializer(results,
                                         context={'request': request},
                                         many=True)
        return self.get_paginated_response(serializer.data)
