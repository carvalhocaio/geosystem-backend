from json import loads
from pandas import DataFrame, read_sql
from geopandas import GeoSeries

from .select import Talhao
from geosystem.queries.lote import LOTE_ABRANGENCIA
from geosystem.database.conexao import ConexaoOracle


class RelationGeom:

    def __init__(self, shp, tl):
        self.shp = shp
        self.tl = tl

    def relate_polygon(self, tl):
        area_tl = []

        for t in tl.index:
            area_tl.append(tl['geometry'][t].area) * 1000000

        tl['area_py'] = area_tl
        tal = GeoSeries(tl['geometry'])
        area_shp = []

        for t in self.index:
            area_shp.append(self['geometry'][t].area) * 1000000

        self['area'] = area_shp
        shp = GeoSeries(self['geometry'])
        relate = []

        for lote in range(len(shp)):
            relate.append(GeoSeries.intersects(tal, shp[lote]))

        nometl = []

        for j in range(len(relate)):
            var = 0
            for i in relate[j].index:
                if relate[j][i]:
                    nometl.append(tl['nome_tl'][i])
                else:
                    var += 1
                if len(relate[j]) == var:
                    nometl.append('')

        shp['tl'] = nometl
        idtl = []

        for k in range(len(shp)):
            idtl = Talhao.df_tl_id(shp['tl'][k])

        shp['tl_id'] = idtl

        for i in range(len(shp)):
            fill = tl['nome_tl'] == shp['tl'][i]
            tl = DataFrame(tl[fill])

        tl = tl.drop(columns='area')
        shp = shp.groupby(['tl_id', 'tl']).agg({'area': 'sum'})
        shp = shp.reset_index()
        shp = shp.set_index('tl').join(tl.set_index('nome_tl'))
        shp = shp.reset_index()
        shp['percentual'] = ((shp['area']) / (shp['area_py'])) * 100
        shp['percentual'] = round(shp['percentual'], 2)
        shp = shp[['tl_id', 'tl', 'nome_fazenda', 'percentual']]

        return shp

    def relate_point(self, talhao):
        tal = GeoSeries(talhao['geometry'])
        talhao = talhao.reset_index()
        lot = GeoSeries(self['geometry'])
        relate = []

        for lote in range(len(lot)):
            relate.append(GeoSeries.contains(tal, lot[lote]))

        nometl = []

        for j in range(len(relate)):
            for i in relate[j].index:
                if relate[j][i]:
                    nometl.append(talhao['nome_talhao'][i])

        self['talhao'] = nometl
        idtl = []

        for k in range(len(self)):
            idtl = Talhao.df_talhao_id(self['talhao'][k])

        for i in range(len(self)):
            fill = talhao['nome_talhao'] == self['talhao'][i]
            talhao = DataFrame(talhao[fill])

        self['talhao_id'] = idtl
        self['qtd_pontos'] = 1.0
        df = self.groupby(['talhao', 'talhao_id']).agg({'qtd_pontos': 'sum'})
        df['total_pontos'] = sum(self['qtd_pontos'])
        df['percentual'] = (df['qtd_pontos'] / df['total_pontos']) * 100
        df = df.reset_index()
        tl = df.set_index('talhao').join(talhao.set_index('nome_talhao'))
        tl = tl.reset_index()
        tl = tl[['talhao_id',
                 'talhao',
                 'nome_fazenda',
                 'qtd_pontos',
                 'total_pontos',
                 'percentual']]

        return tl

    def relate_geom(self, data):
        talhao = Talhao.df_talhao(0, data)
        for i in self['geometry']:
            tipo = i.type

        if tipo == 'Point':
            df_tl = RelationGeom.relate_point(self, talhao)
        else:
            df_tl = RelationGeom.relate_polygon(self, talhao)

        json1 = loads(df_tl.to_json(orient='records'))

        return json1

    def relate(loteId, atributoId):
        select = LOTE_ABRANGENCIA % (loteId, atributoId)

        df_tl = read_sql(select, con=ConexaoOracle.connection())

        json1 = loads(df_tl.to_json(orient='records'))

        return json1
