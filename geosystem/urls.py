from django.urls import path
from geosystem.views import *

urlpatterns = [
    path('atributo/index/', AtributoIndexViewSet.as_view()),
    path('interpolacao/index/', InterpolacaoIndexViewSet.as_view()),
    path('interpolacao/mapa-arquivo/', UploadFilesViewSet.as_view()),
    path('interpolacao/geometria/', GeometriaViewSet.as_view()),
    path('interpolacao/lote/', InterpolacaoLoteViewSet.as_view()),
    path('interpolacao/mapa/', InterpolacaoMapaViewSet.as_view()),
    path('interpolacao/lote/insert/', InterpolacaoLoteInsertViewSet.as_view()),
    path('interpolacao/json/', InterpolacaoJsonViewSet.as_view()),
    path('interpolacao/legenda-json/', InterpolacaoLegendaJsonViewSet.as_view()),
    path('lote/index/', LoteIndexViewSet.as_view()),
    path('lote/mapa/', UploadLoteViewSet.as_view()),
    path('lote/insert/', LoteInsertViewSet.as_view()),
    path('lote/gerarInterpolacao/', LoteAutoViewSet.as_view()),
    path('lote/abrangencia/', LoteAbrangenciaViewSet.as_view()),
    path('talhao/interpolacao/', TalhaoInterpolacaoViewSet.as_view()),
    path('talhao/insert/', TalhaoInsertViewSet.as_view()),
]
