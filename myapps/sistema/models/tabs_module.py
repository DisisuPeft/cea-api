from django.db import models
from .modulo import Modulos
from myapps.authentication.models import Permissions, UserCustomize, Roles
# Create your models here.


class TabsModulo(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    modulo = models.ForeignKey(Modulos, on_delete=models.CASCADE, related_name="pestanias")
    rol = models.ManyToManyField(Roles, related_name="pestanias")
    user = models.ManyToManyField(UserCustomize, related_name="pestanias")
    href = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    orden = models.IntegerField(null=True, blank=True)