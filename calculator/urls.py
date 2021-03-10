from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

from . import views


router1 = SimpleRouter()
router2 = SimpleRouter()

router1.register(r'customers',
                 views.CustomersViewSet,
                 basename='customers')
# router2.register(r'customers/(?P<customers_id>\d+)/calculation',
#                  views.CalculationViewSet,
#                  basename='calculation')
# router2.register(r'customers/(?P<customers_id>\d+)/'
#                  r'calculation/(?P<calculation_id>\d+)/frame',
#                  views.StructuralElementFrameViewSet,
#                  basename='frame')
# router2.register(r'customers/(?P<customers_id>\d+)/'
#                  r'calculation/(?P<calculation_id>\d+)/'
#                  r'frame/(?P<frame_id>\d+)/openings',
#                  views.OpeningsViewSet,
#                  basename='openings')

urlpatterns = [
    path('', include(router1.urls)),
    path('', include(router2.urls)),

    path('materials/', MaterialsListView.as_view(), name='materials'),
    path('calculation/', CalculationListView.as_view(), name='calculation_list'),
    path('calculation/<int:pk>', CalculationDetailView.as_view(), name='calculation_detail'),
]