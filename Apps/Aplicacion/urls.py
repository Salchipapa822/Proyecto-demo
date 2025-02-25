from django.urls import path
from Apps.Aplicacion.views import login_view, ticket_list, TicketCreateView, logout_view, perfil_usuario
from django.views.generic import TemplateView
from .views import ticket_detalle, ticket_detalle, agregar_comentario, TicketCerrar
urlpatterns = [
    path('', login_view, name='login_view'),
    path('login_view/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'), 
    path('tickets/', ticket_list, name='ticket_list'),
    path('crear/', TicketCreateView.as_view(), name='ticket_create'),  
    path('tickets/exito/', TemplateView.as_view(template_name='ticket_success.html'), name='ticket_success'),
    path('tickets/<int:ticket_id>/', ticket_detalle, name='ticket_detalle'),  # URL para los detalles
    path('tickets/<int:ticket_id>/cerrar', TicketCerrar.as_view(), name='ticket_cerrar'),  # URL para cerrar el ticket
    path('tickets/<int:ticket_id>/comentar', agregar_comentario, name='ticket_comentar'),  # URL para agregar comentario
    path('perfil/', perfil_usuario, name='perfil_usuario')
]


