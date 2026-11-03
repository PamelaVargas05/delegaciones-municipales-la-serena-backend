from django.urls import path
from . import views

app_name = 'delegaciones'

urlpatterns = [
    path('', views.lista_delegaciones, name='lista_delegaciones'),
    path('crear/', views.crear_delegacion, name='crear_delegacion'),
    path('editar/<int:pk>/', views.editar_delegacion, name='editar_delegacion'),
    path('eliminar/<int:pk>/', views.eliminar_delegacion, name='eliminar_delegacion'),
]