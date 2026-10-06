from django.shortcuts import render
from .models import Delegacion 

def lista_delegaciones(request):
    """ 
    Vista pública para consultar y listar las 
delegaciones municipales utilizando Django ORM. """ 

    # Consulta ORM a MariaDB 
    delegaciones = Delegacion.objects.all() 

    context = { 'delegaciones': delegaciones 
    } 
    return render(request, 
'delegaciones/lista_delegaciones.html', context)