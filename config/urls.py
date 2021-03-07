from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('calculator.urls')),
    path('api/', include('profiles.urls')),

]

urlpatterns += doc_urls