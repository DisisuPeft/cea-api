from rest_framework import serializers
from ..models import Pipline, Etapas
from ..serializer import EtapaSerializer
from myapps.catalogos.serializer import InstitucionAcademicaSerializer
from myapps.sistema.serializer import EmpresaSerializer
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
from myapps.catalogos.models import InstitucionAcademica
from myapps.sistema.models import Empresa
from myapps.control_escolar.models import ProgramaEducativo

class PipelineSerializerCreate(serializers.ModelSerializer):
    unidad_academica = serializers.IntegerField()
    programa = serializers.IntegerField()
    etapas = EtapaSerializer(many=True)
    empresa = serializers.IntegerField()
    
    class Meta:
        model = Pipline
        fields = ["id", "nombre", "orden", "programa", "unidad_academica", "empresa", 'etapas']
    
    def create(self, validated_data):
        etapas = validated_data.pop('etapas')
        
        programa_id = validated_data.pop('programa')
        unidad_academica_id = validated_data.pop('unidad_academica')
        empresa_id = validated_data.pop('empresa')
        
        programa = ProgramaEducativo.objects.get(id=programa_id)
        unidad_academica = InstitucionAcademica.objects.get(id=unidad_academica_id)
        empresa = Empresa.objects.get(id=empresa_id)
        
        pipeline = Pipline.objects.create(
            programa=programa,
            unidad_academica=unidad_academica,
            empresa=empresa,
            **validated_data
        )
        
        for etapa in etapas:
            etapa = Etapas.objects.create(**etapa)
            pipeline.etapas.add(etapa)
        
        return pipeline 
    
class PipelineSerializerUpdate(serializers.ModelSerializer):
    unidad_academica = serializers.IntegerField(required=False)
    programa = serializers.IntegerField(required=False)
    etapas = EtapaSerializer(many=True, required=False)
    empresa = serializers.IntegerField(required=False)

    class Meta:
        model = Pipline
        fields = ["id", "nombre", "orden", "programa", "unidad_academica", "empresa", "etapas"]

    def update(self, instance, validated_data):
        etapas_data = validated_data.pop('etapas', None)

        # Asigna relaciones por ID si vienen en los datos
        if 'programa' in validated_data:
            instance.programa = ProgramaEducativo.objects.get(id=validated_data.pop('programa'))

        if 'unidad_academica' in validated_data:
            instance.unidad_academica = InstitucionAcademica.objects.get(id=validated_data.pop('unidad_academica'))

        if 'empresa' in validated_data:
            instance.empresa = Empresa.objects.get(id=validated_data.pop('empresa'))

        # Actualiza los campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Si vienen etapas nuevas, las reemplazamos
        if etapas_data is not None:
            instance.etapas.clear()
            for etapa in etapas_data:
                etapa_obj = Etapas.objects.create(**etapa)
                instance.etapas.add(etapa_obj)

        return instance
    
class PipelineSerializer(serializers.ModelSerializer):
    unidad_academica = serializers.SerializerMethodField()
    programa = serializers.SerializerMethodField()
    etapas = serializers.SerializerMethodField()
    empresa = serializers.SerializerMethodField()
    class Meta:
        model = Pipline
        fields = ["id", "nombre", "orden", "programa", "unidad_academica", "empresa", 'etapas']
     
    def get_programa(self, obj):        
        return {'id': obj.programa.id, 'nombre': obj.programa.nombre} if obj.programa else None
    
    def get_unidad_academica(self, obj):        
        return {'id': obj.unidad_academica.id, 'nombre': obj.unidad_academica.nombre} if obj.unidad_academica else None
    
    def get_etapas(self, obj):
     return [
        {'id': etapa.id, 'nombre': etapa.nombre, 'orden': etapa.orden}
        for etapa in obj.etapas.all()
    ]
     
    def get_empresa(self, obj):
        return {'id': obj.empresa.id, 'nombre': obj.empresa.nombre} if obj.empresa else None
    
    
    def create(self, validated_data):
        print(validated_data)
        # etapas = validated_data.pop('etapas')
        # pipeline = Pipline.objects.create(**validated_data)
        
        # for etapa in etapas:
        #     etapa = Etapas.objects.create(**etapa)
        #     pipeline.etapas.add(etapa)
        
        return validated_data