from django.db import models
from django.db.models import OneToOneField
from django.db.models.fields.related import ForeignKey
from myapps.catalogos.models.genero import Genero
from myapps.catalogos.models.niveleducativo import NivelEducativo
from myapps.catalogos.models.tipo_nivel import TipoNivel
# Create your models here.    
    
class Profile(models.Model):
    nombre = models.CharField(max_length=100)
    apellidoP = models.CharField(max_length=100)
    apellidoM = models.CharField(max_length=100, null=True)
    edad = models.IntegerField(null=True, blank=True)  # Permitir valores nulos
    fechaNacimiento = models.DateField(null=True, blank=True)  # Permitir valores nulos
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    nivEdu = models.ForeignKey(TipoNivel, on_delete=models.CASCADE, null=True)  # Permitir valores nulos
    telefono = models.CharField(max_length=15, null=True)
    user = OneToOneField('authentication.UserCustomize', on_delete=models.SET_NULL, related_name='profile', null=True)
    