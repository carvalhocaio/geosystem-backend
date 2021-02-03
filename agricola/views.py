from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *


# Create your views here.
# Plano execução de procedures do sistema
class PlanoCadastroViewSet(viewsets.ModelViewSet):
    queryset = PlanoCadastro.objects.all()
    serializer_class = PlanoCadastroSerializer


class PlanoExecucaoViewSet(viewsets.ModelViewSet):
    queryset = PlanoExecucao.objects.all()
    serializer_class = PlanoExecucaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('plano',)


class PlanoLogViewSet(viewsets.ModelViewSet):
    queryset = PlanoLog.objects.all()
    serializer_class = PlanoLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('plano_execucao',)


# SDP / Talhões
class TalhaoFazendaViewSet(viewsets.ModelViewSet):
    queryset = TalhaoFazenda.objects.all()
    serializer_class = TalhaoFazendaSerializer


class TalhaoCadastroViewSet(viewsets.ModelViewSet):
    queryset = TalhaoCadastro.objects.all()
    serializer_class = TalhaoCadastroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('fazenda',)


class TalhaoGeometriaViewSet(viewsets.ModelViewSet):
    queryset = TalhaoGeometria.objects.all()
    serializer_class = TalhaoGeometriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('talhao_cad',)


# SDP / Paleta de Cores
class PaletaCadastroViewSet(viewsets.ModelViewSet):
    queryset = PaletaCadastro.objects.all()
    serializer_class = PaletaCadastroSerializer


class PaletaCorViewSet(viewsets.ModelViewSet):
    queryset = PaletaCor.objects.all()
    serializer_class = PaletaCorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('paleta',)


# SDP / Atributos
class AtributoCategoriaViewSet(viewsets.ModelViewSet):
    queryset = AtributoCategoria.objects.all()
    serializer_class = AtributoCategoriaSerializer


class AtributoCalculoViewSet(viewsets.ModelViewSet):
    queryset = AtributoCalculo.objects.all()
    serializer_class = AtributoCalculoSerializer


class AtributoCadastroViewSet(viewsets.ModelViewSet):
    queryset = AtributoCadastro.objects.all()
    serializer_class = AtributoCadastroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('categoria', 'calculo',)


class AtributoAliasViewSet(viewsets.ModelViewSet):
    queryset = AtributoAlias.objects.all()
    serializer_class = AtributoAliasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('atributo',)


class AtributoCorViewSet(viewsets.ModelViewSet):
    queryset = AtributoCor.objects.all()
    serializers_class = AtributoCorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('atributo', 'paleta',)

    def get_serializer(self, *args, **kwargs):
        """
        Função que permite enviar vários registros em uma requisição
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(AtributoCorViewSet, self).get_serializer(*args, **kwargs)


class AtributoEnumeracaoViewSet(viewsets.ModelViewSet):
    queryset = AtributoEnumeracao.objects.all()
    serializer_class = AtributoEnumeracaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('atributo',)

    def get_serializer(self, *args, **kwargs):
        """
        Função que permite enviar vários registros em uma requisição
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(AtributoEnumeracaoViewSet, self).get_serializer(*args, **kwargs)


# SDP / Interpolação
class InterpolacaoTipoViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoTipo.objects.all()
    serializer_class = InterpolacaoTipoSerializer


class InterpolacaoCadastroViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoCadastro.objects.all()
    serializer_class = InterpolacaoCadastroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('atributo', 'tipo_interpolacao', 'descricao', 'data', 'lote_id')


class InterpolacaoAbrangenciaViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoAbrangencia.objects.all()
    serializer_class = InterpolacaoAbrangenciaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('interpolacao',)

    def get_serializer(self, *args, **kwargs):
        """
        Função que permite enviar vários registros em uma requisição
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(InterpolacaoAbrangenciaViewSet, self).get_serializer(*args, **kwargs)


class InterpolacaoTalhaoViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoTalhao.objects.all()
    serializer_class = InterpolacaoTalhaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('interpolacao',)

    def get_serializer(self, *args, **kwargs):
        """
        Função que permite enviar vários registros em uma requisição
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(InterpolacaoTalhaoViewSet, self).get_serializer(*args, **kwargs)


class InterpolacaoPontoViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoPonto.objects.all()
    serializer_class = InterpolacaoPontoSerializer


class InterpolacaoGeometriaViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoGeometria.objects.all()
    serializer_class = InterpolacaoGeometriaSerializer


class InterpolacaoLoteViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoLote.objects.all()
    serializer_class = InterpolacaoLoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('tipo_interpolacao',)


class InterpolacaoLotePontoViewSet(viewsets.ModelViewSet):
    queryset = InterpolacaoLotePonto.objects.all()
    serializer_class = InterpolacaoLotePontoSerializer


# SDP / Formulas
class FormulaCadastroViewSet(viewsets.ModelViewSet):
    queryset = FormulaCadastro.objects.all()
    serializer_class = FormulaCadastroSerializer


# SDP / Versão
class VersaoCadastroViewSet(viewsets.ModelViewSet):
    queryset = VersaoCadastro.objects.all()
    serializer_class = VersaoCadastroSerializer


class VersaoAbrangenciaViewSet(viewsets.ModelViewSet):
    queryset = VersaoAbrangencia.objects.all()
    serializer_class = VersaoAbrangenciaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('versao',)

    def get_serializer(self, *args, **kwargs):
        """
        Função que permite enviar vários registros em uma requisição
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(VersaoAbrangenciaViewSet, self).get_serializer(*args, **kwargs)


class VersaoAtributoViewSet(viewsets.ModelViewSet):
    queryset = VersaoAtributo.objects.all()
    serializer_class = VersaoAtributoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('versao',)

    def get_serializer(self, *args, **kwargs):
        """
        Função que permite enviar vários registros em uma requisição
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(VersaoAtributoViewSet, self).get_serializer(*args, **kwargs)


class VersaoGeometriaViewSet(viewsets.ModelViewSet):
    queryset = VersaoGeometria.objects.all()
    serializer_class = VersaoGeometriaSerializer
