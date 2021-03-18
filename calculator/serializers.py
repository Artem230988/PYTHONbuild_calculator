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
        fields = ('id', 'last_name', 'first_name', 'second_name',
                  'phone', 'email', 'adress', 'manager', )


class SpecificMaterialSerializer(serializers.ModelSerializer):
    """Сериализатор для конкретного материала."""
    material = serializers.CharField(source='material.name')
    measurement_unit = serializers.CharField(source='measurement_unit.measurement_unit')

    class Meta:
        model = SpecificMaterial
        fields = ('id', 'material', 'measurement_unit', 'name')


class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для результатов по каждому материалу"""
    specific_material = SpecificMaterialSerializer()

    class Meta:
        model = Result
        fields = ('name', 'specific_material', 'amount',
                  'price', 'full_price')


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
        fields = ('id', 'title', 'manager', 'customer',
                  'adress_object_construction', 'created_date',
                  'state_calculation', 'results')


class OpeningsSerializer(serializers.ModelSerializer):
    """Сериализатор для проемов."""

    class Meta:
        model = Opening
        fields = ('type', 'wigth', 'height', 'count')


class StructuralElementFrameSerializer(serializers.ModelSerializer):
    """Сериализатор для рассчетов."""
    step_of_racks = serializers.DecimalField(max_digits=10, decimal_places=2,
                                             default=0.6)

    class Meta:
        model = StructuralElementFrame
        exclude = ('calculations',)


class FrameOpeningsSerializer(serializers.Serializer):
    frame = StructuralElementFrameSerializer()
    opening = OpeningsSerializer(many=True)


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
    manager = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Calculation
        fields = '__all__'


class FrameSerializer(serializers.Serializer):
    frames = FrameOpeningsSerializer(many=True)
    calculation = CalculationPostSerializer()


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


class OpeningsPatchSerializer(serializers.ModelSerializer):
    """Сериализатор для проемов."""

    class Meta:
        model = Opening
        fields = ('type', 'wigth', 'height', 'count')


class StructuralElementFramePatchSerializer(serializers.ModelSerializer):
    """Сериализатор для рассчетов."""
    id = serializers.SlugRelatedField(
        slug_field='pk',
        queryset=StructuralElementFrame.objects.all(),
        required=True,
    )
    step_of_racks = serializers.DecimalField(max_digits=10, decimal_places=2,
                                             default=0.6)

    class Meta:
        model = StructuralElementFrame
        exclude = ('calculations',)


class FrameOpeningsPatchSerializer(serializers.ModelSerializer):
    frame = StructuralElementFramePatchSerializer()
    opening = OpeningsPatchSerializer(many=True)

    class Meta:
        model = FrameOpening
        fields = ('frame', 'opening')


class FramePatchSerializer(serializers.Serializer):
    frames = FrameOpeningsPatchSerializer(many=True)

    def validate(self, attrs):
        frames = attrs['frames']
        pk = self.context.get('view').kwargs.get('pk')
        calculation = Calculation.objects.get(pk=pk)
        for data in frames:
            frame = data['frame']['id']
            if frame.calculations != calculation:
                raise serializers.ValidationError(
                    'Данный каркас принадлежит другому расчету'
                )
        return attrs
