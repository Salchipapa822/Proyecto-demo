from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'presentado_por','resuelto_por','presentado_en', 'etiqueta']
