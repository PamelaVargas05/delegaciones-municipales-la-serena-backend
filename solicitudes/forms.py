from django import forms

from .models import SolicitudVecinal


class SolicitudVecinalForm(forms.ModelForm):
    class Meta:
        model = SolicitudVecinal
        fields = [
            'folio',
            'nombre_ciudadano',
            'rut',
            'direccion',
            'descripcion_problema',
            'estado',
            'delegacion',
        ]
        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: DS-001'}),
            'nombre_ciudadano': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del ciudadano'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el problema'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'delegacion': forms.Select(attrs={'class': 'form-select'}),
        }
