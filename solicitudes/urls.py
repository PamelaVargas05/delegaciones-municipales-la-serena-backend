from django.urls import path
from . import views


from .views import crear_solicitud, detalle_solicitud, lista_solicitudes

app_name = 'solicitudes'

urlpatterns = [
    path('', lista_solicitudes, name='lista'),
    path('crear/', crear_solicitud, name='crear'),
    path('<int:pk>/', detalle_solicitud, name='detalle'),
    path('recuperar/', views.solicitar_codigo_view, name='solicitar_codigo'),
path('recuperar/verificar/', views.verificar_codigo_view, name='verificar_codigo'),
path('recuperar/nueva-clave/', views.nueva_contrasena_view, name='nueva_contrasena'),
]
