import random
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from delegaciones.models import Delegacion


class SolicitudVecinal(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'Pendiente', _('Pendiente')
        EN_PROCESO = 'En Proceso', _('En Proceso')
        RESUELTO = 'Resuelto', _('Resuelto')

    folio = models.CharField(_('folio'), max_length=30, unique=True)
    nombre_ciudadano = models.CharField(_('nombre del ciudadano'), max_length=150)
    rut = models.CharField(_('RUT'), max_length=20)
    direccion = models.CharField(_('dirección'), max_length=255)
    descripcion_problema = models.TextField(_('descripción del problema'))
    fecha_ingreso = models.DateTimeField(_('fecha de ingreso'), auto_now_add=True)
    estado = models.CharField(
        _('estado'),
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    delegacion = models.ForeignKey(
        Delegacion,
        on_delete=models.CASCADE,
        related_name='solicitudes_vecinales',
        verbose_name=_('delegación'),
    )
    tipo_solicitud = models.ForeignKey(
        'TipoSolicitud',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitudes',
        verbose_name='tipo de solicitud',
    )

    class Meta:
        verbose_name = _('solicitud vecinal')
        verbose_name_plural = _('solicitudes vecinales')
        ordering = ['-fecha_ingreso', '-id']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['delegacion', 'fecha_ingreso']),
            models.Index(fields=['rut']),
            models.Index(fields=['folio']),
        ]

    def __str__(self):
        return f'{self.folio} - {self.nombre_ciudadano}'


class Vecino(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'vecino'
        verbose_name_plural = 'vecinos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.rut})'


class TipoSolicitud(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'tipo de solicitud'
        verbose_name_plural = 'tipos de solicitud'

    def __str__(self):
        return self.nombre


class AtencionSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudVecinal, on_delete=models.CASCADE, related_name='atenciones')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='atenciones_solicitudes')
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=SolicitudVecinal.Estado.choices)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', '-id']
        verbose_name = 'atención de solicitud'
        verbose_name_plural = 'atenciones de solicitudes'

    def __str__(self):
        return f'{self.solicitud.folio} - {self.fecha:%d/%m/%Y %H:%M}'


Solicitud = SolicitudVecinal

class CodigoRecuperacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codigos_recuperacion')
    codigo = models.CharField(max_length=6)
    creado_en = models.DateTimeField(auto_now_add=True)

    def es_valido(self):
        return timezone.now() <= self.creado_en + datetime.timedelta(minutes=15)

    @classmethod
    def generar_codigo(cls, user):
        codigo_num = f"{random.randint(100000, 999999)}"
        return cls.objects.create(user=user, codigo=codigo_num)
