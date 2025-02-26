from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login
from .forms import TicketForm, TicketCloseForm, ComentarioForm, PersonalForm, UsuarioForm, DireccionForm
from .models import Ticket, Usuario, Personal, Direccion
from django.views import View
from django.contrib import messages
from django.utils import timezone

from django.http import HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin


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


@login_required
def ticket_detalle(request, ticket_id):
    # Obtener el ticket por ID
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Obtener el orden de los comentarios desde la solicitud (GET)
    order = request.GET.get('order', 'oldest')  # 'oldest' o 'newest'
    
    # Ordenar los comentarios según el parámetro de orden
    if order == 'newest':
        comentarios = ticket.comentarios.all().order_by('-fecha_creacion')  # Más nuevos primero
    else:
        comentarios = ticket.comentarios.all().order_by('fecha_creacion')  # Más viejos primero

    # Crear formularios
    close_form = TicketCloseForm(instance=ticket)
    comment_form = ComentarioForm()

    # Renderizar la plantilla con el contexto
    return render(request, 'ticket_detalle.html', {
        'ticket': ticket,
        'close_form': close_form,
        'comment_form': comment_form,
        'comentarios': comentarios,  # Pasar los comentarios ordenados a la plantilla
        'order': order,  # Pasar el orden actual a la plantilla
    })





class TicketCerrar(LoginRequiredMixin, View):
    def post(self, request, ticket_id):

        instance = get_object_or_404(Ticket, pk=ticket_id)
        instance.resuelto_por = request.user
        instance.save()

        return redirect('ticket_detalle', ticket_id=instance.pk)

    def get(self, request, *args, **kwargs):

        return HttpResponseNotAllowed(['POST'])
    


def agregar_comentario(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        comment_form = ComentarioForm(request.POST)
        if comment_form.is_valid():
            # Crear el nuevo comentario
            comentario = comment_form.save(commit=False)
            comentario.ticket = ticket  # Asociar el comentario con el ticket
            comentario.autor = request.user  # Asumiendo que el usuario está autenticado
            comentario.save()  # Guardar el comentario

            # Redirigir al ticket específico
            return redirect('ticket_detalle', ticket_id=ticket.id)
    else:
        comment_form = ComentarioForm()

    return render(request, 'agregar_comentario.html', {
        'ticket': ticket,
        'comment_form': comment_form
    })

@login_required
def perfil_usuario(request):
    usuario = request.user  
    return render(request, 'perfil_usuario.html', {'usuario': usuario})

def ticket_list(request):
    tickets = Ticket.objects.all()  # Obtiene todos los tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})

 # CRUD del Sistema

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
    

def personal_list(request):
    personal_list = Personal.objects.all()
    return render(request, 'personal_list.html', {'personal_list': personal_list})

def personal_create(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_list')  
    else:
        form = PersonalForm()
    return render(request, 'personal_form.html', {'form': form})


def usuario_list(request):
    usuario_list = Usuario.objects.all()
    return render(request, 'usuario_list.html', {'usuario_list': usuario_list})

def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuario_list')  
    else:
        form = UsuarioForm()
    return render(request, 'usuario_form.html', {'form': form})


def direccion_list(request):
    direcciones = Direccion.objects.all()
    return render(request, 'direccion_list.html', {'direccion_list': direcciones})

def direccion_form(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('direccion_list')  
    else:
        form = DireccionForm()
    
    return render(request, 'direccion_form.html', {'form': form})

def administracion(request):
    return render(request, 'Administracion.html')