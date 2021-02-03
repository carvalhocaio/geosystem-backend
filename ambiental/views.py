from os import remove
from os.path import isfile, join, expanduser, splitext

from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.clickjacking import xframe_options_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from geosystem.maps.map import CreateMap

from .serializers import *
from rest_framework import viewsets


class MapaTematicoViewSet(viewsets.ModelViewSet):
    queryset = MapaTematico.objects.all()
    serializer_class = MapaTematicoSerializer


class VersaoTemaViewSet(viewsets.ModelViewSet):
    queryset = VersaoTema.objects.all()
    serializer_class = VersaoTemaSerializer


class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer


class VersaoTemaGeometriaViewSet(viewsets.ModelViewSet):
    queryset = VersaoTemaGeometria.objects.all()
    serializer_class = VersaoTemaGeometriaSerializer


class VersaoTemaAtributoGeometriaViewSet(viewsets.ModelViewSet):
    queryset = VersaoTemaAtributoGeometria.objects.all()
    serializer_class = VersaoTemaAtributoGeometriaSerializer


# ---

class UploadTemaViewSet(APIView):
    """
    Realiza o upload dos arquivos para Tema.
    Os arquivos são salvos no diretorio: ~/geosystem/tema/
    """

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        file_list = request.FILES
        data = request.data
        versao_id = data['versaoId']
        file_name = 'versao-' + str(versao_id)

        for f in file_list:
            name, extension = splitext(file_list[f].name)
            local_file = join(expanduser('~'), 'geosystem', 'tema/')

            if isfile(local_file + file_name + extension):
                remove(local_file + file_name + extension)

            fs = FileSystemStorage(location=join(expanduser('~'), 'geosystem', 'tema/'))
            fs.save(file_name + extension, file_list[f])

        CreateMap.gerar_tema(versao_id)
        map = open(join(expanduser('~'), 'geosystem', 'tema/' + file_name + '.html'), 'rb')

        return Response(map)

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        data = request.data
        versao_id = request.GET.get('versaoId')
        file_name = 'versao-' + versao_id
        format = request.GET.get('format')

        if not format:
            map = open(join(expanduser('~'), 'geosystem', 'tema/' + file_name + '.html'), 'rb')
            return FileResponse(map)
        elif format == 'json':
            map = CreateMap.tema_json(versao_id)
            return Response(map)
        else:
            return Response('Não foi possível realizar a requisição!')


class TemaInsertViewSet(APIView):

    def post(self, request):
        data = request.data
        versao_id = request.data['versaoId']

        InsertTable.load_tema(versao_id)

        return f'Versão - {versao_id}'
