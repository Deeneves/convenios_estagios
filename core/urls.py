from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('academico/', include('apps.academico.urls')),
    path('contrapartida/', include('apps.contrapartida.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
]
