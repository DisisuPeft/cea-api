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
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
from .campania_serializers import CampaniaProgramaSerializer
from .notas_serializers import NotasSerializer
from rest_framework.exceptions import ValidationError
# from myapps.sistema.serializer import

class LeadsSerializer(serializers.ModelSerializer):
    fuente = FuenteSerializer(read_only=True)
    etapa = EtapaSerializer(read_only=True)
    vendedor_asignado = UserCustomizeSerializer(read_only=True)
    interesado_en = ProgramaEducativoSerializer(read_only=True)
    institucion = InstitucionAcademicaSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    estatus = EstatusSerializer(read_only=True)
    campania = CampaniaProgramaSerializer(read_only=True)
    notas = NotasSerializer(read_only=True, many=True)
    class Meta:
        model = Lead
        fields = '__all__'
        
class LeadCreateLandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        
    def create(self, validated_data):
        lead = Lead.objects.create(**validated_data)
        if not lead:
            raise ValidationError("lead no creado")
        lead.save()
        return lead