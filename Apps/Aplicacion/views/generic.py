from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,authenticate, login
from ..forms import UsuarioForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.views.generic import TemplateView



class SuperuserRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser



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





@login_required
def perfil_usuario(request):
    usuario = request.user  
    return render(request, 'perfil_usuario.html', {'usuario': usuario})


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


    

class AdministracionView(TemplateView, LoginRequiredMixin):
    template_name = 'Administracion.html'

class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  # Agrega el usuario al contexto
        return context