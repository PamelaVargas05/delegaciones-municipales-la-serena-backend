from django.db import models
from django.utils.translation import gettext_lazy as _


class Delegacion(models.Model):
    nombre = models.CharField(_('nombre'), max_length=150, unique=True)
    direccion = models.CharField(_('dirección'), max_length=255)
    telefono = models.CharField(_('teléfono'), max_length=30, blank=True)
    encargado = models.CharField(_('encargado'), max_length=150)

    class Meta:
        verbose_name = _('delegación')
        verbose_name_plural = _('delegaciones')
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['encargado']),
        ]

    def __str__(self):
        return self.nombre


class Meta(models.Model):
    titulo = models.CharField(_('título'), max_length=255)
    porcentaje = models.IntegerField(_('porcentaje'))
    delegacion = models.ForeignKey(
        Delegacion,
        on_delete=models.CASCADE,
        related_name='metas',
        verbose_name=_('delegación'),
    )

    class Meta:
        verbose_name = _('meta')
        verbose_name_plural = _('metas')
        ordering = ['titulo']

    def __str__(self):
        return self.titulo
