from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavouriteApiView, IngredientViewSet, ShoppingApiView,
                    TagViewSet, RecipeViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:id>/favorite/', FavouriteApiView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingApiView.as_view()),
]
