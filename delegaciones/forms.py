from django import forms
from .models import Delegacion, Meta


class DelegacionForm(forms.ModelForm):
    class Meta:
        model = Delegacion
        fields = ['nombre', 'direccion', 'telefono', 'encargado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['titulo', 'porcentaje', 'delegacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'delegacion': forms.Select(attrs={'class': 'form-select'}),
        }
