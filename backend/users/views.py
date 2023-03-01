# Create your views here.
from djoser.views import UserViewSet
from api.serializers import CustomUserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer

    @action(methods=['get'], detail=False, url_path='me')
    # def me(self, request, *args, **kwargs):
    #     self.get_object = self.get_instance
    #     if request.method == "GET":
    #         return self.retrieve(request, *args, **kwargs)

    # РАБОТАЕТ НЕВЕРНО!

    def me(self, request):
        request_user = request.user
        serialiser = self.get_serializer(request_user)
        return Response(serialiser.data)
    
    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = CustomUserSerializer
    #     kwargs.setdefault('context', self.get_serializer_context())
    #     return serializer_class(*args, **kwargs)

