from rest_framework import serializers

from .models import *


User = get_user_model()


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


class SpecificMaterialSerializer(serializers.ModelSerializer):
    """Сериализатор для конкретного материала."""
    material = serializers.CharField(source='material.name')
    measurement_unit = serializers.CharField(source='measurement_unit.measurement_unit')

    class Meta:
        model = SpecificMaterial
        fields = ('id', 'name', 'material', 'length', 'width', 'thickness', 'volume', 'measurement_unit')


class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для результатов по каждому материалу"""
    specific_material = SpecificMaterialSerializer()

    class Meta:
        model = Result
        fields = ('name', 'specific_material', 'amount', )


class CalculationSerializer(serializers.ModelSerializer):
    """Сериализатор для расчетов."""
    results = ResultSerializer(many=True)
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    customer = CustomersSerializer()

    class Meta:
        model = Calculation
        fields = ('id', 'title', 'manager', 'customer', 'adress_object_construction', 'created_date', 'state_calculation', 'results')