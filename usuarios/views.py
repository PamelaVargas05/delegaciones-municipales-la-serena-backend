from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from delegaciones.models import Delegacion
from solicitudes.models import SolicitudVecinal
from .forms import UsuarioForm


@login_required
def dashboard(request):
    if request.user.is_superuser:
        rol = 'Administrador'
    else:
        nombres_roles = ('Administrador', 'Supervisor', 'Administrativo')
        rol = (
            request.user.groups.filter(name__in=nombres_roles)
            .order_by('name')
            .values_list('name', flat=True)
            .first()
            or 'Administrativo'
        )
    context = {
        'rol': rol,
        'nombre_usuario': request.user.get_full_name() or request.user.username,
        'delegaciones_count': Delegacion.objects.count(),
        'solicitudes_count': SolicitudVecinal.objects.count(),
        'pendientes_count': SolicitudVecinal.objects.filter(
            estado=SolicitudVecinal.Estado.PENDIENTE
        ).count(),
    }
    return render(request, 'usuarios/dashboard.html', context)


@login_required
@permission_required('auth.view_user', raise_exception=True)
def lista_usuarios(request):
    usuarios = User.objects.prefetch_related('groups').annotate(group_count=Count('groups'))
    query = request.GET.get('q', '')
    if query:
        usuarios = usuarios.filter(username__icontains=query)
    return render(request, 'usuarios/usuario_list.html', {'usuarios': usuarios, 'query': query})


@login_required
@permission_required('auth.add_user', raise_exception=True)
def crear_usuario(request):
    form = UsuarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Nuevo usuario'})


@login_required
@permission_required('auth.change_user', raise_exception=True)
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Editar usuario'})


@login_required
@permission_required('auth.delete_user', raise_exception=True)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})
