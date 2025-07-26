from django.db import models
from myapps.authentication.models import Roles, UserCustomize
# Create your models here.


class Empresa(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)  # Para usar en URLs
    logo = models.ImageField(upload_to="instituciones/logos/", blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    rfc = models.CharField(max_length=20, null=True, blank=True)
    activa = models.IntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)