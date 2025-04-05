from django.db import models
from myapps.authentication.models import UserCustomize
from myapps.catalogos.models.especialidades import Especialidades

class Maestro(models.Model):
    user = models.OneToOneField(UserCustomize, on_delete=models.CASCADE, related_name="maestro")
    rfc = models.CharField(max_length=13, unique=True)
    especialidad = models.ForeignKey(Especialidades, on_delete=models.CASCADE, related_name="especialidad")
    fecha_ingreso = models.DateField()
    numero_empleado = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    activo = models.IntegerField()