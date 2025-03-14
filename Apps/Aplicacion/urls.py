from django.urls import path
from Apps.Aplicacion.views.tickets import (
    ticket_list,
    TicketCreateView,
    ticket_detalle,
    agregar_comentario,
    TicketCerrar,
    ticket_reabrir,
    ticket_asignar_etiquetas,

)

from Apps.Aplicacion.views.generic import(
    AdministracionView,
    perfil_usuario,
    login_view,
    logout_view
)

from Apps.Aplicacion.views.usuarios import (
    UsuarioListView,
    CrearUsuarioView,
    EditarUsuarioView,
)

from Apps.Aplicacion.views.direcciones import (
    DireccionListView,
    CrearDireccionView,
    EditarDireccionView,  
    BorrarDireccionView
)

from Apps.Aplicacion.views.personal import (
    PersonalListView,
    CrearPersonalView,
    EditarPersonalView,
    BorrarPersonalView
)

from Apps.Aplicacion.views.etiquetas import ( 
    EtiquetaListView,  
    CrearEtiquetaView, 
    EditarEtiquetaView, 
    BorrarEtiquetaView  
)

from django.views.generic import TemplateView

urlpatterns = [
    path('', ticket_list, name='ticket_list'),  
    path('tickets/', ticket_list, name='ticket_list'),
    path('crear/', TicketCreateView.as_view(), name='ticket_create'),  
    path('tickets/exito/', TemplateView.as_view(template_name='ticket_success.html'), name='ticket_success'),
    path('tickets/<int:ticket_id>/', ticket_detalle, name='ticket_detalle'),  
    path('tickets/<int:ticket_id>/cerrar/', TicketCerrar.as_view(), name='ticket_cerrar'),  
    path('tickets/<int:ticket_id>/comentar/', agregar_comentario, name='ticket_comentar'),  
    
    path('personal/', PersonalListView.as_view(), name='personal_list'),            
    path('personal/crear/', CrearPersonalView.as_view(), name='personal_create'),
    path('personal/editar/<int:cedula>/', EditarPersonalView.as_view(), name='personal_edit'),
    path('personal/borrar/<int:personal_cedula>/', BorrarPersonalView.as_view(), name='personal_delete'),
    
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),                
    path('usuarios/crear/', CrearUsuarioView.as_view(), name='usuario_create'), 
    path('usuarios/editar/<int:id>/', EditarUsuarioView.as_view(), name='usuario_edit'),    
    
    path('direccion/', DireccionListView.as_view(), name='direccion_list'),
    path('direccion/crear/', CrearDireccionView.as_view(), name='crear_direccion'),  
    path('direccion/editar/<int:pk>/', EditarDireccionView.as_view(), name='editar_direccion'),  
    path('direccion/borrar/<int:pk>/', BorrarDireccionView.as_view(), name='borrar_direccion'),  
    
    path('administracion/', AdministracionView.as_view(), name='administracion'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('login/', login_view, name='login_view'),  
    path('logout/', logout_view, name='logout'), 
    
    path('ticket/<int:ticket_id>/reabrir/', ticket_reabrir, name='ticket_reabrir'), 
    path('tickets/<int:ticket_id>/asignar-etiquetas/', ticket_asignar_etiquetas, name='ticket_asignar_etiquetas'),

    path('etiquetas/', EtiquetaListView.as_view(), name='etiqueta_list'), 
    path('etiquetas/crear/', CrearEtiquetaView.as_view(), name='crear_etiqueta'),
    path('etiquetas/editar/<int:etiqueta_id>/', EditarEtiquetaView.as_view(), name='editar_etiqueta'),
    path('etiquetas/borrar/<int:etiqueta_id>/', BorrarEtiquetaView.as_view(), name='borrar_etiqueta'),
]
