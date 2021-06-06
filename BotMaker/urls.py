from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('api.urls')),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]
