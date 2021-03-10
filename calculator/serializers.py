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


class OpeningsSerializer(serializers.ModelSerializer):
    """Сериализатор для проемов."""

    class Meta:
        model = Openings
        fields = '__all__'


class StructuralElementFrameSerializer(serializers.ModelSerializer):
    """Сериализатор для рассчетов."""
    calculations = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Calculation.objects.all(),
        required=True,
    )
    openings = OpeningsSerializer(many=True)

    class Meta:
        model = StructuralElementFrame
        fields = '__all__'


class StructuralElementFramePostSerializer(serializers.ModelSerializer):
    """Сериализатор для рассчетов."""
    calculations = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Calculation.objects.all(),
        required=True,
    )
    openings = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Openings.objects.all(),
        many=True
    )

    class Meta:
        model = StructuralElementFrame
        fields = '__all__'


class SpecificMaterialsSerializer(serializers.ModelSerializer):
    """Сериализатор для материалов."""

    class Meta:
        model = SpecificMaterial
        fields = '__all__'


class ResultsSerializer(serializers.ModelSerializer):
    """Сериализатор для результатов по каждому материалу"""
    specific_material = SpecificMaterialsSerializer()

    class Meta:
        model = Results
        fields = ('name', 'specific_material', 'amount', 'price')


class CalculationSerializer(serializers.ModelSerializer):
    """Сериализатор для расчетов."""
    results = ResultsSerializer(many=True)
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    customer = serializers.CharField(source='customer.first_name')

    class Meta:
        model = Calculation
        fields = ('id', 'title', 'manager', 'customer',
                  'adress_object_construction', 'created_date',
                  'state_calculation', 'results')
