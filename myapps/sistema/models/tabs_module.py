from django.db import models
from .modulo import Modulos
from myapps.authentication.models import Permissions
# Create your models here.


class TabsModulo(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    modulo = models.ForeignKey(Modulos, on_delete=models.CASCADE, related_name="modulo")
    permiso = models.ManyToManyField(Permissions, related_name="permiso")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)