from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

from . import views


router1 = SimpleRouter()
router1.register(r'customers',
                 views.CustomersViewSet,
                 basename='customers')
router1.register(r'customers/(?P<customers_id>\d+)/calculation',
                 views.CalculationViewSet,
                 basename='calculation')
router1.register(r'customers/(?P<customers_id>\d+)/'
                 r'calculation/(?P<calculation_id>\d+)/frame',
                 views.StructuralElementFrameViewSet,
                 basename='frame')
router1.register(r'customers/(?P<customers_id>\d+)/'
                 r'calculation/(?P<calculation_id>\d+)/'
                 r'frame/(?P<frame_id>\d+)/openings',
                 views.OpeningsViewSet,
                 basename='openings')

urlpatterns = [
    path('', include(router1.urls)),

    path('materials/', MaterialsListView.as_view(), name='materials'),
]