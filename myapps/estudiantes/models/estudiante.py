from django.db import models
from myapps.authentication.models import UserCustomize
from myapps.perfil.models import User as Profile
from myapps.catalogos.models import (Grupos, NivelEducativo, EstadosRepublica, Municipios)

class Estudiante(models.Model):
    user = models.OneToOneField(UserCustomize, on_delete=models.CASCADE, null=True, blank=True, related_name="estudiante")
    perfil = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="estudiante")
    curp = models.CharField(max_length=18, unique=True, null=True, blank=True)
    rfc = models.CharField(max_length=13, unique=True, null=True, blank=True)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    matricula = models.CharField(max_length=20, unique=True)
    grupo = models.ForeignKey(Grupos, on_delete=models.SET_NULL, null=True, blank=True)
    lugar_nacimiento = models.ForeignKey(EstadosRepublica, related_name="estudiante", on_delete=models.SET_NULL, blank=True, null=True)
    municipio = models.ForeignKey(Municipios, related_name="estudiante", on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    tutor_nombre = models.CharField(max_length=100, blank=True, null=True)
    tutor_telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    activo = models.IntegerField()
    fecha_creacion = models.DateField(auto_now=True)
    fecha_actualizacion = models.DateField(null=True, blank=True)