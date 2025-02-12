from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Ticket

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





def ticket_list(request):
    tickets = Ticket.objects.all()  # Obtiene todos los tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})