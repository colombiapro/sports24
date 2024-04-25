from django import forms 
from .models import Eventos, Usuario, Deporte


class EventoForm(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['nombre_ev', 'fecha', 'hora', 'lugar', 'descripcion']  # Lista explícita de campos
        widgets = {
            'nombre_ev': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        model2 = Deporte   
        fields = ('nombre',"programa","semestre")     