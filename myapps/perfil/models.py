from django.db import models
from django.db.models import OneToOneField
from django.db.models.fields.related import ForeignKey
# Create your models here.

class Genero(models.Model):
    name = models.CharField(max_length=50)
    
class NivelEducativo(models.Model):
    name = models.CharField(max_length=50)
    
class Profile(models.Model):
    nombre = models.CharField(max_length=100)
    apellidoP = models.CharField(max_length=100)
    apellidoM = models.CharField(max_length=100, null=True)
    edad = models.IntegerField(null=True, blank=True)  # Permitir valores nulos
    fechaNacimiento = models.DateField(null=True, blank=True)  # Permitir valores nulos
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    nivEdu = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, null=True)  # Permitir valores nulos
    telefono = models.CharField(max_length=15, null=True)
    user = OneToOneField('authentication.UserCustomize', on_delete=models.SET_NULL, related_name='profile', null=True)