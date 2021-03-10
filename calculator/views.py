from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics, permissions
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


# class CalculationViewSet(viewsets.ModelViewSet):
#     """CRUD для расчетов."""
#     http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
#     serializer_class = CalculationSerializer
#
#     def get_queryset(self):
#         customer_id = self.kwargs['customers_id']
#         return Calculation.objects.filter(customer=customer_id)
#
#     def perform_create(self, serializer, *args, **kwargs):
#         customer_id = self.kwargs['customers_id']
#         customer = get_object_or_404(Customers, id=customer_id)
#         serializer.save(customer=customer)
#
#
class StructuralElementFrameViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """CRUD для конструктивного элемента каркас."""
    queryset = StructuralElementFrame.objects.all()
    serializer_class = StructuralElementFrameSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return StructuralElementFrameSerializer
        return StructuralElementFramePostSerializer

    def perform_create(self, serializer):
        serializer.save()
        frame = StructuralElementFrame.objects.all()
        calculate_frame(frame[len(frame)-1])

    def perform_update(self, serializer):
        frame = self.get_object()
        serializer.save()
        calculate_frame(frame)


class OpeningsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Openings.objects.all()
    serializer_class = OpeningsSerializer


#   def get_queryset(self):
#       frame = self.kwargs['frame_id']
#       queryset = FrameOpenings.objects.filter(
#           structural_element_frame=frame,
#       )
#       list_q = []
#       for i in queryset:
#           list_q.append(i.openings)
#       return list_q
#
#   def get_object(self):
#       openings = self.kwargs['openings_id']
#       return get_object_or_404(Openings, pk=openings)
#
#   def perform_create(self, serializer):
#       frame = self.kwargs['frame_id']
#       frame = get_object_or_404(StructuralElementFrame, pk=frame)
#       opening = serializer.validated_data
#       serializer.save()
#       opening = Openings.objects.get(
#           type=opening['type'],
#           wigth=opening['wigth'],
#           height=opening['height'],
#           count=opening['count'],
#       )
#       frame_openings = FrameOpenings.objects.create(
#           structural_element_frame=frame,
#           openings=opening,
#       )
#       frame_openings.save()


class MaterialsListView(generics.ListAPIView):
    queryset = Materials.objects.all()
    serializer_class = SpecificMaterialsSerializer
    # permission_classes = [permissions.IsAuthenticated, ]


class CalculationListView(generics.ListAPIView):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
    # permission_classes = [permissions.IsAuthenticated, ]
