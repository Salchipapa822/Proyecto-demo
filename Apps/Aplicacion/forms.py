from django import forms
from .models import Ticket, Comentario, Usuario

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'presentado_por','asignado_a','presentado_en']

class TicketCloseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['resuelto_por', 'etiqueta']



class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']  # Solo necesitas el contenido del comentario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'imagen_perfil']  # Agrega los campos que necesites