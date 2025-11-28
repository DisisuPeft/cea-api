from rest_framework import serializers
from myapps.estudiantes.models import Estudiante
from myapps.perfil.models.user_profile import User as Profile
from rest_framework.exceptions import ValidationError
from myapps.perfil.serializer import ProfileSerializer
from myapps.control_escolar.models import MaterialModulos, TypeFile
import os, re
from django.urls import reverse
from django.db.models.fields.files import FieldFile
from urllib.parse import urlparse, urlunparse

class UploadFilesSerializer(serializers.Serializer):
    file = serializers.FileField()
    programa = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        if not attrs.get("programa"):
            raise serializers.ValidationError("No se envio el identificador del programa.")
        return attrs

    def create(self, validated_data):
        file = validated_data.pop("file")
        programa = validated_data.pop("programa", None)
        tipo = validated_data.pop("type", None)

        if programa:
            filename = f"programa_{programa}_{file.name}"

        file.name = os.path.join("materiales", filename)

        instance = MaterialModulos.objects.create(
            file=file,
            type_id=tipo,
            programa_id=programa
        )
        return instance


class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=TypeFile
        fields = ["id", "nombre"]
        

    # def _display_name_from_path(path: str) -> str:
    #     name = os.path.basename(path or "")
    #     # Elimina los prefijos para mostrar a usuarios
    #     return re.sub(r'^(programa)_\d+_', '', name, flags=re.I)
    
    def _force_https(url: str) -> str:
        p = urlparse(url)
        if p.scheme != "https":
            p = p._replace(scheme="https")
        return urlunparse(p)

class MaterialSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialModulos
        fields = [
            "id", "file"
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        admin = bool(request and request.user.roleID.filter(name="Administrador").exists())
        
        if not admin:
            return data.pop('file', None)
        return data
    
    def get_file(self, obj):
        # Obten el path, si existe, la URL publica directa
        # Si es FileField tendra .name/.url
        if isinstance(obj.file, FieldFile) and obj.file:
            path = obj.file.name
            public_url = getattr(obj.file, "url", None)
        else:
            path = str(obj.file or "")
            public_url = None
            
        display_name = self._display_name_from_path(path)
        
        # URL absoula al endpoint de descarga
        download_url = None
        rq = self.context.get("request")
        if rq:
            download_url = rq.build_absolute_uri(
                reverse("material-download", args=[obj.id])
            )
            # download_url = _force_https(raw_url)
        return {
            
            "name": display_name,
            "id": obj.id,
            # "path": path,
            # "public_url": public_url,
            # "download_url": download_url
        }

    @staticmethod
    def _display_name_from_path(path):
        name = os.path.basename(path or "")
        # Elimina los prefijos para mostrar a usuarios
        return re.sub(r'^(programa)_\d+_', '', name, flags=re.I)