from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import TicketForm
from .models import Ticket
from django.views import View
from django.contrib import messages

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


def ticket_list(request):
    tickets = Ticket.objects.all()  # Obtiene todos los tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})


class TicketCreateView (View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'ticket_form.html', {'form': form})
    
    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_success')  # Redirige a una página de éxito o lista de tickets
        return render(request, 'ticket_form.html', {'form': form})

    