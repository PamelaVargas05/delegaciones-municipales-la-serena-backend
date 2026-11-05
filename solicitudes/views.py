from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from delegaciones.models import Delegacion
from .forms import AtencionSolicitudForm, SolicitudVecinalForm, TipoSolicitudForm
from .models import AtencionSolicitud, CodigoRecuperacion, SolicitudVecinal, TipoSolicitud
from .models import Vecino
from .forms import VecinoForm



@login_required
@permission_required(
    'solicitudes.view_solicitudvecinal', raise_exception=True
)
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


@login_required
@permission_required(
    'solicitudes.view_solicitudvecinal', raise_exception=True
)
def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(
        SolicitudVecinal.objects.select_related('delegacion'), pk=pk
    )
    return render(
        request, 'solicitudes/solicitud_detail.html', {'solicitud': solicitud}
    )


@login_required
@permission_required('solicitudes.add_solicitudvecinal', raise_exception=True)
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudVecinalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud registrada correctamente.')
            return redirect('solicitudes:lista')
    else:
        form = SolicitudVecinalForm()
    return render(request, 'solicitudes/solicitud_form.html', {'form': form})


@login_required
@permission_required('solicitudes.change_solicitudvecinal', raise_exception=True)
def editar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudVecinal, pk=pk)
    form = SolicitudVecinalForm(request.POST or None, instance=solicitud)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Solicitud actualizada correctamente.')
        return redirect('solicitudes:detalle', pk=pk)
    return render(request, 'solicitudes/solicitud_form.html', {'form': form})


@login_required
@permission_required('solicitudes.delete_solicitudvecinal', raise_exception=True)
def eliminar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudVecinal, pk=pk)
    if request.method == 'POST':
        solicitud.delete()
        messages.success(request, 'Solicitud eliminada correctamente.')
        return redirect('solicitudes:lista')
    return render(request, 'solicitudes/solicitud_confirm_delete.html', {'solicitud': solicitud})


@login_required
@permission_required('solicitudes.add_atencionsolicitud', raise_exception=True)
def crear_atencion(request, pk):
    solicitud = get_object_or_404(SolicitudVecinal, pk=pk)
    form = AtencionSolicitudForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        atencion = form.save(commit=False)
        atencion.solicitud = solicitud
        atencion.usuario = request.user
        atencion.save()
        solicitud.estado = atencion.estado
        solicitud.save(update_fields=['estado'])
        messages.success(request, 'Atención registrada correctamente.')
        return redirect('solicitudes:detalle', pk=pk)
    return render(request, 'solicitudes/atencion_form.html', {'form': form, 'solicitud': solicitud})


@login_required
@permission_required('solicitudes.view_atencionsolicitud', raise_exception=True)
def historial_atenciones(request, pk):
    solicitud = get_object_or_404(SolicitudVecinal, pk=pk)
    return render(request, 'solicitudes/atencion_list.html', {
        'solicitud': solicitud,
        'atenciones': solicitud.atenciones.select_related('usuario'),
    })


@login_required
@permission_required('solicitudes.view_tiposolicitud', raise_exception=True)
def lista_tipos(request):
    query = request.GET.get('q', '')
    tipos = TipoSolicitud.objects.all()
    if query:
        tipos = tipos.filter(nombre__icontains=query)
    return render(request, 'solicitudes/tipo_list.html', {'tipos': tipos, 'query': query})


@login_required
@permission_required('solicitudes.add_tiposolicitud', raise_exception=True)
def crear_tipo(request):
    form = TipoSolicitudForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('solicitudes:lista_tipos')
    return render(request, 'solicitudes/tipo_form.html', {'form': form, 'titulo': 'Nuevo tipo de solicitud'})


