from django.urls import path, include
from .views import UserDetailView


urlpatterns = [
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('myprofile/', UserDetailView.as_view(), name='myprofile'),
]