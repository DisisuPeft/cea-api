from django.db import models
from myapps.authentication.models import UserCustomize as User
from .estatus import Estatus
from .fuentes import Fuentes
from .etapas import Etapas
from myapps.sistema.models import Empresa
from myapps.catalogos.models import InstitucionAcademica
from myapps.control_escolar.models import ProgramaEducativo
from .campanias import Campania, CampaniaPrograma
from .pipline import Pipline
# Create your models here.

class Lead(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fuente = models.ForeignKey(Fuentes, on_delete=models.CASCADE, related_name="leads")
    interesado_en = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="leads_interesado", null=True, blank=True)
    etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE, related_name="leads_etapa")
    estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE, related_name="leads_estatus")
    vendedor_asignado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='leads_asignados')
    pipeline = models.ForeignKey(Pipline, on_delete=models.SET_NULL, related_name="leads", blank=True, null=True)
    campania = models.ForeignKey(CampaniaPrograma, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads")
    tiempo_primera_respuesta = models.DurationField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    institucion = models.ForeignKey(InstitucionAcademica, on_delete=models.CASCADE, null=True, blank=True)
    etapa_anterior = models.ForeignKey(Etapas, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads_previos")
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
    
# Anadir tabla mas adelante para trazar el moviento de los leads

