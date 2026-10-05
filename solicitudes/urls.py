from django.urls import path

from .views import crear_solicitud, detalle_solicitud, lista_solicitudes

app_name = 'solicitudes'

urlpatterns = [
    path('', lista_solicitudes, name='lista'),
    path('crear/', crear_solicitud, name='crear'),
    path('<int:pk>/', detalle_solicitud, name='detalle'),
]
