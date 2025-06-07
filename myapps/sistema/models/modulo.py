from django.db import models
from myapps.authentication.models import Roles, UserCustomize
# Create your models here.


class Modulos(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=50)
    bgColor = models.CharField(max_length=20)
    textColor = models.CharField(max_length=20)
    route = models.CharField(max_length=50, null=True, blank=True)
    role = models.ManyToManyField(Roles, related_name='menu_role', null=True, blank=True)
    usuario = models.ManyToManyField(UserCustomize, related_name="user_menu", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    orden = models.IntegerField(blank=True, null=True)