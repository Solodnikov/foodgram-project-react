from rest_framework import serializers
from .models import CustomUser, Subscribe
from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            subscriber=request_user,
            subscribing=obj
        ).exists()
