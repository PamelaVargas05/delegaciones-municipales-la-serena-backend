from django import forms
from .models import Delegacion


class DelegacionForm(forms.ModelForm):

    class Meta:
        model = Delegacion
        fields = ['nombre', 'direccion', 'telefono', 'encargado']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la delegación',
                }
            ),
            'direccion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Dirección'}
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Teléfono de contacto',
                }
            ),
            'encargado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del encargado',
                }
            ),
        }