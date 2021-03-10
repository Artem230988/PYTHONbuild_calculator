from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

from . import views

router = SimpleRouter()

router.register(r'customers',
                views.CustomersViewSet,
                basename='customers')
# router2.register(r'customers/(?P<customers_id>\d+)/calculation',
#                  views.CalculationViewSet,
#                  basename='calculation')
router.register(r'frame',
                views.StructuralElementFrameViewSet,
                basename='frame')
router.register(r'orderings',
                views.OpeningsViewSet,
                basename='orderings')

urlpatterns = [
    path('', include(router.urls)),

    path('materials/', MaterialsListView.as_view(), name='materials'),
    path('customers/<int:pk>/calculation/', CalculationListView.as_view(),
         name='calculation'),
]
