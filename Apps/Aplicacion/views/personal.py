from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from Apps.Aplicacion.models import Personal
from Apps.Aplicacion.forms import PersonalForm
from .generic import SuperuserRequiredMixin



class PersonalListView(SuperuserRequiredMixin, ListView):
    model = Personal
    template_name = 'personal/personal_list.html'
    context_object_name = 'personal_list'


class CrearPersonalView(SuperuserRequiredMixin, CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'personal/personal_form.html'
    success_url = reverse_lazy('personal_list')

    def form_valid(self, form):
        messages.success(self.request, 'Personal creado con éxito.')
        return super().form_valid(form)


class EditarPersonalView(SuperuserRequiredMixin, UpdateView):
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


class BorrarPersonalView(SuperuserRequiredMixin, DeleteView):
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
    