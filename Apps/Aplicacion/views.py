from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.utils import timezone
from .forms import TicketForm, TicketCloseForm, ComentarioForm, UsuarioForm
from .models import Ticket
from django.views import View
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('ticket_list')
        messages.error(request, 'Credenciales inválidas.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login_view')

@login_required
def ticket_detalle(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    close_form = TicketCloseForm(instance=ticket)
    comment_form = ComentarioForm()

    if request.method == 'POST':
        close_form = TicketCloseForm(request.POST, instance=ticket)
        comment_form = ComentarioForm(request.POST)

        if close_form.is_valid() and comment_form.is_valid():
            ticket.fecha_cierre = timezone.now()
            ticket.resuelto_por = close_form.cleaned_data['resuelto_por']
            ticket.etiqueta = close_form.cleaned_data['etiqueta']
            ticket.save()

            comentario = comment_form.save(commit=False)
            comentario.ticket = ticket
            comentario.autor = request.user
            comentario.save()

            return redirect('ticket_detalle', ticket_id=ticket.id)

    return render(request, 'ticket_detalle.html', {
        'ticket': ticket,
        'close_form': close_form,
        'comment_form': comment_form
    })

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()  # Asegúrate de que esto devuelve un queryset
    return render(request, 'ticket_list.html', {'tickets': tickets})

@login_required
def crear_o_actualizar_perfil(request):
    form = UsuarioForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        if not usuario.imagen_perfil:
            imagen_inicial = generar_imagen_inicial(usuario.username)
            usuario.imagen_perfil.save(f"{usuario.username}_inicial.png", imagen_inicial)
        return redirect('perfil_usuario')

    return render(request, 'perfil_usuario.html', {'form': form})

def generar_imagen_inicial(nombre_usuario):
    inicial = nombre_usuario[0].upper()
    imagen = Image.new('RGB', (100, 100), color=(240, 240, 240))
    dibujo = ImageDraw.Draw(imagen)
    fuente = ImageFont.truetype("arial.ttf", 60)
    ancho_texto, alto_texto = dibujo.textsize(inicial, font=fuente)
    x, y = (100 - ancho_texto) / 2, (100 - alto_texto) / 2
    dibujo.text((x, y), inicial, font=fuente, fill=(0, 0, 0))

    mascara = Image.new('L', (100, 100), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, 100, 100), fill=255)
    imagen.putalpha(mascara)

    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    return InMemoryUploadedFile(buffer, None, f"{nombre_usuario}_inicial.png", 'image/png', buffer.getbuffer().nbytes, None)

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
def perfil_usuario(request):
    return render(request, 'perfil_usuario.html', {'usuario': request.user})
