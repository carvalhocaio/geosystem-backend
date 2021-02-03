from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agricola/', include('agricola.urls')),
    path('ambiental/', include('ambiental.urls')),
    path('geosystem/', include('geosystem.urls'))
]
