from django.urls import path
from . import views


from .views import crear_solicitud, detalle_solicitud, lista_solicitudes

app_name = 'solicitudes'

urlpatterns = [
    path('', lista_solicitudes, name='lista'),
    path('crear/', crear_solicitud, name='crear'),
    path('<int:pk>/', detalle_solicitud, name='detalle'),
    path('<int:pk>/editar/', views.editar_solicitud, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_solicitud, name='eliminar'),
    path('<int:pk>/atenciones/crear/', views.crear_atencion, name='crear_atencion'),
    path('<int:pk>/atenciones/', views.historial_atenciones, name='historial_atenciones'),
    path('tipos/', views.lista_tipos, name='lista_tipos'),
    path('tipos/crear/', views.crear_tipo, name='crear_tipo'),
    path('tipos/editar/<int:pk>/', views.editar_tipo, name='editar_tipo'),
    path('tipos/eliminar/<int:pk>/', views.eliminar_tipo, name='eliminar_tipo'),
    path('vecinos/', views.lista_vecinos, name='lista_vecinos'),
    path('vecinos/crear/', views.crear_vecino, name='crear_vecino'),
    path('vecinos/editar/<int:pk>/', views.editar_vecino, name='editar_vecino'),
    path('vecinos/eliminar/<int:pk>/', views.eliminar_vecino, name='eliminar_vecino'),
    path('recuperar/', views.solicitar_codigo_view, name='solicitar_codigo'),
path('recuperar/verificar/', views.verificar_codigo_view, name='verificar_codigo'),
path('recuperar/nueva-clave/', views.nueva_contrasena_view, name='nueva_contrasena'),
]
