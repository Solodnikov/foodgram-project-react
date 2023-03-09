from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscribe
from .pagination import CustomUserPagination
# from rest_framework.permissions import AllowAny
from .permissions import CustomUserPermission
from .serializers import CustomUserSerializer, SubscribeSerializer
from django.shortcuts import get_object_or_404


class CustomUserViewSet(UserViewSet):
    # serializer_class = CustomUserSerializer
    pagination_class = CustomUserPagination
    permission_classes = (CustomUserPermission, )


class SubscribeApiView(APIView):
    """ Добавление/удаление подписки на автора. """

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
