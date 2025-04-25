from rest_framework import serializers
from ..models import Lead
from myapps.catalogos.serializer import InstitucionAcademicaSerializer
from myapps.catalogos.models import InstitucionAcademica
from .fuentes_serializer import FuenteSerializer
from .estatus_serializer import EstatusSerializer
from .etapas_serializers import EtapaSerializer
from myapps.authentication.serializers import UserCustomizeSerializer
from myapps.catalogos.serializer import InstitucionAcademicaSerializer
from myapps.sistema.serializer import EmpresaSerializer
# from myapps.sistema.serializer import

class LeadsSerializer(serializers.ModelSerializer):
    fuente = FuenteSerializer(read_only=True)
    etapa = EtapaSerializer(read_only=True)
    vendedor_asignado = UserCustomizeSerializer(read_only=True)
    interesado_en = InstitucionAcademicaSerializer(read_only=True)
    institucion = InstitucionAcademicaSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    
    class Meta:
        model = Lead
        fields = '__all__'