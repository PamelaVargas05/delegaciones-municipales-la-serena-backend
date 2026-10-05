from django.db import models
from django.utils.translation import gettext_lazy as _

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


Solicitud = SolicitudVecinal

