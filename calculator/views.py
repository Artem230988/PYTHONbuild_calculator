from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics, permissions
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


class MaterialsListView(generics.ListAPIView):
    """Список всех материалов"""
    queryset = SpecificMaterial.objects.all()
    serializer_class = SpecificMaterialSerializer
    # permission_classes = [permissions.IsAuthenticated, ]


class CalculationListView(generics.ListAPIView):
    """Список расчетов"""
    serializer_class = CalculationSerializer
    # permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Calculation.objects.filter(manager=self.request.user)


class CalculationDetailView(generics.ListAPIView):
    """Расчет детально"""
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
    # permission_classes = [permissions.IsAuthenticated, ]