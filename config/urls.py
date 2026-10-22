"""
URLs principais do projeto.

Cada app tem seu próprio urls.py e aqui só "plugamos" eles com include().
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('api/', include('apps.autores.urls')),
    path('api/', include('apps.livros.urls')),
]
