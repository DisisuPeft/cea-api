from django.db import models
from myapps.authentication.models import UserCustomize
from myapps.catalogos.models.especialidades import Especialidades
from myapps.catalogos.models import Genero, NivelEducativo
from myapps.authentication.models import UserCustomize

class User(models.Model):
    nombre = models.CharField(max_length=100)
    apellidoP = models.CharField(max_length=100)
    apellidoM = models.CharField(max_length=100, null=True)
    edad = models.IntegerField(null=True, blank=True)  # Permitir valores nulos
    fechaNacimiento = models.DateField(null=True, blank=True)  # Permitir valores nulos
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    nivEdu = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, null=True)  # Permitir valores nulos
    telefono = models.CharField(max_length=15, null=True)
    user = models.OneToOneField(UserCustomize, on_delete=models.SET_NULL, related_name='profile', null=True, blank=True)