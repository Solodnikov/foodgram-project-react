# from django.shortcuts import get_object_or_404
# from djoser.views import UserViewSet
# from rest_framework import permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from users.models import Subscribe
# from api.pagination import CustomPagination
# from api.permissions import CustomUserPermission
# from api.serializers import SubscribeSerializer


# class CustomUserViewSet(UserViewSet):
#     pagination_class = CustomPagination
#     permission_classes = (CustomUserPermission, )


# class SubscribeApiView(APIView):
#     """ Добавление/удаление подписки на автора. """
#     permission_classes = (permissions.IsAuthenticated, )

#     def post(self, request, id):
#         data = {
#             'subscriber': request.user.id,
#             'subscribing': id
#         }
#         if not Subscribe.objects.filter(subscriber=request.user.id,
#                                         subscribing=id).exists():
#             serializer = SubscribeSerializer(data=data,
#                                              context={'request': request})
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     serializer.data, status=status.HTTP_201_CREATED)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         user = request.user.id
#         subscribing = id
#         if Subscribe.objects.filter(subscriber=user,
#                                     subscribing=subscribing).exists():
#             subscription = get_object_or_404(
#                 Subscribe, subscriber=user, subscribing=subscribing)
#             subscription.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# class SubscriptionsApiView(APIView, CustomPagination):
#     """ Получение пользователем сведений о своих подписках. """

#     permission_classes = (permissions.IsAuthenticated, )

#     def get(self, request):
#         user = request.user.id
#         if not Subscribe.objects.filter(subscriber=user).exists():
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         subscriptions = Subscribe.objects.filter(
#             subscriber=user)
#         results = self.paginate_queryset(subscriptions, request, view=self)
#         serializer = SubscribeSerializer(results,
#                                          context={'request': request},
#                                          many=True)
#         return self.get_paginated_response(serializer.data)
