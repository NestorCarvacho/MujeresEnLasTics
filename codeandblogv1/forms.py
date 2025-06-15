# forms.py
from django import forms
from .models import BloqueEditable

class BloqueEditableForm(forms.ModelForm):
    class Meta:
        model = BloqueEditable
        fields = ['nombre', 'contenido_html', 'estilos_css', 'aparece_en_inicio', 'imagen', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la publicación'}),
            'contenido_html': forms.Textarea(attrs={'class': 'form-control','id': 'editor_html'}),
            'estilos_css': forms.Textarea(attrs={'class': 'form-control','id': 'editor_css'}),
            'aparece_en_inicio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'})
        }
