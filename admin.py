from django.contrib import admin

from delegaciones.models import Delegacion, Meta
from solicitudes.models import SolicitudVecinal, Vecino


@admin.register(Delegacion)
class DelegacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'encargado')
    search_fields = ('nombre', 'direccion', 'telefono', 'encargado')
    ordering = ('nombre',)


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'porcentaje', 'delegacion')
    search_fields = ('titulo', 'delegacion__nombre')
    list_filter = ('delegacion',)


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

