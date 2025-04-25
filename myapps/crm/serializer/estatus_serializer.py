from rest_framework import serializers
from ..models import Estatus


class EstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estatus
        fields = '__all__'