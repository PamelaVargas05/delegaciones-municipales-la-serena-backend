from django.contrib import admin

from .models import Delegacion, Meta


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
