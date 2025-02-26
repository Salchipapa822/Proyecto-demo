from django.urls import path
from Apps.Aplicacion.views import (
    login_view,
    ticket_list,
    TicketCreateView,
    logout_view,
    perfil_usuario,
    ticket_detalle,
    agregar_comentario,
    TicketCerrar,
    personal_list,
    personal_create,
    usuario_create,
    usuario_list,
    direccion_list,
    direccion_form,
    administracion, 
)
from django.views.generic import TemplateView

urlpatterns = [
    path('', ticket_list, name='ticket_list'),  
    path('login/', login_view, name='login_view'),  
    path('logout/', logout_view, name='logout'), 
    path('tickets/', ticket_list, name='ticket_list'),
    path('crear/', TicketCreateView.as_view(), name='ticket_create'),  
    path('tickets/exito/', TemplateView.as_view(template_name='ticket_success.html'), name='ticket_success'),
    path('tickets/<int:ticket_id>/', ticket_detalle, name='ticket_detalle'),  
    path('tickets/<int:ticket_id>/cerrar/', TicketCerrar.as_view(), name='ticket_cerrar'),  
    path('tickets/<int:ticket_id>/comentar/', agregar_comentario, name='ticket_comentar'),  
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('personal/', personal_list, name='personal_list'),            
    path('personal/crear/', personal_create, name='personal_create'),  
    path('usuarios/', usuario_list, name='usuario_list'),                
    path('usuarios/crear/', usuario_create, name='usuario_create'),     
    path('direccion/', direccion_list, name='direccion_list'),          
    path('direccion/crear/', direccion_form, name='direccion_form'),   
    path('administracion/', administracion, name='Administracion') 
]

