from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import *

User = get_user_model()


class CalculationCustomerSerializer(serializers.ModelSerializer):
    """Сериализатор для расчетов."""
    state_calculation = serializers.SlugRelatedField(
        slug_field='title',
        queryset=CalculationState.objects.all(),
        required=True,
    )

    class Meta:
        model = Calculation
        fields = ('id', 'title', 'adress_object_construction',
                  'created_date', 'state_calculation')


class CustomersSerializer(serializers.ModelSerializer):
    """Сериализатор для заказчиков."""
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Customers
        fields = ('id', 'last_name', 'first_name', 'second_name',
                  'phone', 'email', 'adress', 'manager')


class CustomersDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для заказчиков."""
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    calculation = CalculationCustomerSerializer(many=True, read_only=True)

    class Meta:
        model = Customers
        fields = ('id', 'last_name', 'first_name', 'second_name',
                  'phone', 'email', 'adress', 'manager', 'calculation')


class SpecificMaterialSerializer(serializers.ModelSerializer):
    """Сериализатор для конкретного материала."""
    material = serializers.CharField(source='material.name')
    measurement_unit = serializers.CharField(
        source='measurement_unit.measurement_unit')

    class Meta:
        model = SpecificMaterial
        fields = ('id', 'material', 'measurement_unit', 'name')


class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для результатов по каждому материалу"""
    specific_material = SpecificMaterialSerializer()

    class Meta:
        model = Result
        fields = ('name', 'specific_material', 'amount',
                  'price', 'full_price', 'floor')


class CalculationPostSerializer(serializers.ModelSerializer):
    """Сериализатор для расчетов."""
    customer = serializers.SlugRelatedField(
        slug_field='pk',
        queryset=Customers.objects.all(),
        required=True,
    )
    state_calculation = serializers.SlugRelatedField(
        slug_field='title',
        queryset=CalculationState.objects.all(),
        required=True,
    )

    class Meta:
        model = Calculation
        fields = ('customer', 'adress_object_construction',
                  'title', 'state_calculation')


class CalculationStateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения статуса расчета"""
    state_calculation = serializers.SlugRelatedField(
        slug_field='title',
        queryset=CalculationState.objects.all(),
        required=True,
    )

    class Meta:
        model = Calculation
        fields = ('state_calculation', )


class OpeningsSerializer(serializers.ModelSerializer):
    """Сериализатор для проемов."""

    class Meta:
        model = Opening
        fields = ('type', 'wigth', 'height', 'count')


class StructuralElementFrameSerializer(serializers.ModelSerializer):
    """Сериализатор для рассчетов."""
    step_of_racks = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.6
    )
    external_wall_thickness = serializers.SlugRelatedField(
        slug_field='width',
        queryset=SpecificMaterial.objects.filter(
            material__name='Доска',
            thickness=50,
            length=3000
        )
    )
    internal_wall_thickness = serializers.SlugRelatedField(
        slug_field='width',
        queryset=SpecificMaterial.objects.filter(
            material__name='Доска',
            thickness=50,
            length=3000
        )
    )
    steam_waterproofing_external_walls = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    steam_waterproofing_base_area = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    windscreen_external_walls = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    windscreen_base_area = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    insulation_external_walls = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    insulation_base_area = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    OSB_for_interior_walls = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    OSB_for_external_walls = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    OSB_for_base_area = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )

    class Meta:
        model = StructuralElementFrame
        exclude = ('calculations',)


class FrameOpeningsSerializer(serializers.Serializer):
    frame = StructuralElementFrameSerializer()
    openings = OpeningsSerializer(many=True)


class FrameSerializer(serializers.ModelSerializer):
    openings = OpeningsSerializer(many=True)

    class Meta:
        model = StructuralElementFrame
        exclude = ('calculations',)


class StructuralElementFoundationSerializer(serializers.ModelSerializer):
    """Сериализатор для фундамента"""
    concrete_pile = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )
    concrete = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SpecificMaterial.objects.all()
    )

    class Meta:
        model = StructuralElementFoundation
        fields = ('perimeter_of_external_walls', 'internal_wall_length',
                  'concrete_pile', 'concrete')


class CalcPostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового Расчета."""
    structural_element_foundation = StructuralElementFoundationSerializer(
        required=True
    )
    structural_element_frame = FrameOpeningsSerializer(
        many=True,
        required=True
    )
    calculation = CalculationPostSerializer()

    class Meta:
        model = Calculation
        fields = ('structural_element_foundation',
                  'structural_element_frame', 'calculation')


class CalcUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для Update Расчета."""
    structural_element_foundation = StructuralElementFoundationSerializer(
        required=True)
    structural_element_frame = FrameOpeningsSerializer(many=True,
                                                       required=True)

    def validate(self, attrs):
        if 'structural_element_frame' in attrs.keys():
            frames = attrs['structural_element_frame']
            pk = self.context.get('view').kwargs.get('pk')
            calculation = Calculation.objects.get(pk=pk)
            for data in frames:
                floor = data['frame']['number_of_floors']
                try:
                    frame_unit = StructuralElementFrame.objects.get(
                        calculations=calculation,
                        number_of_floors=floor
                    )
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(
                        f'У этого расчета нет этажа {floor}'
                    )
        return attrs

    class Meta:
        model = Calculation
        fields = ('structural_element_foundation', 'structural_element_frame')


class CalculationSerializer(serializers.ModelSerializer):
    """Сериализатор для расчетов."""
    results = ResultSerializer(many=True)
    manager = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    customer = serializers.SlugRelatedField(
        slug_field='pk',
        queryset=Customers.objects.all(),
        required=True,
    )
    state_calculation = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Customers.objects.all(),
        required=True,
    )
    structural_element_foundation = StructuralElementFoundationSerializer(
        many=True)
    structural_element_frame = FrameSerializer(many=True)

    class Meta:
        model = Calculation
        fields = ('id', 'title', 'manager', 'customer',
                  'adress_object_construction', 'created_date',
                  'state_calculation', 'results',
                  'structural_element_foundation', 'structural_element_frame')
