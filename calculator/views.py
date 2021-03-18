from django.shortcuts import redirect
from rest_framework import viewsets, mixins, generics, permissions

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
    queryset = FrameOpening.objects.all()
    serializer_class = FrameSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = self.perform_create(serializer)
        return redirect('calculation_detail', pk=id)

    def perform_create(self, serializer):
        customer = serializer.validated_data['calculation']['customer']
        state_calculation = serializer.validated_data['calculation']['state_calculation']
        title = serializer.validated_data['calculation']['title']
        adress_object_construction = serializer.validated_data['calculation']['adress_object_construction']
        calculation = Calculation.objects.create(
            customer=customer,
            state_calculation=state_calculation,
            title=title,
            adress_object_construction=adress_object_construction,
            manager=self.request.user
        )
        frames = serializer.validated_data['frame']
        for data in frames:
            openings = data['opening']
            frame = StructuralElementFrameSerializer(
                data=data['frame']
            )
            frame.is_valid()
            frame.save(calculations=calculation)
            frames = StructuralElementFrame.objects.all()
            last_frame = frames[len(frames)-1]
            for opening in openings:
                opening = OpeningsSerializer(data=opening)
                opening.is_valid()
                opening.save(frame=last_frame)
            calculate_frame(last_frame)
        return calculation.id


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
    http_method_names = ['patch', ]
    serializer_class = CalculationStateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)
