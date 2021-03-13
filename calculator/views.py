from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet

from .calculate_frame import calculate_frame
from .serializers import *
from .models import *


class CustomersViewSet(viewsets.ModelViewSet):
    """CRUD для заказчиков."""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = CustomersSerializer

    def get_queryset(self):
        manager = self.request.user.id
        return Customers.objects.filter(manager=manager)

    def perform_create(self, serializer, *args, **kwargs):
        manager = self.request.user
        serializer.save(manager=manager)


class FrameOpeningsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = FrameOpening.objects.all()
    serializer_class = FrameOpeningsSerializer

    def perform_create(self, serializer):
        openings = serializer.validated_data['opening']
        frame = StructuralElementFrameSerializer(data=serializer.validated_data['frame'])
        frame.is_valid()
        frame.save()
        frames = StructuralElementFrame.objects.all()
        last_frame = frames[len(frames)-1]
        for opening in openings:
            opening = OpeningsSerializer(data=opening)
            opening.is_valid()
            opening.save(frame=last_frame)
        calculate_frame(last_frame)


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
