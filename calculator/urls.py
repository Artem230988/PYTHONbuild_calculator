from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

from . import views

router = SimpleRouter()

router.register(r'customers',
                views.CustomersViewSet,
                basename='customers')
router.register(r'calculation_frame',
                views.FrameOpeningsViewSet,
                basename='frameorderings')
router.register(r'calculation_frame',
                views.FrameOpeningsPatchViewSet,
                basename='frameorderings')
router.register(r'calc_post',
                views.CalcPostViewSet,
                basename='calculation_post')

urlpatterns = [
    path('', include(router.urls)),

    path('calculation_foundation/',
         StructuralElementFoundationCreate.as_view(),
         name='calculation_foundation_create'),
    path('calculation_foundation/<int:pk>',
         StructuralElementFoundationUpdate.as_view(),
         name='calculation_foundation_update'),

    path('calc_update/<int:pk>', CalcUpdate.as_view(),
         name='calculation_patch'),

    path('materials/', MaterialsListView.as_view(), name='materials'),
    path('calculation/', CalculationListView.as_view(),
         name='calculation_list'),
    path('calculation/<int:pk>', CalculationDetailView.as_view(),
         name='calculation_detail'),
    path('calculation/update_state/<int:pk>',
         CalculationStateUpdateView.as_view(),
         name='calculation_state_update'),
]
