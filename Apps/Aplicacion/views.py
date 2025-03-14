from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,authenticate, login
from .forms import TicketForm, TicketCloseForm, ComentarioForm, PersonalForm, UsuarioForm,UsuarioEditForm, DireccionForm, DireccionEditForm, EtiquetaForm, PersonalEditForm
from .models import Ticket, Usuario, Personal, Direccion, Etiqueta
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from django.urls import reverse_lazy



class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func


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
    


# CRUD PERSONAL #

class PersonalListView(LoginRequiredMixin, ListView):
    model = Personal
    template_name = 'personal/personal_list.html'
    context_object_name = 'personal_list'


class CrearPersonalView(LoginRequiredMixin, CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'personal/personal_form.html'
    success_url = reverse_lazy('personal_list')

    def form_valid(self, form):
        messages.success(self.request, 'Personal creado con éxito.')
        return super().form_valid(form)


class EditarPersonalView(LoginRequiredMixin, UpdateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'personal/personal_form.html'
    context_object_name = 'personal'
    success_url = reverse_lazy('personal_list')

    def form_valid(self, form):
        if 'delete' in self.request.POST:
            self.object.delete()  
            messages.success(self.request, 'Personal eliminado con éxito.')  
            return redirect(self.success_url)
        return super().form_valid(form)

    def get_object(self, queryset=None):
        cedula = self.kwargs.get('cedula')
        return get_object_or_404(Personal, cedula=cedula)


class BorrarPersonalView(LoginRequiredMixin, DeleteView):
    model = Personal
    template_name = 'personal/personal_confirm_delete.html'
    context_object_name = 'personal'
    success_url = reverse_lazy('personal_list')

    def get_object(self, queryset=None):
        cedula = self.kwargs.get('personal_cedula')
        return get_object_or_404(Personal, cedula=cedula)

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Personal eliminado con éxito.')
        return redirect(self.success_url) 
    
# CRUD Usuarios #

class UsuarioListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuario_list'

class CrearUsuarioView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Usuario creado con éxito.')
        return super().form_valid(form)

class EditarUsuarioView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioEditForm
    template_name = 'usuarios/usuario_edit.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('usuario_list')

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Usuario, pk=id)

    def form_valid(self, form):
        usuario = self.get_object()
        new_password = form.cleaned_data.get('new_password')  
        if new_password: 
            usuario.set_password(new_password)
        form.save()  
        messages.success(self.request, 'Usuario actualizado con éxito.')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        usuario = self.get_object()
        if 'delete' in request.POST:
            usuario.delete()
            messages.success(request, 'Usuario eliminado con éxito.')
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)




# CRUD DIRECCIONES #

class DireccionListView(LoginRequiredMixin, ListView):
    model = Direccion
    template_name = 'direcciones/direccion_list.html'
    context_object_name = 'direccion_list'

class CrearDireccionView(LoginRequiredMixin, CreateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'direcciones/direccion_form.html'
    success_url = reverse_lazy('direccion_list')

    def form_valid(self, form):
        messages.success(self.request, 'Dirección creada con éxito.')
        return super().form_valid(form)

class EditarDireccionView(LoginRequiredMixin, UpdateView):
    model = Direccion
    form_class = DireccionEditForm
    template_name = 'direcciones/direccion_form.html'
    success_url = reverse_lazy('direccion_list')

    def form_valid(self, form):
        messages.success(self.request, 'Dirección editada con éxito.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['direccion_id'] = self.object.pk  
        return context

class BorrarDireccionView(LoginRequiredMixin, DeleteView):
    model = Direccion
    template_name = 'direcciones/borrar_direccion.html'
    success_url = reverse_lazy('direccion_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Dirección eliminada con éxito.')
        return super().delete(request, *args, **kwargs)




# CRUD ETIQUETAS #


class EtiquetaListView(LoginRequiredMixin, ListView):
    model = Etiqueta
    template_name = 'etiquetas/etiqueta_list.html'
    context_object_name = 'etiqueta_list'


class CrearEtiquetaView(LoginRequiredMixin, CreateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = 'etiquetas/crear_etiqueta.html'
    success_url = reverse_lazy('etiqueta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Etiqueta creada con éxito.')
        return super().form_valid(form)


class EditarEtiquetaView(LoginRequiredMixin, UpdateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = 'etiquetas/editar_etiqueta.html'
    success_url = reverse_lazy('etiqueta_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Etiqueta, id=self.kwargs['etiqueta_id'])

    def form_valid(self, form):
        messages.success(self.request, 'Etiqueta editada con éxito.')
        return super().form_valid(form)
    

class BorrarEtiquetaView(LoginRequiredMixin, DeleteView):
    model = Etiqueta
    template_name = 'etiquetas/borrar_etiqueta.html'
    success_url = reverse_lazy('etiqueta_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Etiqueta, id=self.kwargs['etiqueta_id'])

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Etiqueta eliminada con éxito.')
        return super().delete(request, *args, **kwargs)
    

class AdministracionView(TemplateView, LoginRequiredMixin):
    template_name = 'Administracion.html'

class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  # Agrega el usuario al contexto
        return context