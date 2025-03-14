from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from Apps.Aplicacion.models import Direccion
from Apps.Aplicacion.forms import DireccionForm, DireccionEditForm



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

