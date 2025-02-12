from django import forms
from .models import Ticket, Personal

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'fecha_cierre', 'presentado_por', 'resuelto_por', 'presentado_en', 'etiqueta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resuelto_por'].queryset = Personal.objects.all()  # Asegúrate de que el queryset sea correcto
