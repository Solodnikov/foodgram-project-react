from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavouriteApiView, IngredientViewSet, ShoppingApiView,
                    TagViewSet, RecipeViewSet, DownloadShoppingCartApiView)
from users.views import SubscribeApiView


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartApiView.as_view()),
    path('', include(router.urls)),
    path('recipes/<int:id>/favorite/', FavouriteApiView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingApiView.as_view()),
    path('users/<int:id>/subscribe/', SubscribeApiView.as_view()),
    # path('/api/users/subscriptions/', Subscriptions)

]
