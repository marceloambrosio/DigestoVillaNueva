from django import forms
from .models import Decreto
from django.forms import ModelForm, Textarea, NumberInput, Select, DateInput, FileInput

class DecretoForm(forms.ModelForm):
    class Meta:
        model = Decreto
        fields = ['fecha_creacion', 'descripcion', 'archivo_pdf', 'publicado', 'eliminado', 'numero_decreto', 'anio', 'fecha_publicacion']
        widgets = {
            'fecha_creacion': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'descripcion': Textarea(attrs={'class': 'form-control'}),    
            'archivo_adjunto': Select(attrs={'class': 'form-control'}),    
            'archivo_pdf': FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}), 
            'numero_decreto': NumberInput(attrs={'class': 'form-control'}),    
            'anio': NumberInput(attrs={'class': 'form-control'}),    
            'fecha_publicacion': DateInput(attrs={'class': 'form-control','type': 'date',}),    
        }