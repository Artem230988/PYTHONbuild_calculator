from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для получении информации о своем профиле."""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'second_name', 'last_name', 'email', 'photo', 'phone')
