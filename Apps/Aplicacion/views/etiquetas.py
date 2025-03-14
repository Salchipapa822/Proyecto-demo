from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from Apps.Aplicacion.models import Etiqueta
from Apps.Aplicacion.forms import EtiquetaForm
from .generic import SuperuserRequiredMixin


class EtiquetaListView(SuperuserRequiredMixin, ListView):
    model = Etiqueta
    template_name = 'etiquetas/etiqueta_list.html'
    context_object_name = 'etiqueta_list'


class CrearEtiquetaView(SuperuserRequiredMixin, CreateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = 'etiquetas/crear_etiqueta.html'
    success_url = reverse_lazy('etiqueta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Etiqueta creada con éxito.')
        return super().form_valid(form)


class EditarEtiquetaView(SuperuserRequiredMixin, UpdateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = 'etiquetas/editar_etiqueta.html'
    success_url = reverse_lazy('etiqueta_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Etiqueta, id=self.kwargs['etiqueta_id'])

    def form_valid(self, form):
        messages.success(self.request, 'Etiqueta editada con éxito.')
        return super().form_valid(form)
    

class BorrarEtiquetaView(SuperuserRequiredMixin, DeleteView):
    model = Etiqueta
    template_name = 'etiquetas/borrar_etiqueta.html'
    success_url = reverse_lazy('etiqueta_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Etiqueta, id=self.kwargs['etiqueta_id'])

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Etiqueta eliminada con éxito.')
        return super().delete(request, *args, **kwargs)