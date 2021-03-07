from rest_framework import serializers

from .models import *


class CustomersSerializer(serializers.ModelSerializer):
    """Сериализатор для заказчиков."""
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Customers
        fields = '__all__'


class CalculationSerializer(serializers.ModelSerializer):
    """Сериализатор для рассчетов."""
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Calculation
        fields = '__all__'
