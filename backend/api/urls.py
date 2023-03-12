from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import SubscribeApiView, SubscriptionsApiView

from .views import (DownloadShoppingCartApiView, FavouriteApiView,
                    IngredientViewSet, RecipeViewSet, ShoppingApiView,
                    TagViewSet)

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
    path('users/subscriptions/', SubscriptionsApiView.as_view())
]
