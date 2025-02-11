from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Ticket

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('ticket_list')  # Reemplaza 'pagina_principal' con la URL de tu página principal
        else:
            error_message = "Credenciales inválidas"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')




def ticket_list(request):
    tickets = Ticket.objects.all()  # Obtiene todos los tickets
    return render(request, 'ticket_list.html', {'tickets': tickets})