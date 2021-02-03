from json import loads
from pandas import read_sql
from os.path import join, expanduser
from numpy.ma import masked_invalid
from warnings import filterwarnings
from geopandas import read_file, GeoSeries, GeoDataFrame, points_from_xy
from wradlib.ipol import Idw, Nearest, Linear, OrdinaryKriging
from matplotlib.pyplot import axis, figure, savefig

from geosystem.database.conexao import ConexaoOracle
from geosystem.controllers.coordenadas import ConvertCoords

from geosystem.queries.lote import LOTE_INDEX, \
    SELECT_LOTE_INT, SELECT_LOTE_DATA, LOTE_TALHAO, LOTE_INDEX_NULL, LOTE_AUTO
from geosystem.queries.talhao import SELECT_TALHAO, TALHAO_ID, TALHAO, TALHAO_ALL
from geosystem.queries.atributo import ATRIBUTO_INDEX
from geosystem.queries.interpolacao import INTERPOLACAO_INDEX, INTERPOLACAO_LOTE

filterwarnings('ignore')


class JSON:

    def __init__(self, var):
        self.var = var

    def talhao_interpolacao(self, interpolacao_id):
        """
        Função que define o talhão da interpolação
        @param interpolacao_id: recebe o id da interpolação
        @return: grava as informações da interpolação no talhão
        """
        connect = ConexaoOracle.connection()
        ap = []
        df = read_file(join(expanduser('~'), 'geosystem', 'files/' + self + '.shp'))
        json_tl = ConvertCoords.coords_union(df)
        select = SELECT_TALHAO % (json_tl, interpolacao_id)
        df = read_sql(select, con=connect)
        for i in range(len(df['json_sel'])):
            j = loads(df['json_sel'][i])
            ap.append(j)

        return ap

    def index(self, lote=0, atributo=2,  nulo='false'):
        """
        Função que retorna o index de interpolação e/ou de atributo e/ou de de lote
        É definido a partir da requisição realizada. Ex:.
        GET => ~/api/lote/index
        GET => ~/api/atributo/index
        GET => ~/api/interpolacao/index/
        @return: nome dos parâmetros ao invés dos IDs
        """
        connect = ConexaoOracle.connection()
        ap = []

        if self.upper() == 'INTERPOLACAO':
            select = INTERPOLACAO_INDEX
        elif self.upper() == 'ATRIBUTO':
            select = ATRIBUTO_INDEX
        elif self.upper() == 'LOTE':
            if nulo == 'false':
                select = LOTE_INDEX % (lote, lote, lote, lote, atributo, atributo)
            else:
                select = LOTE_INDEX_NULL % (lote, lote, lote, lote, atributo, atributo)
        df = read_sql(select, con=connect)

        for i in range(len(df['json'])):
            j = loads(df['json'][i])
            new = []
            old = []

            for x in j.keys():
                head1 = x.title().replace('_', '')
                pri = head1[0].lower()
                rest = head1[1:]
                new.append(pri + rest)
                old.append(x)

            for t in range(len(new)):
                j[new[t]] = j[old[t]]
                del j[old[t]]

            ap.append(j)

        return ap

    def df_lote(self, atributoId):
        select = SELECT_LOTE_INT % (self, atributoId)
        lote = read_sql(select, con=ConexaoOracle.connection())
        df_lote = GeoDataFrame(lote, geometry=points_from_xy(lote['longitude'], lote['latitude']))
        df_lote = df_lote.drop('latitude', axis=1)
        df_lote = df_lote.drop('longitude', axis=1)

        return df_lote

    def df_lote_dt(self):
        select = SELECT_LOTE_DATA % self
        dat = read_sql(select, con=ConexaoOracle.connection())
        dat = dat['data_cadastro'][0]

        return dat

    def lote_json(self):
        con = ConexaoOracle.connection()

        ap = []
        select = LOTE_AUTO % self
        df = read_sql(select, con=con)
        for i in range(len(df['json_sel'])):
            j = loads(df['json_sel'][i])
            ap.append(j)
        return ap


class Talhao:

    def __init__(self, var):
        self.var = var

    def df_talhao(self, dat):
        if self == 0:
            select = TALHAO_ALL % dat
        else:
            select = TALHAO % (self, dat)

        talhao = read_sql(select, con=ConexaoOracle.connection())
        df_talhao = ConvertCoords.char_to_geometry(talhao)

        return df_talhao

    def df_talhao_id(self):
        select = TALHAO_ID % self
        df = read_sql(select, con=ConexaoOracle.connection())
        talhao_id = df['id'][0]

        return talhao_id

    def relate_talhao(self, lote_id, dat):
        tl = Talhao.df_talhao(0, dat)
        tal = GeoSeries(tl['geometry'])
        talhao = tl.reset_index()
        lot = GeoSeries(self['geometry'])
        relate = []
        for geometria in range(len(lot)):
            relate.append(GeoSeries.contains(tal, lot[geometria]))
        nometl = []

        for j in range(len(relate)):
            for i in relate[j].index:
                if relate[j][i]:
                    nometl.append(talhao['nome_talhao'][i])
        self['talhao'] = nometl
        idtl = []

        for k in range(len(self)):
            idtl = Talhao.df_talhao_id(self['talhao'][k])
        self['talhao_id'] = idtl

        return self

    def df_talhao_lote(self):
        select = LOTE_TALHAO % self
        talhao = read_sql(select, con=ConexaoOracle.connection())

        return talhao


class Atributo:

    def __init__(self, var):
        self.var = var

    def df_atr(self):
        select = INTERPOLACAO_LOTE % self
        lista_atr = []
        atr = read_sql(select, con=ConexaoOracle.connection())
        for i in range(len(atr)):
            lista_atr.append(atr['descricao_atributo'][i])
        return lista_atr
