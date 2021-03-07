from rest_framework import viewsets
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
