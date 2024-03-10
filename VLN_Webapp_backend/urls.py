from django.contrib import admin
from django.urls import path, include
from hospital import urls
from home import urls

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('hospital/', include('hospital.urls')),
]
