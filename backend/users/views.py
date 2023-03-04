# Create your views here.
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import CustomUserPagination
# from rest_framework.permissions import AllowAny
from .permissions import CustomUserPermission


class CustomUserViewSet(UserViewSet):
    # serializer_class = CustomUserSerializer
    pagination_class = CustomUserPagination
    permission_classes = (CustomUserPermission, )

    # @action(methods=['get'], detail=False, url_path='me')
    # def me(self, request):
    #     request_user = request.user
    #     serialiser = self.get_serializer_class(request_user)
    #     return Response(serialiser.data)

    #  КОСТЫЛЬ ДЛЯ ПОЛУЧЕНИЯ is_subscribed В /api/users/me/
    def get_serializer_class(self):
        if self.action == 'list' or (
            self.action == 'me' or self.action == 'retrieve'
        ):
            return CustomUserSerializer
        return super().get_serializer_class()
