from django.urls import path
from Apps.Aplicacion.views import login_view, ticket_list, TicketCreateView, logout_view
from django.views.generic import TemplateView
from .views import ticket_detalle
from . import views


urlpatterns = [
    path('', login_view, name='login_view'),
    path('login_view/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'), 
    path('tickets/', ticket_list, name='ticket_list'),
    path('crear/', TicketCreateView.as_view(), name='ticket_create'),  
    path('tickets/exito/', TemplateView.as_view(template_name='ticket_success.html'), name='ticket_success'),
    path('ticket/<int:ticket_id>/', views.ticket_detalle, name='ticket_detalle'),  # URL para los detalles
]


