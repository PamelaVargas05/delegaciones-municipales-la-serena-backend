from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Delegacion, Meta
from .forms import DelegacionForm, MetaForm

@login_required
@permission_required('delegaciones.view_delegacion', raise_exception=True)
def lista_delegaciones(request):
    query = request.GET.get('q', '')
    if query:
        delegaciones = Delegacion.objects.filter(nombre__icontains=query)
    else:
        delegaciones = Delegacion.objects.all()
    return render(request, 'delegaciones/lista_delegaciones.html', {'delegaciones': delegaciones, 'query': query})

@login_required
@permission_required('delegaciones.add_delegacion', raise_exception=True)
def crear_delegacion(request):
    if request.method == 'POST':
        form = DelegacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delegación creada correctamente.')
            return redirect('delegaciones:lista_delegaciones')
    else:
        form = DelegacionForm()
    return render(request, 'delegaciones/delegacion_form.html', {'form': form, 'titulo': 'Nueva Delegación'})

@login_required
@permission_required('delegaciones.change_delegacion', raise_exception=True)
def editar_delegacion(request, pk):
    delegacion = get_object_or_404(Delegacion, pk=pk)
    if request.method == 'POST':
        form = DelegacionForm(request.POST, instance=delegacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delegación actualizada correctamente.')
            return redirect('delegaciones:lista_delegaciones')
    else:
        form = DelegacionForm(instance=delegacion)
    return render(request, 'delegaciones/delegacion_form.html', {'form': form, 'titulo': 'Editar Delegación'})

@login_required
@permission_required('delegaciones.delete_delegacion', raise_exception=True)
def eliminar_delegacion(request, pk):
    delegacion = get_object_or_404(Delegacion, pk=pk)
    if request.method == 'POST':
        delegacion.delete()
        messages.success(request, 'Delegación eliminada con éxito.')
        return redirect('delegaciones:lista_delegaciones')
    return render(request, 'delegaciones/delegacion_confirm_delete.html', {'delegacion': delegacion})


@login_required
@permission_required('delegaciones.view_meta', raise_exception=True)
def lista_metas(request):
    query = request.GET.get('q', '')
    metas = Meta.objects.select_related('delegacion')
    if query:
        metas = metas.filter(titulo__icontains=query)
    return render(request, 'delegaciones/meta_list.html', {'metas': metas, 'query': query})


@login_required
@permission_required('delegaciones.add_meta', raise_exception=True)
def crear_meta(request):
    form = MetaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Meta creada correctamente.')
        return redirect('delegaciones:lista_metas')
    return render(request, 'delegaciones/meta_form.html', {'form': form, 'titulo': 'Nueva Meta'})


@login_required
@permission_required('delegaciones.change_meta', raise_exception=True)
def editar_meta(request, pk):
    meta = get_object_or_404(Meta, pk=pk)
    form = MetaForm(request.POST or None, instance=meta)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Meta actualizada correctamente.')
        return redirect('delegaciones:lista_metas')
    return render(request, 'delegaciones/meta_form.html', {'form': form, 'titulo': 'Editar Meta'})


@login_required
@permission_required('delegaciones.delete_meta', raise_exception=True)
def eliminar_meta(request, pk):
    meta = get_object_or_404(Meta, pk=pk)
    if request.method == 'POST':
        meta.delete()
        messages.success(request, 'Meta eliminada correctamente.')
        return redirect('delegaciones:lista_metas')
    return render(request, 'delegaciones/meta_confirm_delete.html', {'meta': meta})