# forms.py
from django import forms
from .models import BloqueEditable

class BloqueEditableForm(forms.ModelForm):
    class Meta:
        model = BloqueEditable
        fields = ['nombre', 'contenido_html', 'estilos_css', 'aparece_en_inicio', 'imagen']
        widgets = {
            'contenido_html': forms.Textarea(attrs={'id': 'editor_html'}),
            'estilos_css': forms.Textarea(attrs={'id': 'editor_css'}),
            'aparece_en_inicio': forms.CheckboxInput(),
        }
