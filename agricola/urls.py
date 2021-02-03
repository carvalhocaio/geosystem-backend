from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# SDP / Plano
router.register(r'plano-cadastro', PlanoCadastroViewSet)
router.register(r'plano-execucao', PlanoExecucaoViewSet)
router.register(r'plano-log', PlanoLogViewSet)

# SDP / Talhão
router.register(r'talhao-fazenda', TalhaoFazendaViewSet)
router.register(r'talhao-cadastro', TalhaoCadastroViewSet)
router.register(r'talhao-geometria', TalhaoGeometriaViewSet)

# SDP / Paleta de Cores
router.register(r'paleta-cadastro', PaletaCadastroViewSet)
router.register(r'paleta-cor', PaletaCorViewSet)

# SDP / Atributos
router.register(r'atributo-categoria', AtributoCategoriaViewSet)
router.register(r'atributo-calculo', AtributoCalculoViewSet)
router.register(r'atributo-cadastro', AtributoCadastroViewSet)
router.register(r'atributo-alias', AtributoAliasViewSet)
router.register(r'atributo-cor', AtributoCorViewSet)
router.register(r'atributo-enumeracao', AtributoEnumeracaoViewSet)

# SDP / Interpolação
router.register(r'interpolacao-tipo', InterpolacaoTipoViewSet)
router.register(r'interpolacao-cadastro', InterpolacaoCadastroViewSet)
router.register(r'interpolacao-abrangencia', InterpolacaoAbrangenciaViewSet)
router.register(r'interpolacao-talhao', InterpolacaoTalhaoViewSet)
router.register(r'interpolacao-ponto', InterpolacaoPontoViewSet)
router.register(r'interpolacao-geometria', InterpolacaoGeometriaViewSet)
router.register(r'interpolacao-lote', InterpolacaoLoteViewSet)
router.register(r'interpolacao-lote-ponto', InterpolacaoLotePontoViewSet)

# SDP / Fórmula
router.register(r'formula-cadastro', FormulaCadastroViewSet)

# SDP / Versão
router.register(r'versao-cadastro', VersaoCadastroViewSet)
router.register(r'versao-abrangencia', VersaoAbrangenciaViewSet)
router.register(r'versao-atributo', VersaoAtributoViewSet)
router.register(r'versao-geometria', VersaoGeometriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
