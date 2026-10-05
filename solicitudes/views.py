from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from delegaciones.models import Delegacion

from .forms import SolicitudVecinalForm
from .models import SolicitudVecinal


def lista_solicitudes(request):
    delegacion_id = request.GET.get('delegacion')
    query = request.GET.get('q')

    solicitudes = SolicitudVecinal.objects.select_related('delegacion').all()

    if delegacion_id:
        solicitudes = solicitudes.filter(delegacion_id=delegacion_id)

    if query:
        solicitudes = solicitudes.filter(
            Q(folio__icontains=query)
            | Q(rut__icontains=query)
            | Q(nombre_ciudadano__icontains=query)
        )

    delegaciones = Delegacion.objects.all().order_by('nombre')
    return render(
        request,
        'solicitudes/solicitudes_list.html',
        {
            'solicitudes': solicitudes,
            'delegaciones': delegaciones,
            'delegacion_id': delegacion_id,
            'q': query or '',
        },
    )


def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudVecinal.objects.select_related('delegacion'), pk=pk)
    return render(request, 'solicitudes/solicitud_detail.html', {'solicitud': solicitud})


def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudVecinalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('solicitudes:lista')
    else:
        form = SolicitudVecinalForm()

    return render(request, 'solicitudes/solicitud_form.html', {'form': form})

