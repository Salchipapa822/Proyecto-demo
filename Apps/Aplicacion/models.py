from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.conf import settings
# Create your models here.


class Usuario(AbstractUser):
    username = models.IntegerField(
		'Cedula',
        validators=[MinValueValidator(1)],
		primary_key=True
	)
    # first_name = models.CharField(
    #     'Nombres',
	# 	max_length=255,
	# 	blank=True,
	# 	null=True
	# )
    # last_name = models.CharField(
    #     'Apellidos',
	# 	max_length=255,
	# 	blank=True,
	# 	null=True
	# )

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Administrador(models.Model):
    username = models.OneToOneField(
        Usuario,
        on_delete = models.CASCADE
    ) 
   

    def __str__(self):
        return f'{self.username}'

def validate_only_letters(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('El nombre solo debe contener letras.')


class Direccion(models.Model):
    nombre = models.CharField(
        max_length=255,
        validators=[validate_only_letters]
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'dirección'
        verbose_name_plural = 'direcciones'


class Etiqueta(models.Model):
    nombre = models.CharField(
        max_length=255,
        validators=[validate_only_letters]
    )

    class Meta:
        verbose_name = 'etiqueta'
        verbose_name_plural = 'etiquetas'

    def __str__(self):
        return self.nombre


class Personal(models.Model):
    cedula = models.IntegerField(
        primary_key=True,
        unique=True,
        validators=[
            MinValueValidator(
                1000000,
                message='La cédula debe tener al menos 8 dígitos.'
            ),
            MaxValueValidator(
                999999999,
                message='La cédula debe tener como máximo 9 dígitos.'
            )
        ]
    )
    nombre = models.CharField(
        max_length=100,
        validators=[validate_only_letters]
    )
    apellido = models.CharField(
        max_length=100,
        validators=[validate_only_letters]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'personal'
        verbose_name_plural = 'personal'

class Ticket(models.Model):
    titulo = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)  
    presentado_por = models.ForeignKey('Personal', on_delete=models.CASCADE)
    resuelto_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)  # Hacer resuelto_por opcional
    presentado_en = models.ForeignKey('Direccion', on_delete=models.CASCADE)
    etiqueta = models.ForeignKey('Etiqueta',null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.fecha_cierre:
            self.resuelto_por = None
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'



class Comentario(models.Model):
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    def __str__(self):
        return "({timestamp}) {autor}: {comentario}".format(
            timestamp=self.fecha_creacion,
            autor=self.autor,
            comentario=self.contenido
        )

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'
