from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.


@admin.register(models.Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username')


