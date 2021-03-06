from rest_framework import serializers

from .models import *


class CustomersSerializer(serializers.ModelSerializer):
    """Сериализатор для заказчиков"""
    class Meta:
        model = Customers
        fields = '__all__'