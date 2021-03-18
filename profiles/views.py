from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserDetailSerializer
from .models import User


class UserDetailView(APIView):
    """Профиль пользователя детально"""

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
