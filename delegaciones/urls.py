from django.urls import path 
from . import views

app_name = 'delegaciones' 

urlpatterns = [ 
    path('', views.lista_delegaciones, 
        name='lista_delegaciones'), 
]