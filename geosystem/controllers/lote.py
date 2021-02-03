import os
from os.path import join, expanduser
from decouple import config

from .read import ReadGeom
from .insert import InsertTable

from pandas import read_sql
from geosystem.maps.map import CreateMap
from geosystem.database.conexao import ConexaoOracle
from datetime import datetime
from geosystem.maps.util import ListaHead

from geosystem.queries.lote import INSERT_INTER_LOTE


class Lote:
    def __init__(self):
        pass

    def lote_mapa(self, lote_id):
        """
        Função que gera o mapa do lote passando o nome do arquivo e o id do lote.
        O mapa é salvo como lote-{lote_id}.html
        Para visualização do mapa é utilizado método GET passando o id do lote via query param
        @param self: recebe o nome do lote
        @param lote_id: recebe o id do lote
        @return: gera o mapa e salva no diretório ~/geosystem/mapas/ com extensão .html
        """
        file = join(expanduser('~'), 'geosystem', 'lote/')
        df = ReadGeom.df_gdf(file + self)
        return CreateMap.gerar_point(df, 'lote-' + lote_id)

    def lote_insert(self, lote_id):
        """
        Função que faz o insert do lote no banco de dados passando o nome do arquivo e o id do lote
        @param self: recebe o nome do arquivo
        @param lote_id: recebe o id do lote
        @return: grava as informações no banco de dados
        """
        file = join(expanduser('~'), 'geosystem', 'lote/')
        df = ReadGeom.df_gdf(file + self)
        return InsertTable.lote(df, lote_id)
