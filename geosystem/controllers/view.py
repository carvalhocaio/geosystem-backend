from json import loads
from pandas import read_sql
from geopandas import GeoSeries
from geosystem.maps.map import CreateMap
from geosystem.queries.paleta import PALETA_LEGENDA
from geosystem.database.conexao import ConexaoOracle
from geosystem.queries.interpolacao import VIEW_INTERPOLACAO
from geosystem.controllers.coordenadas import ConvertCoords


class View:
    def __init__(self):
        pass

    def viewinterpolacao(self):
        # self recebe o id do interpolacao
        query = VIEW_INTERPOLACAO % self

        select = read_sql(query, con=ConexaoOracle.connection())

        geom = ConvertCoords.char_to_geometry(select)
        atributo = geom['atributo_id'][0]
        title = 'interpolacao-' + str(geom['interpolacao_id'][0])

        CreateMap.gerar(geom, title, atributo)

        return f'Mapa Gerado => {title} '


class JSONMapa:
    def __init__(self):
        pass

    def jsoninterpolacao(self):
        # self recebe o id do interpolacao
        query = VIEW_INTERPOLACAO % self

        select = read_sql(query, con=ConexaoOracle.connection())

        geom = ConvertCoords.char_to_geometry(select)
        jsonread = geom.to_json()
        jsonread = loads(jsonread)
    
        union = geom.unary_union
        centro = GeoSeries(union.centroid)
        longitude = centro.map(lambda p: p.x)
        latitude = centro.map(lambda p: p.y)
        centroide = {'centroide': [{'latitude': latitude[0], 'longitude': longitude[0]}]}
    
        return jsonread, centroide

    def legendajson(self):
        # self recebe o id da interpolacao
        paleta = PALETA_LEGENDA % self

        legenda = read_sql(paleta, con=ConexaoOracle.connection())

        legenda_json = legenda.to_json(force_ascii=False, orient="records")
        legenda_json = loads(legenda_json)



        return legenda_json
