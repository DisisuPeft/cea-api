from django.db import models
from myapps.authentication.models import UserCustomize
from myapps.catalogos.models import Especialidades
from myapps.perfil.models import User as Profile
from myapps.catalogos.models import EstadosRepublica, Municipios, EstatusMaestro

class Maestro(models.Model):
    user = models.OneToOneField(UserCustomize, on_delete=models.CASCADE, blank=True, null=True, related_name="maestro")
    perfil = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="maestro")
    rfc = models.CharField(max_length=13, unique=True)
    curp = models.CharField(max_length=18, unique=True, null=True, blank=True)
    especialidad = models.ForeignKey(Especialidades, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_ingreso = models.DateField()
    numero_colaborador = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    estado = models.ForeignKey(EstadosRepublica, related_name="maestro", on_delete=models.SET_NULL, blank=True, null=True)
    municipio = models.ForeignKey(Municipios, related_name="maestro", on_delete=models.SET_NULL, blank=True, null=True)
    estatus = models.ForeignKey(EstatusMaestro, related_name="maestro", on_delete=models.SET_NULL, blank=True, null=True)
    activo = models.IntegerField()
    fecha_creacion = models.DateField(auto_now=True)
    fecha_actualizacion = models.DateField(null=True, blank=True)