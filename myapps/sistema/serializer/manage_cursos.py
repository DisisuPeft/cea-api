from rest_framework import serializers
from myapps.estudiantes.models import Estudiante
from myapps.perfil.models.user_profile import User as Profile
from rest_framework.exceptions import ValidationError
from myapps.perfil.serializer import ProfileSerializer
from myapps.control_escolar.models import MaterialModulos, TypeFile
import os

class UploadFilesSerializer(serializers.Serializer):
    file = serializers.FileField()
    modulo = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        if not attrs.get("modulo"):
            raise serializers.ValidationError("Debes asignar un módulo.")
        return attrs

    def create(self, validated_data):
        file = validated_data.pop("file")
        modulo = validated_data.pop("modulo", None)
        tipo = validated_data.pop("type", None)

        if modulo:
            filename = f"modulo_{modulo}_{file.name}"

        file.name = os.path.join("materiales", filename)

        instance = MaterialModulos.objects.create(
            file=file,
            modulo_id=modulo,
            type_id=tipo,
        )
        return instance


class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=TypeFile
        fields = ["id", "nombre"]