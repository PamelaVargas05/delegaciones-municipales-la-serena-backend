from django.contrib import admin

from .models import SolicitudVecinal, Vecino


@admin.register(Vecino)
class VecinoAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre')
    search_fields = ('rut', 'nombre')


@admin.register(SolicitudVecinal)
class SolicitudVecinalAdmin(admin.ModelAdmin):
    list_display = ('folio', 'nombre_ciudadano', 'rut', 'delegacion', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'delegacion')
    search_fields = ('folio', 'rut', 'nombre_ciudadano')
    ordering = ('-fecha_ingreso',)
    date_hierarchy = 'fecha_ingreso'
    list_select_related = ('delegacion',)
