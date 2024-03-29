from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import AuthorAdminAndReadPermission, CustomUserPermission
from api.serializers import (FavouriteSerializer, IngredientSerializer,
                             RecipeCreateSerialiser, RecipeSerialiser,
                             ShoppingSerializer, SubscribeSerializer,
                             TagSerializer)
from users.models import Subscribe
from recipes.models import (AmountOfIngredient, Favourite, Ingredient, Recipe,
                            ShoppingList, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )


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
        ingredients = AmountOfIngredient.objects.filter(
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
    """ Получение пользователем сведений о своих подписках.
    Добавление/удаление подписки на автора.
    """
    pagination_class = CustomPagination
    permission_classes = (CustomUserPermission, )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscriptions(self, request):
        request_user = request.user
        queryset = Subscribe.objects.filter(subscriber=request_user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscribe(self, request, id):
        if request.method == 'POST':
            data = {
                'subscriber': request.user.id,
                'subscribing': id
            }
            if not request.user.subscriber.filter(subscribing=id).exists():
                serializer = SubscribeSerializer(data=data,
                                                 context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if request.user.subscriber.filter(subscribing=id).exists():
                subscription = get_object_or_404(
                    Subscribe,
                    subscriber=request.user.id,
                    subscribing=id
                )
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
