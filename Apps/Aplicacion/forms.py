from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket, Comentario, Personal, Usuario, Direccion, Etiqueta
from .models import Ticket, Comentario, Usuario


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'presentado_por', 'asignado_a', 'presentado_en']


class TicketCloseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['resuelto_por','etiqueta']  # Solo incluir el campo que deseas mostrar

    def __init__(self, *args, **kwargs):
        super(TicketCloseForm, self).__init__(*args, **kwargs)
        # Si el ticket ya está resuelto, no mostrar el campo resuelto_por
        if kwargs.get('instance') and kwargs['instance'].resuelto_por:
            self.fields.pop('resuelto_por', None)  # Eliminar el campo si ya está lleno


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['nombre', 'apellido'] 

class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['cedula','nombre', 'apellido'] 


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']  


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['cedula', 'nombre', 'apellido']

    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        self.fields['cedula'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        instance = super(PersonalForm, self).save(commit=False)
        if 'cedula' in self.data:
            instance.cedula = self.data['cedula']
        if commit:
            instance.save()
        return instance

class UsuarioForm(UserCreationForm): 
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff']

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['nombre']

class DireccionEditForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['nombre']  

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'imagen_perfil'] 

