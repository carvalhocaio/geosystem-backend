from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# Mapa Temático
router.register(r'mapa-tematico', MapaTematicoViewSet)
router.register(r'versao-tema', VersaoTemaViewSet)
router.register(r'atributo', AtributoViewSet)
router.register(r'versao-tema-geometria', VersaoTemaGeometriaViewSet)
router.register(r'versao-tema-atributo-geometria', VersaoTemaAtributoGeometriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tema/', UploadTemaViewSet.as_view()),
    path('tema/insert/', TemaInsertViewSet.as_view())
]
