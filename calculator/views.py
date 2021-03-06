from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *


class CustomersViewSet(viewsets.ModelViewSet):
    """CRUD для заказчиков"""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = CustomersSerializer

    def get_queryset(self):
        manager = self.request.user.id
        return Customers.objects.filter(manager=manager)

