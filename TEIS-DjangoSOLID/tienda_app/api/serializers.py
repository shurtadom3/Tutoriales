from rest_framework import serializers
from tienda_app.models import Libro


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'stock_actual']


class OrdenInputSerializer(serializers.Serializer):
    """
    Serializer para validar la entrada de datos, no necesariamente ligado a un modelo.
    Actúa como un DTO (Data Transfer Object).
    """
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)