@login_required
@permission_required('solicitudes.change_tiposolicitud', raise_exception=True)
def editar_tipo(request, pk):
    tipo = get_object_or_404(TipoSolicitud, pk=pk)
    form = TipoSolicitudForm(request.POST or None, instance=tipo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('solicitudes:lista_tipos')
    return render(request, 'solicitudes/tipo_form.html', {'form': form, 'titulo': 'Editar tipo de solicitud'})


@login_required
@permission_required('solicitudes.delete_tiposolicitud', raise_exception=True)
def eliminar_tipo(request, pk):
    tipo = get_object_or_404(TipoSolicitud, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        return redirect('solicitudes:lista_tipos')
    return render(request, 'solicitudes/tipo_confirm_delete.html', {'tipo': tipo})




def solicitar_codigo_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            codigo_obj = CodigoRecuperacion.generar_codigo(user)
            asunto = 'Código de recuperación - Delegaciones Municipales'
            enlace = request.build_absolute_uri('/solicitudes/recuperar/verificar/')
            mensaje = (
                f'Hola {user.username},\n\n'
                f'Tu código de verificación es:\n\n{codigo_obj.codigo}\n\n'
                'Este código es válido durante 15 minutos.\n\n'
                f'Para continuar con la recuperación puedes ingresar aquí:\n{enlace}\n\n'
                'Si no solicitaste este cambio, ignora este mensaje.'
            )
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            request.session['email_recuperacion'] = user.email
        messages.success(
            request,
            'Si el correo está asociado a una cuenta activa, recibirás un código de verificación.',
        )
        if user:
            return redirect('solicitudes:verificar_codigo')
    return render(request, 'registration/solicitar_codigo.html')


def verificar_codigo_view(request):
    email = request.session.get('email_recuperacion')
    if not email:
        return redirect('solicitudes:solicitar_codigo')

    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip()
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user and len(codigo_ingresado) == 6 and codigo_ingresado.isdigit():
            ultimo_codigo = CodigoRecuperacion.objects.filter(
                user=user
            ).order_by('-creado_en').first()
            if ultimo_codigo and ultimo_codigo.codigo == codigo_ingresado and ultimo_codigo.es_valido():
                request.session['codigo_verificado'] = True
                return redirect('solicitudes:nueva_contrasena')
        messages.error(request, 'Código incorrecto o expirado.')

    return render(
        request, 'registration/verificar_codigo.html', {'email': email}
    )


def nueva_contrasena_view(request):
    email = request.session.get('email_recuperacion')
    verificado = request.session.get('codigo_verificado')

    if not email or not verificado:
        return redirect('solicitudes:solicitar_codigo')

    if request.method == 'POST':
        pass1 = request.POST.get('password1', '')
        pass2 = request.POST.get('password2', '')

        if len(pass1) < 8:
            messages.error(
                request, 'La contraseña debe tener al menos 8 caracteres.'
            )
        elif pass1 != pass2:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            user = User.objects.filter(email__iexact=email, is_active=True).first()
            if not user:
                messages.error(request, 'No fue posible completar la recuperación.')
                return redirect('solicitudes:solicitar_codigo')
            user.set_password(pass1)
            user.save()
            CodigoRecuperacion.objects.filter(user=user).delete()
            request.session.pop('email_recuperacion', None)
            request.session.pop('codigo_verificado', None)
            messages.success(
                request,
                '¡Contraseña actualizada con éxito! Ya puedes iniciar sesión.',
            )
            return redirect('login')

    return render(request, 'registration/nueva_contrasena.html')


@login_required
@permission_required('solicitudes.view_vecino', raise_exception=True)
def lista_vecinos(request):
    query = request.GET.get('q', '')
    if query:
        vecinos = Vecino.objects.filter(Q(rut__icontains=query) | Q(nombre__icontains=query))
    else:
        vecinos = Vecino.objects.all()
    return render(request, 'solicitudes/vecinos_list.html', {'vecinos': vecinos, 'query': query})

@login_required
@permission_required('solicitudes.add_vecino', raise_exception=True)
def crear_vecino(request):
    if request.method == 'POST':
        form = VecinoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vecino registrado exitosamente.')
            return redirect('solicitudes:lista_vecinos')
    else:
        form = VecinoForm()
    return render(request, 'solicitudes/vecino_form.html', {'form': form, 'titulo': 'Registrar Vecino'})

@login_required
@permission_required('solicitudes.change_vecino', raise_exception=True)
def editar_vecino(request, pk):
    vecino = get_object_or_404(Vecino, pk=pk)
    if request.method == 'POST':
        form = VecinoForm(request.POST, instance=vecino)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del vecino actualizados.')
            return redirect('solicitudes:lista_vecinos')
    else:
        form = VecinoForm(instance=vecino)
    return render(request, 'solicitudes/vecino_form.html', {'form': form, 'titulo': 'Editar Vecino'})

@login_required
@permission_required('solicitudes.delete_vecino', raise_exception=True)
def eliminar_vecino(request, pk):
    vecino = get_object_or_404(Vecino, pk=pk)
    if request.method == 'POST':
        vecino.delete()
        messages.success(request, 'Vecino eliminado de la base de datos.')
        return redirect('solicitudes:lista_vecinos')
    return render(request, 'solicitudes/vecino_confirm_delete.html', {'vecino': vecino})