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
    queryset = FrameOpening.objects.all()
    serializer_class = FrameSerializer
    permission_classes = (permissions.IsAuthenticated, )

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
        frames = serializer.validated_data['frames']
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


class FrameOpeningsPatchViewSet(mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    queryset = FrameOpening.objects.all()
    serializer_class = FramePatchSerializer
    http_method_names = ('patch', )
    permission_classes = (permissions.IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def perform_update(self, serializer):
        frames = serializer.validated_data['frames']
        for data in frames:
            frame_id = data['frame']['id']
            openings = data['opening']
            frame = StructuralElementFrameSerializer(
                instance=frame_id,
                data=data['frame']
            )
            frame.is_valid()
            frame.save()
            for opening in openings:
                opening_id = Opening.objects.get(type=opening['type'],
                                                 frame=frame_id)
                opening = OpeningsSerializer(instance=opening_id,
                                             data=opening)
                opening.is_valid()
                opening.save()
            # calculate_frame(frame_id)


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


class CalculationDetailView(generics.RetrieveAPIView):
    """Расчет детально"""
    serializer_class = CalculationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)


class CalculationStateUpdateView(generics.UpdateAPIView):
    http_method_names = ('patch', )
    serializer_class = CalculationStateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)
