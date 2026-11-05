from django.urls import include, path
from usuarios import views as usuario_views


urlpatterns = [
    path('', usuario_views.dashboard, name='inicio'),
    path('dashboard/', usuario_views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('delegaciones/', include('delegaciones.urls')),
    path('solicitudes/', include('solicitudes.urls')),
]
