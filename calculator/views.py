from django.http import Http404
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
        customers_id = self.kwargs['customers_id']
        return Calculation.objects.filter(customer=customers_id)


class StructuralElementFrameViewSet(viewsets.ModelViewSet):
    """CRUD для конструктивного элемента каркас."""
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = StructuralElementFrameSerializer

    def get_queryset(self):
        calculation = self.kwargs['calculation_id']
        return StructuralElementFrame.objects.filter(calculations=calculation)


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
        try:
            return Openings.objects.get(pk=openings)
        except Openings.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        frame = self.kwargs['frame_id']
        frame = StructuralElementFrame.objects.get(pk=frame)
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
