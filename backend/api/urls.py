from api.views import (DownloadShoppingCartApiView, FavouriteApiView,
                       IngredientViewSet, RecipeViewSet, ShoppingApiView,
                       TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartApiView.as_view()),
    # path('', include(router.urls)),
    # path('recipes/download_shopping_cart/',
    #      DownloadShoppingCartApiView.as_view()),
    path('recipes/<int:id>/favorite/', FavouriteApiView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingApiView.as_view()),
    path('', include(router.urls)),
]
