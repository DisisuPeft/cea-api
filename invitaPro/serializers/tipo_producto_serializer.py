from rest_framework import serializers
from invitaPro.models import TipoProducto
# from myapps.sistema.serializer import

class TPFormViewSerializar(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ["id", "name"]
        

