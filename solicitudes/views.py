from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from delegaciones.models import Delegacion
from .forms import SolicitudVecinalForm
from .models import CodigoRecuperacion, SolicitudVecinal



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




def solicitar_codigo_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            codigo_obj = CodigoRecuperacion.generar_codigo(user)
            asunto = 'Código de Verificación - Recuperación de Contraseña'
            mensaje = (
                f'Hola {user.username},\n\n'
                f'Tu código de verificación para cambiar la contraseña es: {codigo_obj.codigo}\n\n'
                f'Este código vencerá en 15 minutos.'
            )
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            request.session['email_recuperacion'] = user.email
            messages.success(
                request, f'Se ha enviado un código de 6 dígitos a {user.email}'
            )
            return redirect('solicitudes:verificar_codigo')
        except User.DoesNotExist:
            messages.error(
                request,
                'No existe ninguna cuenta asociada a este correo electrónico.',
            )
    return render(request, 'registration/solicitar_codigo.html')


def verificar_codigo_view(request):
    email = request.session.get('email_recuperacion')
    if not email:
        return redirect('solicitudes:solicitar_codigo')

    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip()
        try:
            user = User.objects.get(email=email)
            ultimo_codigo = CodigoRecuperacion.objects.filter(
                user=user
            ).latest('creado_en')
            if (
                ultimo_codigo.codigo == codigo_ingresado
                and ultimo_codigo.es_valido()
            ):
                request.session['codigo_verificado'] = True
                return redirect('solicitudes:nueva_contrasena')
            else:
                messages.error(
                    request,
                    'El código es incorrecto o ha expirado (dura 15 min).',
                )
        except (User.DoesNotExist, CodigoRecuperacion.DoesNotExist):
            messages.error(
                request, 'Ocurrió un error. Solicita un nuevo código.'
            )

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
            user = User.objects.get(email=email)
            user.set_password(pass1)
            user.save()
            del request.session['email_recuperacion']
            del request.session['codigo_verificado']
            messages.success(
                request,
                '¡Contraseña actualizada con éxito! Ya puedes iniciar sesión.',
            )
            return redirect('login')

    return render(request, 'registration/nueva_contrasena.html')