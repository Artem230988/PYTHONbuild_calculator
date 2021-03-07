from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router1 = SimpleRouter()
router1.register(r'customers', views.CustomersViewSet, basename='customers')

urlpatterns = [
    path('v1/', include(router1.urls)),
]