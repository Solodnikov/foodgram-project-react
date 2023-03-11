from api.permissions import AuthorAdminAndReadPermission
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favourite, Ingredient, IngredientsinRecipt, Recipe,
                            Shopping_list, Tag)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter
from .pagination import RecipePagination
from .serializers import (FavouriteSerializer, IngredientSerializer,
                          RecipeCreateSerialiser, RecipeSerialiser,
                          ShoppingSerializer, TagSerializer)
from django.http import HttpResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


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


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для действий с рецептами.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialiser
    pagination_class = RecipePagination
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




        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename={filename}'
        # sheet = canvas.Canvas(response,)
        #                     #   pagesize=A4)
        # sheet.setTitle('Список покупок')
        # begin_position_x = 20
        # begin_position_y = 650
        # for ingredient in ingredients:
        #     sheet.drawString(
        #         begin_position_x,
        #         begin_position_y,
        #         text=(f'- {ingredient["ingredient__name"]} '
        #               f'({ingredient["ingredient__measurement_unit"]})'
        #               f' - {ingredient["amount"]}')
        #     )
        #     begin_position_y -= 30
        #     sheet.showPage()
        #     sheet.save()
        #     return response
