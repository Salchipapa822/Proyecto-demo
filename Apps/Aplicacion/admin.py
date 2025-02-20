from django.contrib import admin
from .models import Usuario, Administrador, Direccion, Etiqueta, Personal, Ticket, Comentario

# Registro del modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'username')

# Registro del modelo Direccion
@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registro del modelo Etiqueta
@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registro del modelo Personal
@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'cedula')

# Registro del modelo Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_creacion', 'presentado_por', 'resuelto_por', 'fecha_cierre')
    search_fields = ('titulo',)
    list_filter = ('fecha_creacion', 'presentado_por', 'resuelto_por')

# Registro del modelo Comentario
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'autor', 'ticket')
    search_fields = ('contenido',)
    list_filter = ('fecha_creacion', 'autor')
