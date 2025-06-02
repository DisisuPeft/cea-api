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
from myapps.authentication.models import UserCustomize
# from myapps.sistema.serializer import

class LeadsSerializer(serializers.ModelSerializer):
    fuente = serializers.SerializerMethodField()
    etapa = serializers.SerializerMethodField()
    vendedor_asignado = serializers.SerializerMethodField()
    interesado_en = serializers.SerializerMethodField()
    institucion = serializers.SerializerMethodField()
    # empresa = EmpresaSerializer(read_only=True)
    estatus = serializers.SerializerMethodField()
    campania = CampaniaProgramaSerializer(read_only=True)
    notas = NotasSerializer(read_only=True, many=True)
    
    class Meta:
        model = Lead
        fields = '__all__'
        
    def get_fuente(self, obj):
        return obj.fuente.nombre if obj.fuente else None
    
    def get_etapa(self, obj):
        return obj.etapa.nombre if obj.etapa else None
    
    def get_estatus(self, obj):
        return obj.estatus.nombre if obj.estatus else None
    
    def get_vendedor_asignado(self, obj):
        return f"{obj.vendedor_asignado.profile.nombre} {obj.vendedor_asignado.profile.apellidoP} {obj.vendedor_asignado.profile.apellidoM or ''}" if obj.vendedor_asignado else None
    
    def get_interesado_en(self, obj):
        return obj.interesado_en.nombre if obj.interesado_en else None   
    
    def get_institucion(self, obj):
        return obj.institucion.nombre if obj.institucion else None 
    
class LeadRecentSerializer(serializers.ModelSerializer):
    interesado_en = serializers.SerializerMethodField()
    etapa = serializers.SerializerMethodField()
    estatus = serializers.SerializerMethodField()
    vendedor_asignado = serializers.SerializerMethodField()
    class Meta:
        model = Lead
        fields = ["id", "nombre", "interesado_en", "etapa", "estatus", "vendedor_asignado"]
        
    def get_interesado_en(self, obj):
        return obj.interesado_en.nombre if obj.interesado_en else None    
        
    def get_etapa(self, obj):
        return obj.etapa.nombre if obj.etapa else None
    def get_estatus(self, obj):
        return obj.estatus.nombre if obj.estatus else None
    
    def get_vendedor_asignado(self, obj):
        # print(obj.vendedor_asignado)
        return f"{obj.vendedor_asignado.profile.nombre} {obj.vendedor_asignado.profile.apellidoP} {obj.vendedor_asignado.profile.apellidoM or ''}" if obj.vendedor_asignado else None
    
        
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
    
    
class VendedorSerializer(serializers.ModelSerializer):
    perfil = serializers.SerializerMethodField()
    class Meta:
        model = UserCustomize
        fields = ["id", "email", "perfil"]
        
        
    def get_perfil(self, obj):
        return {"id": obj.profile.id, "nombre_completo": f"{obj.profile.nombre} {obj.profile.apellidoP} {obj.profile.apellidoM or ''}"} if obj.profile else None