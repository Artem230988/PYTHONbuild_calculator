from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router1 = SimpleRouter()
router1.register(r'customers',
                 views.CustomersViewSet,
                 basename='customers')
router1.register(r'customers/(?P<customers_id>\d+)/calculation',
                 views.CalculationViewSet,
                 basename='calculation')

urlpatterns = [
    path('', include(router1.urls)),
]