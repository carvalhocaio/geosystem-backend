from os import remove
from os.path import isfile, join, expanduser, splitext

from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.clickjacking import xframe_options_exempt

from pandas import read_sql
from pandas.api import extensions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from geosystem.maps.map import CreateMap
from geosystem.maps.util import FileSearch
from geosystem.database.conexao import ConexaoOracle
from geosystem.controllers.lote import Lote
from geosystem.controllers.view import View, JSONMapa
from geosystem.controllers.talhao import RelationGeom
from geosystem.controllers.select import JSON
from geosystem.controllers.insert import InsertTable


# SDP / Upload dos arquivos
class UploadFilesViewSet(APIView):
    """
    Realiza o upload dos arquivos passando o nome do atributo e o id da interpolação
    Os arquivos são salvos como {atributo}-{interpolacaoId}.[extensão]
    Encontram-se no diretório: ~/geosystem/files/
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Função que grava os arquivos no diretório
        @return: grava os arquivos com o nome {atributo}-{interpolacaoId}.[extensão]
        Ex:. calagem-18.shp / calagem-18.shx / calagem-18.dbf
        O mapa é salvo como {atributo}-{interpolacaoId}.html
        Encontra-se no diretório ~/geosystem/mapas/
        Ex:. calagem-18.html
        """
        files_list = request.FILES
        data = request.data
        file_name = data['atributoName'] + '-' + data['interpolacaoId']

        for f in files_list:
            name, extension = splitext(files_list[f].name)
            local_file = join(expanduser('~'), 'geosystem', 'files/')

            if isfile(local_file + file_name + extension):
                remove(local_file + file_name + extension)

            fs = FileSystemStorage(location=join(
                expanduser('~'), 'geosystem', 'files/'))
            fs.save(file_name + extension, files_list[f])

        select = 'SELECT ATRIBUTO_ID FROM INTERPOLACAO_CADASTRO WHERE ID = %s' % data[
            'interpolacaoId']
        atributo_id = read_sql(select, con=ConexaoOracle.connection())
        atributo_id = atributo_id['atributo_id']
        atributo_id = atributo_id[0]

        CreateMap.view_map(file_name, data['interpolacaoId'], atributo_id)
        map = open(join(expanduser('~'), 'geosystem',
                        'mapas/' + file_name + '.html'), 'rb')

        print(atributo_id)
        return FileResponse(map)

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        data = request.data
        file_name = request.GET.get(
            'atributoName') + '-' + request.GET.get('interpolacaoId')
        mapa = open(join(expanduser('~'), 'geosystem',
                         'mapas/' + file_name + '.html'), 'rb')

        return FileResponse(mapa)


# SDP / Lote
class UploadLoteViewSet(APIView):
    """
    Realiza o upload dos arquivos passando o id do lote.
    Os arquivos são salvos como lote-{loteId}.[extensão]
    Encontram-se no diretório: ~/geosystem/lote/
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Função que grava os arquivos no diretório e gera o mapa
        @return: grava os arquivos com o nome lote-{loteId}.[extensão]
        Ex:. lote-18.csv / lote-19.xlsx / lote-16.dbf / lote-16.shp / lote-16.shx
        O mapa é salvo como lote-{loteId}.html
        Encontra-se no diretório ~/geosystem/mapas/
        """

        files_list = request.FILES
        data = request.data
        file_name = 'lote-' + data['loteId']
        extension = None

        for f in files_list:
            name, extension = splitext(files_list[f].name)
            local_file = join(expanduser('~'), 'geosystem', 'lote/')

            if isfile(local_file + file_name + extension):
                remove(local_file + file_name + extension)

            fs = FileSystemStorage(location=join(
                expanduser('~'), 'geosystem', 'lote/'))
            fs.save(file_name + extension, files_list[f])

        if 1 == len(files_list):
            file = file_name + extension
        else:
            file = file_name + '.shp'

        Lote.lote_mapa(file, data['loteId'])
        map = open(join(expanduser('~'), 'geosystem', 'mapas/' + file_name + '.html'), 'rb')

        return FileResponse(map)

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        """
        Função que retorna o mapa do lote passado o id do lote via query param
        Endpoint: ~/lote/mapa/?loteId={loteId}
        """
        data = request.data
        file_name = 'lote-' + request.GET.get('loteId')
        map = open(join(expanduser('~'), 'geosystem',
                        'mapas/' + file_name + '.html'), 'rb')

        return FileResponse(map)


class LoteInsertViewSet(APIView):

    def post(self, request):
        """
        Função que grava as informações do lote no banco de dados passando o nome do arquivo e o id do lote
        """
        data = request.data
        lote = request.data['loteId']

        file = FileSearch.search('lote-' + str(lote))
        save = Lote.lote_insert(file, lote)

        return Response(save)


class LoteAbrangenciaViewSet(APIView):

    def get(self, request):
        data = request.data
        lote = request.GET.get('loteId')
        atributo = request.GET.get('atributoId')
        # date = request.GET.get('data')

        # df = JSON.df_lote(lote, atributo)
        # rg = RelationGeom.relate_geom(df, date)

        rg = RelationGeom.relate(lote, atributo)

        return Response(rg)


