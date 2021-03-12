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
router.register(r'frame-orderings',
                views.FrameOpeningsViewSet,
                basename='frameorderings')

urlpatterns = [
    path('', include(router.urls)),

    path('materials/', MaterialsListView.as_view(), name='materials'),
    path('calculation/', CalculationListView.as_view(), name='calculation_list'),
    path('calculation/<int:pk>', CalculationDetailView.as_view(), name='calculation_detail'),
]
