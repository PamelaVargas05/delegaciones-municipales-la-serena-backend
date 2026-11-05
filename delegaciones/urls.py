from django.urls import path
from . import views

app_name = 'delegaciones'

urlpatterns = [
    path('', views.lista_delegaciones, name='lista_delegaciones'),
    path('crear/', views.crear_delegacion, name='crear_delegacion'),
    path('editar/<int:pk>/', views.editar_delegacion, name='editar_delegacion'),
    path('eliminar/<int:pk>/', views.eliminar_delegacion, name='eliminar_delegacion'),
    path('metas/', views.lista_metas, name='lista_metas'),
    path('metas/crear/', views.crear_meta, name='crear_meta'),
    path('metas/editar/<int:pk>/', views.editar_meta, name='editar_meta'),
    path('metas/eliminar/<int:pk>/', views.eliminar_meta, name='eliminar_meta'),
]