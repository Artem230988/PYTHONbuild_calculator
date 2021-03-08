from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
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


class CalculationViewSet(viewsets.ModelViewSet):
    """CRUD для расчетов."""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = CalculationSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customers_id']
        return Calculation.objects.filter(customer=customer_id)

    def perform_create(self, serializer, *args, **kwargs):
        customer_id = self.kwargs['customers_id']
        customer = get_object_or_404(Customers, id=customer_id)
        serializer.save(customer=customer)


class StructuralElementFrameViewSet(viewsets.ModelViewSet):
    """CRUD для конструктивного элемента каркас."""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = StructuralElementFrameSerializer

    def get_queryset(self):
        calculation = self.kwargs['calculation_id']
        return StructuralElementFrame.objects.filter(calculations=calculation)

    def perform_create(self, serializer, *args, **kwargs):
        calculation_id = self.kwargs['calculation_id']
        calculation = get_object_or_404(Calculation, id=calculation_id)
        serializer.save(calculations=calculation)


class OpeningsViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """CRUD для проемов."""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = OpeningsSerializer
    lookup_field = 'openings_id'

    def get_queryset(self):
        frame = self.kwargs['frame_id']
        queryset = FrameOpenings.objects.filter(
            structural_element_frame=frame,
        )
        print(queryset)
        list_q = []
        for i in queryset:
            list_q.append(i.openings)
        return queryset

    def get_object(self):
        openings = self.kwargs['openings_id']
        return get_object_or_404(Openings, pk=openings)

    def perform_create(self, serializer):
        frame = self.kwargs['frame_id']
        frame = get_object_or_404(StructuralElementFrame, pk=frame)
        opening = serializer.validated_data
        serializer.save()
        opening = Openings.objects.get(
            type=opening['type'],
            wigth=opening['wigth'],
            height=opening['height'],
            count=opening['count'],
        )
        frame_openings = FrameOpenings.objects.create(
            structural_element_frame=frame,
            openings=opening,
        )
        frame_openings.save()
