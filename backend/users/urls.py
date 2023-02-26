from django.urls import path
from django.urls import include


app_name = 'users'

urlpatterns = [
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
