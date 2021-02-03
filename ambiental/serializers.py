from rest_framework import serializers
from .models import *

class MapaTematicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapaTematico
        fields = '__all__'

class VersaoTemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoTema
        fields = '__all__'


class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'


class VersaoTemaGeometriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoTemaGeometria
        fields = '__all__'


class VersaoTemaAtributoGeometriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoTemaAtributoGeometria
        fields = '__all__'
