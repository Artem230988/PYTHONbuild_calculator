from django.shortcuts import redirect
from rest_framework import viewsets, mixins, generics, permissions, status
from rest_framework.response import Response

from .calculate_frame import calculate_frame
from .serializers import *
from .models import *


class CustomersViewSet(viewsets.ModelViewSet):
    """CRUD для заказчиков."""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = CustomersSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        manager = self.request.user.id
        return Customers.objects.filter(manager=manager)

    def perform_create(self, serializer, *args, **kwargs):
        manager = self.request.user
        serializer.save(manager=manager)


class FrameOpeningsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = StructuralElementFrame.objects.all()
    serializer_class = FrameSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = self.perform_create(serializer)
        return redirect('calculation_detail', pk=id)

    def perform_create(self, serializer):
        calculation_data = serializer.validated_data['calculation']
        calculation = Calculation.objects.create(**calculation_data)
        frames = serializer.validated_data['frames']
        for data in frames:
            openings = data['openings']
            frame = StructuralElementFrameSerializer(
                data=data['frame']
            )
            frame.is_valid()
            frame.save(calculations=calculation)
            frames = StructuralElementFrame.objects.all()
            last_frame = frames[len(frames) - 1]
            for opening in openings:
                opening = OpeningsSerializer(data=opening)
                opening.is_valid()
                opening.save(frame=last_frame)
            calculate_frame(last_frame)
        return calculation.id


class FrameOpeningsPatchViewSet(mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    queryset = FrameOpening.objects.all()
    serializer_class = FramePatchSerializer
    http_method_names = ('patch',)
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        pk = self.kwargs['pk']
        return redirect('calculation_state_update', pk=pk)

    def perform_update(self, serializer):
        frames = serializer.validated_data['frames']
        for data in frames:
            frame_id = data['frame']['id']
            frame = StructuralElementFrameSerializer(
                instance=frame_id,
                data=data['frame'],
                partial=True
            )
            frame.is_valid()
            frame.save()
            if 'opening' in data.keys():
                openings = data['opening']
                for opening in openings:
                    opening_id = Opening.objects.get(
                        type=opening['type'],
                        frame=frame_id
                    )
                    opening = OpeningsSerializer(
                        instance=opening_id,
                        data=opening
                    )
                    opening.is_valid()
                    opening.save()
            calculate_frame(frame_id)


class MaterialsListView(generics.ListAPIView):
    """Список всех материалов"""
    queryset = SpecificMaterial.objects.all()
    serializer_class = SpecificMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class CalculationListView(generics.ListAPIView):
    """Список расчетов"""
    serializer_class = CalculationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)


class CalculationDetailView(generics.RetrieveDestroyAPIView):
    """Расчет детально"""
    serializer_class = CalculationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)


class CalculationStateUpdateView(generics.UpdateAPIView):
    """Обновление статуса расчета"""
    http_method_names = ('patch', )
    serializer_class = CalculationStateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)


class StructuralElementFoundationCreate(generics.CreateAPIView):
    """Создание элемента фундамента"""
    queryset = StructuralElementFoundation.objects.all()
    serializer_class = StructuralElementFoundationSerializer

    def perform_create(self, serializer, *args, **kwargs):
        data = serializer.validated_data['calculation']
        calculation = Calculation.objects.create(**data)
        calculate_foundation(serializer.validated_data, calculation.id)
        serializer.save(calculation=calculation)
        return calculation.id

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = self.perform_create(serializer)
        return redirect('calculation_detail', pk=id)


class StructuralElementFoundationUpdate(generics.UpdateAPIView):
    """Создание элемента фундамента"""
    queryset = Calculation.objects.all()
    serializer_class = CalcUpdateSerializer

    def perform_update(self, serializer, *args, **kwargs):
        obj = StructuralElementFoundation.objects.get(pk=self.kwargs['pk'])
        serializer.save()


class CalcPostViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание любого расчета."""
    queryset = Calculation.objects.all()
    serializer_class = CalcPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = self.perform_create(serializer)
        return redirect('calculation_detail', pk=id)

    def perform_create(self, serializer):
        calculation_data = serializer.validated_data['calculation']
        calculation = Calculation.objects.create(**calculation_data)
        keys = serializer.validated_data.keys()
        if 'structural_element_foundation' in keys:
            foundation_data = serializer.validated_data['structural_element_foundation']
            foundation = StructuralElementFoundationSerializer(
                data=foundation_data
            )
            foundation.is_valid()
            print(foundation.validated_data)
            calculate_foundation(foundation.validated_data, calculation.id)
            foundation.save(calculation=calculation)
        if 'structural_element_frame' in keys:
            frames = serializer.validated_data['structural_element_frame']
            for data in frames:
                openings = data['openings']
                frame = StructuralElementFrameSerializer(
                    data=data['frame']
                )
                frame.is_valid()
                frame.save(calculations=calculation)
                frames = StructuralElementFrame.objects.all()
                last_frame = frames[len(frames) - 1]
                for opening in openings:
                    opening = OpeningsSerializer(data=opening)
                    opening.is_valid()
                    opening.save(frame=last_frame)
                calculate_frame(last_frame)
        return calculation.id


class CalcUpdate(generics.UpdateAPIView):
    """Обновление любого расчета."""
    http_method_names = ['patch', ]
    queryset = Calculation.objects.all()
    serializer_class = CalcUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        pk = self.kwargs['pk']
        return redirect('calculation_state_update', pk=pk)

    def perform_update(self, serializer):
        keys = serializer.validated_data.keys()
        pk = self.kwargs['pk']
        calculate = Calculation.objects.get(pk=pk)
        if 'structural_element_foundation' in keys:
            print("Артем")
        if 'structural_element_frame' in keys:
            frames = serializer.validated_data['structural_element_frame']
            for data in frames:
                floor = data['frame']['number_of_floors']
                frame_unit = StructuralElementFrame.objects.get(
                    calculations=calculate,
                    number_of_floors=floor
                )
                frame = StructuralElementFrameSerializer(
                    instance=frame_unit,
                    data=data['frame'],
                    partial=True
                )
                frame.is_valid()
                frame.save()
                if 'opening' in data.keys():
                    openings = data['opening']
                    for opening in openings:
                        opening_id = Opening.objects.get(
                            type=opening['type'],
                            frame=frame_unit
                        )
                        opening = OpeningsSerializer(
                            instance=opening_id,
                            data=opening
                        )
                        opening.is_valid()
                        opening.save()
                calculate_frame(frame_unit)
