from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from Apps.Aplicacion.models import Usuario
from Apps.Aplicacion.forms import UsuarioForm, UsuarioEditForm
from .generic import SuperuserRequiredMixin


class UsuarioListView(SuperuserRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuario_list'

class CrearUsuarioView(SuperuserRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Usuario creado con éxito.')
        return super().form_valid(form)

class EditarUsuarioView(SuperuserRequiredMixin, UpdateView):
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


