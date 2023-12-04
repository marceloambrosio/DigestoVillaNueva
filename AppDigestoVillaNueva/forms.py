from django import forms
from .models import Decreto, Ordenanza, Resolucion, Declaracion, BoletinOficial
from django.forms import ModelForm, Textarea, NumberInput, Select, DateInput, FileInput, CheckboxInput

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

class OrdenanzaForm(forms.ModelForm):
    class Meta:
        model = Ordenanza
        fields = ['fecha_creacion', 'descripcion', 'archivo_pdf', 'publicado', 'eliminado', 'numero_ordenanza', 'anio', 'fecha_publicacion']
        widgets = {
            'fecha_creacion': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'descripcion': Textarea(attrs={'class': 'form-control'}),    
            'archivo_adjunto': Select(attrs={'class': 'form-control'}),    
            'archivo_pdf': FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}), 
            'numero_ordenanza': NumberInput(attrs={'class': 'form-control'}),    
            'anio': NumberInput(attrs={'class': 'form-control'}),    
            'fecha_publicacion': DateInput(attrs={'class': 'form-control','type': 'date',}),    
        }

class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Resolucion
        fields = ['fecha_creacion', 'descripcion', 'archivo_pdf', 'publicado', 'eliminado', 'numero_resolucion', 'anio', 'fecha_publicacion']
        widgets = {
            'fecha_creacion': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'descripcion': Textarea(attrs={'class': 'form-control'}),    
            'archivo_adjunto': Select(attrs={'class': 'form-control'}),    
            'archivo_pdf': FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}), 
            'numero_resolucion': NumberInput(attrs={'class': 'form-control'}),    
            'anio': NumberInput(attrs={'class': 'form-control'}),    
            'fecha_publicacion': DateInput(attrs={'class': 'form-control','type': 'date',}),    
        }

class DeclaracionForm(forms.ModelForm):
    class Meta:
        model = Declaracion
        fields = ['fecha_creacion', 'descripcion', 'archivo_pdf', 'publicado', 'eliminado', 'numero_declaracion', 'anio', 'fecha_publicacion']
        widgets = {
            'fecha_creacion': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'descripcion': Textarea(attrs={'class': 'form-control'}),    
            'archivo_adjunto': Select(attrs={'class': 'form-control'}),    
            'archivo_pdf': FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}), 
            'numero_declaracion': NumberInput(attrs={'class': 'form-control'}),    
            'anio': NumberInput(attrs={'class': 'form-control'}),    
            'fecha_publicacion': DateInput(attrs={'class': 'form-control','type': 'date',}),    
        }

class BoletinOficialForm(forms.ModelForm):
    class Meta:
        model = BoletinOficial
        fields = ['fecha_creacion', 'fecha_desde', 'fecha_hasta', 'decretos', 'resoluciones', 'ordenanzas', 'declaraciones']
        widgets = {
            'fecha_creacion': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'fecha_desde': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'fecha_hasta': DateInput(attrs={'class': 'form-control','type': 'date',}),
            'decretos': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch'}),
            'resoluciones': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch'}),
            'ordenanzas': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch'}),
            'declaraciones': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role': 'switch'}),
        }