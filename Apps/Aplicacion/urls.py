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
    personal_edit,
    personal_delete,
    usuario_create,
    usuario_list,
    usuario_edit,
    direccion_list,
    crear_direccion,  
    borrar_direccion,
    editar_direccion,
    administracion,
    ticket_reabrir,
    ticket_asignar_etiquetas,
    CrearEtiquetaView,  # Cambiado a la vista basada en clase
    EtiquetaListView,   # Cambiado a la vista basada en clase
    EditarEtiquetaView, # Cambiado a la vista basada en clase
    BorrarEtiquetaView   # Cambiado a la vista basada en clase
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
    path('personal/editar/<int:personal_cedula>/', personal_edit, name='personal_edit'),
    path('personal/borrar/<int:personal_cedula>/', personal_delete, name='personal_delete'),
    path('usuarios/', usuario_list, name='usuario_list'),                
    path('usuarios/crear/', usuario_create, name='usuario_create'), 
    path('usuarios/editar/<int:id>/', usuario_edit, name='usuario_edit'),    
    path('direccion/', direccion_list, name='direccion_list'),
    path('direccion/crear/', crear_direccion, name='crear_direccion'),  
    path('direccion/editar/<int:direccion_id>/', editar_direccion, name='editar_direccion'),  
    path('direccion/borrar/<int:direccion_id>/', borrar_direccion, name='borrar_direccion'),  
    path('administracion/', administracion, name='administracion'),
    path('ticket/<int:ticket_id>/reabrir/', ticket_reabrir, name='ticket_reabrir'), 
    path('tickets/<int:ticket_id>/asignar-etiquetas/', ticket_asignar_etiquetas, name='ticket_asignar_etiquetas'),
    path('etiquetas/', EtiquetaListView.as_view(), name='etiqueta_list'), 
    path('etiquetas/crear/', CrearEtiquetaView.as_view(), name='crear_etiqueta'),
    path('etiquetas/editar/<int:etiqueta_id>/', EditarEtiquetaView.as_view(), name='editar_etiqueta'),
    path('etiquetas/borrar/<int:etiqueta_id>/', BorrarEtiquetaView.as_view(), name='borrar_etiqueta'),
]
