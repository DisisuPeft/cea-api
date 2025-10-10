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
from myapps.crm.helpers import get_now, get_today
from myapps.crm.model import Base


class Request(Base):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fuente = models.ForeignKey(Fuentes, on_delete=models.CASCADE, related_name="request")
    interesado_en = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE, related_name="request_interesado", null=True, blank=True)
    producto_interes = models.ForeignKey('invitaPro.Producto', on_delete=models.CASCADE, null=True, blank=True, related_name="request_producto")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    
# Anadir tabla mas adelante para trazar el moviento de los leads

