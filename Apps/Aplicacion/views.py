from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import TicketForm, TicketCloseForm, ComentarioForm, UsuarioForm
from .models import Ticket, Usuario
from django.views import View
from django.contrib import messages
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

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

def crear_o_actualizar_perfil(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            usuario = form.save()
            if not usuario.imagen_perfil:
                imagen_inicial = generar_imagen_inicial(usuario.username)
                usuario.imagen_perfil.save(f"{usuario.username}_inicial.png", imagen_inicial)
            return redirect('perfil_usuario.html')  # Reemplaza con la URL de éxito
    else:
        form = UsuarioForm(instance=request.user)
    return render(request, 'perfil_usuario.html', {'form': form})

def generar_imagen_inicial(nombre_usuario):
    """Genera una imagen circular con la inicial del nombre de usuario."""
    inicial = nombre_usuario[0].upper()
    ancho, alto = 100, 100
    imagen = Image.new('RGB', (ancho, alto), color=(240, 240, 240))  # Fondo gris claro
    dibujo = ImageDraw.Draw(imagen)
    fuente = ImageFont.truetype("arial.ttf", 60)  # Reemplaza "arial.ttf" con la ruta a una fuente TTF
    ancho_texto, alto_texto = dibujo.textsize(inicial, font=fuente)
    x = (ancho - ancho_texto) / 2
    y = (alto - alto_texto) / 2
    dibujo.text((x, y), inicial, font=fuente, fill=(0, 0, 0))  # Texto negro
    mascara = Image.new('L', (ancho, alto), 0)
    dibujo_mascara = ImageDraw.Draw(mascara)
    dibujo_mascara.ellipse((0, 0, ancho, alto), fill=255)
    imagen.putalpha(mascara)
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    archivo_imagen = InMemoryUploadedFile(
        buffer,
        None,
        f"{nombre_usuario}_inicial.png",
        'image/png',
        buffer.getbuffer().nbytes,
        None
    )
    return archivo_imagen

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


    