class LoteIndexViewSet(APIView):

    def get(self, request):
        """
        Retorna o nome dos atributos ao invés do IDs. Usado na tela de cadastro de atributo
        Endpoint: ~/geosystem/lote/index/
        """
        data = request.data
        lote = request.GET.get('loteId')
        atributo = request.GET.get('atributoId')
        classificado = request.GET.get('classificado')

        if classificado:
            valida = 'true'
        else:
            valida = 'false'

        if lote:
            index = JSON.index('Lote', lote, valida)
        else:
            index = JSON.index('Lote', lote=0, nulo=valida)

        return Response(index)


class LoteAutoViewSet(APIView):

    def post(self, request):
        data = request.data
        lote_id = data['loteId']

        InsertTable.insert_auto(lote_id)

        return Response(f'Lote {lote_id} gerado')


# SDP / Geometria
class GeometriaViewSet(APIView):

    def post(self, request):
        """
        Função que salva a geometria da interpolação passando o nome do atributo e o id da interpolação
        """
        data = request.data
        atributo = request.data['atributoName']
        interpolacao_id = request.data['interpolacaoId']
        save = InsertTable.interpolacao(
            atributo + '-' + interpolacao_id, interpolacao_id)

        return Response(save)


class TalhaoInterpolacaoViewSet(APIView):
    """
    Realiza a interpolação do talhão passando o nome da interpolacao e o id da interpolacao
    Ex: {
        "interpolacao": "calagem"
        "interpolacaoId": 18
    }
    """

    def get(self, request):
        data = request.data
        interpolacao = request.GET.get('interpolacao')
        interpolacao_id = request.GET.get('interpolacaoId')
        save = JSON.talhao_interpolacao(interpolacao, interpolacao_id)

        return Response(save)


class TalhaoInsertViewSet(APIView):
    """
    Realiza o insert das informações do talhão no banco de dados, passando o talhão o id da fazenda
    o ano safra e a data inicial
    """

    def post(self, request):
        data = request.data
        talhao = request.data['talhao']
        fazenda = request.data['fazendaId']
        safra = request.data['safra']
        data_ini = request.data['dataIni']

        save = InsertTable.talhao(
            talhao, fazenda, safra, data_ini, data_fim=None)

        return Response(save)


class AtributoIndexViewSet(APIView):

    def get(self, request):
        """
        Retorna o nome dos atributos ao invés do IDs. Usado na tela de cadastro de atributo
        Endpoint: ~/api/atributo/index/
        """
        data = request.data
        save = JSON.index('Atributo')
        return Response(save)


class InterpolacaoIndexViewSet(APIView):

    def get(self, request):
        """
        Retorna o nome ao invés do IDs. Usado na tela de cadastro de interpolação
        Endpoint: ~/api/interpolacao/index/
        """
        data = request.data
        save = JSON.index('Interpolacao')
        return Response(save)


class InterpolacaoLoteInsertViewSet(APIView):

    def post(self, request):
        """
        Função que salva a interpolação do lote enviando como parâmetro o id da interpolacao
        """
        data = request.data
        interpolacao = data['interpolacaoId']

        select = 'SELECT LOTE_ID, ATRIBUTO_ID FROM INTERPOLACAO_CADASTRO WHERE ID = %s' % interpolacao
        var = read_sql(select, con=ConexaoOracle.connection())
        # save = InsertTable.interpolacao_lote(interpolacao)
        # save = Lote.load_shapefile(interpolacao)
        lote = var['lote_id'][0]
        atributo = var['atributo_id'][0]

        save = InsertTable.load_shapefile(interpolacao, lote, atributo)

        return Response(save)


class InterpolacaoLoteViewSet(APIView):

    def post(self, request):
        """
        Função que gera o mapa da interpolacao do lote
        """
        data = request.data
        lote = data['loteId']
        talhao = data['talhaoId']
        date = data['data']
        atributo = data['atributoId']

        file_name = 'interpolacao-' + str(atributo)

        CreateMap.gera_multmap(lote, talhao, date, 'IDW', atributo)
        mapa = open(join(expanduser('~'), 'geosystem',
                         'mapas/' + file_name + '.html'), 'rb')

        return FileResponse(mapa)

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        data = request.data
        atributo = request.GET.get('atributoId')
        file_name = 'interpolacao-' + str(atributo)
        mapa = open(join(expanduser('~'), 'geosystem',
                         'mapas/' + file_name + '.html'), 'rb')

        return FileResponse(mapa)


class InterpolacaoMapaViewSet(APIView):

    def get(self, request):
        data = request.data
        interpolacao_id = request.GET.get('interpolacaoId')
        file_name = 'interpolacao-' + str(interpolacao_id)

        View.viewinterpolacao(interpolacao_id)
        map = open(join(expanduser('~'), 'geosystem',
                        'mapas/' + file_name + '.html'), 'rb')

        return FileResponse(map)


class InterpolacaoJsonViewSet(APIView):

    def get(self, request):
        data = request.data
        interpolacao_id = request.GET.get('interpolacaoId')

        json = JSONMapa.jsoninterpolacao(interpolacao_id)

        return Response(json)


class InterpolacaoLegendaJsonViewSet(APIView):

    def get(self, request):
        data = request.data
        interpolacao_id = request.GET.get('interpolacaoId')

        json = JSONMapa.legendajson(interpolacao_id)

        return Response(json)
