from rest_framework import serializers
from ..models import Lead, Request, Fuentes
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
from django.db import transaction
from myapps.sistema.models import Empresa
from myapps.control_escolar.models import ProgramaEducativo
from invitaPro.models import TipoProducto

# from myapps.sistema.serializer import

class LeadsFormSerializar(serializers.ModelSerializer):
    notas = serializers.SerializerMethodField(required=False)
    class Meta:
        model = Lead
        fields = "__all__"
        
    def create(self, validated_data):
        try:
            with transaction.atomic():
                empresa = Empresa.objects.get(id=1)
                validated_data["empresa_id"] = empresa.id
                lead = Lead.objects.create(**validated_data)
                return lead
        except Exception as e:
            raise ValueError(e)


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
        fields = [
            "id",     
            "nombre",
            "correo",
            "telefono",
            "fuente",
            "interesado_en",
            "etapa",
            "etapa_id",
            "estatus",
            "estatus_id",
            "vendedor_asignado",
            "pipeline",
            "campania",
            "tiempo_primera_respuesta",
            "empresa",
            "institucion",
            "etapa_anterior",
            "notas"
        ]
        
    def get_fuente(self, obj):
        return obj.fuente.nombre if obj.fuente else None
    
    def get_etapa(self, obj):
        return obj.etapa.nombre if obj.etapa else None
    
    def get_etapa_id(self, obj):
        return obj.etapa.id if obj.etapa else None       
    
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
    tiempo_primera_respuesta = serializers.SerializerMethodField()
    class Meta:
        model = Lead
        fields = ["id", "nombre", "interesado_en", "etapa", "estatus", "vendedor_asignado", "tiempo_primera_respuesta"]
        
    def get_interesado_en(self, obj):
        return obj.interesado_en.nombre if obj.interesado_en else None    
        
    def get_etapa(self, obj):
        return obj.etapa.nombre if obj.etapa else None
    def get_estatus(self, obj):
        return obj.estatus.nombre if obj.estatus else None
    
    def get_vendedor_asignado(self, obj):
        # print(obj.vendedor_asignado)
        return f"{obj.vendedor_asignado.profile.nombre} {obj.vendedor_asignado.profile.apellidoP} {obj.vendedor_asignado.profile.apellidoM or ''}" if obj.vendedor_asignado else None
    
    def get_tiempo_primera_respuesta(self, obj):
        duration = obj.tiempo_primera_respuesta
        total_seconds = int(duration.total_seconds())
        seconds = abs(int(total_seconds))
        
        # operations
        
        days = seconds // 86400
        horas = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        segundos = seconds % 60
        
        if days >= 1:
            format_date = f"{days} día(s), {horas:02}:{minutes:02}:{segundos:02}"
        if days == 0:
            format_date = f"{horas:02}:{minutes:02}:{segundos:02}"
            
        return format_date if obj.tiempo_primera_respuesta else None
        
class RequestAddSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    correo = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    telefono = serializers.CharField(max_length=15, allow_blank=True, allow_null=True)
    fuente = serializers.PrimaryKeyRelatedField(
        queryset=Fuentes.objects.all(),
        required=False,
        allow_null=True
    )
    interesado_en = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaEducativo.objects.all(),
        required=False,
        allow_null=True
    )
    producto_interes = serializers.PrimaryKeyRelatedField(
        queryset=TipoProducto.objects.all(),
        required=False,
        allow_null=True
    )
    empresa = serializers.SlugRelatedField(
        queryset=Empresa.objects.all(),
        slug_field="nombre",
        required=False,
        allow_null=True
    )
    
    def validate(self, attrs):
        if not attrs.get("interesado_en") and not attrs.get("producto_interes"):
            # raise serializers.ValidationError(
            #     "Se debe indicar un interes para que se pueda almacenar al prospecto"
            # )
            pass
        return attrs

    def create(self, validated_data):
        if validated_data.get("fuente") is None:
            validated_data['fuente'] = Fuentes.objects.get(nombre="Sitio Web")
        return Request.objects.create(**validated_data)
    
    
class VendedorSerializer(serializers.ModelSerializer):
    perfil = serializers.SerializerMethodField()
    class Meta:
        model = UserCustomize
        fields = ["id", "email", "perfil"]
        
        
    def get_perfil(self, obj):
        return {"id": obj.profile.id, "nombre_completo": f"{obj.profile.nombre} {obj.profile.apellidoP} {obj.profile.apellidoM or ''}"} if obj.profile else None