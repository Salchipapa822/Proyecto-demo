from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import TicketForm, TicketCloseForm, ComentarioForm
from ..models import Ticket, Etiqueta
from django.views import View

from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin



class TicketCreateView(View):
    def get(self, request):
        return render(request, 'ticket_form.html', {'form': TicketForm()})
    
    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            return redirect('ticket_detalle', ticket_id=ticket.id)
        return render(request, 'ticket_form.html', {'form': form})
    

@login_required

def ticket_detalle(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Obtener el orden de los comentarios
    order = request.GET.get('order', 'oldest')  
    
    if order == 'newest':
        comentarios = ticket.comentarios.all().order_by('-fecha_creacion')  
    else:
        comentarios = ticket.comentarios.all().order_by('fecha_creacion')  

    close_form = TicketCloseForm(instance=ticket)
    comment_form = ComentarioForm()
    todas_etiquetas = Etiqueta.objects.all()  # Obtener todas las etiquetas

    if request.method == 'POST':
        # Manejar la asignación de etiquetas
        if 'etiquetas' in request.POST:
            etiquetas_ids = request.POST.getlist('etiquetas')
            ticket.etiquetas.set(etiquetas_ids)  # Asignar las etiquetas seleccionadas
            ticket.save()
            return redirect('ticket_detalle', ticket_id=ticket.id)  # Redirigir a la misma vista

    return render(request, 'ticket_detalle.html', {
        'ticket': ticket,
        'close_form': close_form,
        'comment_form': comment_form,
        'comentarios': comentarios,  # Pasar los comentarios ordenados a la plantilla
        'order': order,  # Pasar el orden actual a la plantilla
        'todas_etiquetas': todas_etiquetas,  # Pasar todas las etiquetas a la plantilla
    })





class TicketCerrar(LoginRequiredMixin, View):
    def post(self, request, ticket_id):

        instance = get_object_or_404(Ticket, pk=ticket_id)
        instance.resuelto_por = request.user
        instance.fecha_cierre = timezone.now()
        instance.save()

        return redirect('ticket_detalle', ticket_id=instance.pk)

    def get(self, request, *args, **kwargs):

        return HttpResponseNotAllowed(['POST'])


def ticket_reabrir(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        ticket.resuelto_por = None  
        ticket.fecha_cierre = None 
        ticket.save()  

    return redirect('ticket_detalle', ticket_id=ticket.id)  



def ticket_asignar_etiquetas(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    todas_etiquetas = Etiqueta.objects.all()  # Obtener todas las etiquetas

    if request.method == 'POST':
        etiquetas_ids = request.POST.getlist('etiquetas')  
        ticket.etiqueta.set(etiquetas_ids)  # Asignar las etiquetas seleccionadas
        ticket.save()
        return redirect('ticket_detalle', ticket_id=ticket.id)  # Redirigir a la vista de detalles del ticket

    return render(request, 'ticket_asignar_etiquetas.html', {
        'ticket': ticket,
        'todas_etiquetas': todas_etiquetas,
    })



def agregar_comentario(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        comment_form = ComentarioForm(request.POST)
        if comment_form.is_valid():
            # Crear el nuevo comentario
            comentario = comment_form.save(commit=False)
            comentario.ticket = ticket
            comentario.autor = request.user
            comentario.save()

            # Redirigir al ticket específico
            return redirect('ticket_detalle', ticket_id=ticket.id)
    else:
        comment_form = ComentarioForm()


    return render(request, 'agregar_comentario.html', {
        'ticket': ticket,
        'comment_form': comment_form
    })


def ticket_list(request):
    tickets = Ticket.objects.all()  # Asegúrate de que esto devuelve un queryset
    return render(request, 'ticket_list.html', {'tickets': tickets})