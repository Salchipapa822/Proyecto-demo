from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import TicketForm, TicketCloseForm, ComentarioForm
from .models import Ticket, Usuario
from django.views import View
from django.contrib import messages
from django.utils import timezone

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ticket_list')  # Redirige a la vista de ticket_list
        else:
            # Manejar el error de inicio de sesión
            return render(request, 'login.html', {'error': 'Credenciales inválidas.'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login_view')


def ticket_detalle(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        # Manejar el cierre del ticket
        close_form = TicketCloseForm(request.POST, instance=ticket)
        comment_form = ComentarioForm(request.POST)

        if close_form.is_valid() and comment_form.is_valid():
            # Cerrar el ticket
            ticket.fecha_cierre = timezone.now()  # Establecer la fecha de cierre
            ticket.resuelto_por = close_form.cleaned_data['resuelto_por']  # Asignar el usuario que resolvió
            ticket.etiqueta = close_form.cleaned_data['etiqueta']  # Asignar la etiqueta
            ticket.save()  # Guardar los cambios en el ticket

            # Crear el nuevo comentario
            comentario = comment_form.save(commit=False)
            comentario.ticket = ticket  # Asociar el comentario con el ticket
            comentario.autor = request.user  # Asumiendo que el usuario está autenticado
            comentario.save()  # Guardar el comentario

            # Redirigir al ticket específico
            return redirect('ticket_detalle', ticket_id=ticket.id)  # Cambia esto para redirigir al ticket específico
    else:
        close_form = TicketCloseForm(instance=ticket)
        comment_form = ComentarioForm()

    return render(request, 'ticket_detalle.html', {
        'ticket': ticket,
        'close_form': close_form,
        'comment_form': comment_form
    })

def ticket_list(request):
    tickets = Ticket.objects.all()  # Obtiene todos los tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})

class TicketCreateView(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'ticket_form.html', {'form': form})
    
    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()  # Guarda el ticket y lo asigna a la variable ticket
            return redirect('ticket_detalle', ticket_id=ticket.id)  # Redirige a la vista de detalles del ticket
        return render(request, 'ticket_form.html', {'form': form})
    

@login_required
def perfil_usuario(request):
    usuario = request.user  
    return render(request, 'perfil_usuario.html', {'usuario': usuario})


    