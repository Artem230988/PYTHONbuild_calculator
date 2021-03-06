from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


router1 = SimpleRouter()
router1.register(r'customers', views.CustomersViewSet, basename='customers')

urlpatterns = router1.urls
