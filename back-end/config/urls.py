from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/', include('modules.authentication.presentation.urls')),
    path('api/v1/', include('modules.fuel.presentation.urls')),   
    path('api/v2/', include('modules.fuelv2.presentation.urls')),   
    path('api/v2/', include('modules.dashboard.presentation.urls')),   
    
]
