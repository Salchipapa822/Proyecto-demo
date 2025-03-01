from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login
from .forms import TicketForm, TicketCloseForm, ComentarioForm, PersonalForm, UsuarioForm, DireccionForm, EtiquetaForm, UsuarioForm
from .models import Ticket, Usuario, Personal, Direccion, Etiqueta
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.



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

@login_required
def perfil_usuario(request):
    usuario = request.user  
    return render(request, 'perfil_usuario.html', {'usuario': usuario})

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
            # Guarda el usuario y la contraseña
            form.save()
            return redirect('usuario_list')  # Redirige a la lista de usuarios después de crear
    else:
        form = UsuarioForm()  # Crea un nuevo formulario vacío

    # Renderiza la plantilla con el formulario
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


def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')  # Redirige a la lista de tickets o donde desees
    else:
        form = EtiquetaForm()
    return render(request, 'crear_etiqueta.html', {'form': form})

def etiqueta_list(request):
    if request.user.is_superuser:
        etiqueta_list = Etiqueta.objects.all()
        return render(request, 'etiqueta_list.html', {'etiqueta_list': etiqueta_list})
    else:
        return render(request, 'etiqueta_list.html') 

def administracion(request):
    return render(request, 'Administracion.html')

@login_required
def perfil_usuario(request):
    return render(request, 'perfil_usuario.html', {'usuario': request.user})

