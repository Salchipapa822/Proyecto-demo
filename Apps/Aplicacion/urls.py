"""
URL configuration for Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Apps.Aplicacion.views import login_view, ticket_list, TicketCreateView
from django.views.generic import TemplateView

urlpatterns = [
    path('login_view/', login_view, name='login_view'),  # Agregar nombre para la vista de login
    path('tickets/', ticket_list, name='ticket_list'),
    path('crear/', TicketCreateView.as_view(), name='ticket_form'),  # Llamar a as_view()
    path('tickets/exito/', TemplateView.as_view(template_name='ticket_success.html'), name='ticket_success'), 
]
