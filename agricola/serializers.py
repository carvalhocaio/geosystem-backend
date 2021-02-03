from rest_framework import serializers
from .models import *


# Plano Execução procedures do sistema
class PlanoCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoCadastro
        fields = '__all__'


class PlanoExecucaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoExecucao
        fields = '__all__'


class PlanoLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoLog
        fields = '__all__'


class TalhaoFazendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalhaoFazenda
        fields = '__all__'


# SDP / Talhões
class TalhaoCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalhaoCadastro
        fields = '__all__'


class TalhaoGeometriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalhaoGeometria
        fields = '__all__'


# SDP / Paleta de Cores
class PaletaCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletaCadastro
        fields = '__all__'


class PaletaCorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletaCor
        fields = '__all__'


# SDP / Atributos
class AtributoCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCategoria
        fields = '__all__'


class AtributoCalculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCalculo
        fields = '__all__'


class AtributoCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCadastro
        fields = '__all__'


class AtributoAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoAlias
        fields = '__all__'


class AtributoCorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoCor
        fields = '__all__'


class AtributoEnumeracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoEnumeracao
        fields = '__all__'


# SDP / Interpolação
class InterpolacaoTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoTipo
        fields = '__all__'


class InterpolacaoCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoCadastro
        fields = '__all__'


class InterpolacaoAbrangenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoAbrangencia
        fields = '__all__'


class InterpolacaoTalhaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoTalhao
        fields = '__all__'


class InterpolacaoPontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoPonto
        fields = '__all__'


class InterpolacaoGeometriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoGeometria
        fields = '__all__'


class InterpolacaoLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoLote
        fields = '__all__'


class InterpolacaoLotePontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolacaoLotePonto
        fields = '__all__'


# SDP / Fórmulas
class FormulaCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaCadastro
        fields = '__all__'


# SDP / Versão
class VersaoCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoCadastro
        fields = '__all__'


class VersaoAbrangenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoAbrangencia
        fields = '__all__'


class VersaoAtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoAtributo
        fields = '__all__'


class VersaoGeometriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoGeometria
        fields = '__all__'
