import json
from re import compile
from numpy import array, vstack, linspace, meshgrid
from pandas import read_csv, to_numeric, DataFrame, read_json, read_sql, read_excel
from shapely import wkt
from warnings import filterwarnings
from geopandas import read_file, GeoSeries, GeoDataFrame, points_from_xy

from geosystem.queries.talhao import TALHAO
from geosystem.database.conexao import ConexaoOracle

filterwarnings('ignore')


class ConvertCoords:
    """
    Define as propriedades das coordenadas
    """

    def __init__(self):
        pass

    def coords_json(self, cod=0):
        v = self
        c = cod
        v = v.reset_index()
        fill = v['index'] == c
        v = v[fill]
        json_geom = v.geometry.to_json()
        json_geom = json.loads(json_geom)
        for feature in json_geom['features']:
            for key, value in feature['geometry'].items():
                if key == 'type':
                    j = ('{"%s": "%s", ' % (key, value))
                elif key == 'coordinates':
                    j += ('"%s": %s}' % (key, value))
        return j

    def coords_list(self, cod=0):
        v = self
        c = cod
        v = v.reset_index()
        fill = v['index'] == c
        v = v[fill]
        json_geom = v.geometry.to_json()
        json_geom = json.loads(json_geom)
        for feature in json_geom['features']:
            for key, value in feature['geometry'].items():
                if key == 'coordinates':
                    j = [value[1], value[0]]
        return j

    def coords_point(self, cod=0):
        v = self
        c = cod
        v = v.reset_index()
        fill = v['index'] == c
        v = v[fill]
        json_geom = v.geometry.to_json()
        json_geom = json.loads(json_geom)
        for feature in json_geom['features']:
            for key, value in feature['geometry'].items():
                if key == 'coordinates':
                    j = (value[1], value[0])
        return j

    def points(self):
        coords = []
        for i in range(len(self)):
            coords.append(ConvertCoords.coords_point(self, i))
        return coords

    def coords_union(self):
        self = self.unary_union
        self = GeoDataFrame(GeoSeries(self))
        self = self.rename(columns={0: 'geometry'}).set_geometry('geometry')
        j = ConvertCoords.coords_json(self)
        return j

    def char_to_geometry(self):
        df = DataFrame(self)
        json = df.to_json()
        dt = read_json(json)
        geometry = dt['geom'].apply(wkt.loads)
        df = dt.drop(['geom'], axis=1)
        geo = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
        return geo

    def coords_talhao(self, dat):
        select = TALHAO % (self, dat)
        lon1 = []
        lat1 = []
        talhao = read_sql(select, con=ConexaoOracle.connection())
        df_talhao = ConvertCoords.char_to_geometry(talhao)
        json_fa = ConvertCoords.coords_json(df_talhao)
        df_fa = read_json(json_fa)

        for j in range(len(df_fa['coordinates'][0])):
            lon1.append(df_fa['coordinates'][0][j][0])
            lat1.append(df_fa['coordinates'][0][j][1])

        # Extraindo Latitude e Longitude máxima e mínima
        long = array(lon1)
        lati = array(lat1)

        return long.max(), long.min(), lati.max(), lati.min()

    def coords_proj(self, lomax, lomin, lamax, lamin, pixel=360):
        lon, lat, val = [], [], []

        for i in range(len(self)):
            lon.append(self['geometry'][i].x)
            lat.append(self['geometry'][i].y)
            val.append(self['valor'][i])

        # Incluindo Listas em array numpy    
        lon, lat, vals = array(lon), array(lat), array(val)
        # Lista de coordenadas origem 
        src = vstack([lon, lat]).transpose()

        # Definindo tamanho da imagem com base nas coordenadas maximas e minimas
        xtrg = linspace(lomin - 0.005, lomax + 0.005, pixel)
        ytrg = linspace(lamin - 0.005, lamax + 0.005, pixel)

        # Definindo Coordenadas dos pontos alvos
        trg = meshgrid(xtrg, ytrg)
        # Lista de coordenadas em pontos alvos
        trg = vstack((trg[0].ravel(), trg[1].ravel())).T

        return src, trg, xtrg, ytrg, vals

    def ler_csv(self):
        # Leitura do arquivo
        csv = read_csv(self, sep=";", encoding="ISO-8859-1", decimal=",")
        search = compile(r'id')
        matches = [x for x in csv.columns if search.match(x)]
        mat = matches[0]

        # Leitura das colunas do arquivo
        for i in csv.columns:
            tipo = csv[i].dtype
            if (i != mat) and (tipo == 'object' or tipo == 'int64' or tipo == 'int32'):
                csv[i] = csv[i].replace('.', ',')
                # Conversão das colunas para numérico
                csv[i] = to_numeric(csv[i], errors='ignore', downcast='float')

        # Leitura das colunas do arquivo
        for i in csv.columns:
            tipo = csv[i].dtype
            if tipo == 'object':
                for j in range(len(csv[i])):
                    # Altera de ponto para em branco
                    csv[i][j] = csv[i][j].replace('.', '')

        # Leitura das colunas do arquivo
        for i in csv.columns:
            tipo = csv[i].dtype
            if tipo == 'object' and (i == 'Latitude' or i == 'Longitude'):
                for j in range(len(csv[i])):
                    # Monta a string para conversão do número de lat/lon
                    csv[i][j] = csv[i][j][0:3] + '.' + csv[i][j][3:]
                # Converte para número
                csv[i] = to_numeric(csv[i])

        # Cria geometria e converte DataFrame para GeoDataFrame
        gdf = GeoDataFrame(csv, geometry=points_from_xy(csv.Longitude, csv.Latitude))

        return gdf

    # Caminho do arquivo xlsx
    def ler_xlsx(self):
        # Leitura do arquivo
        xlsx = read_excel(self)
        search = compile(r'id')
        matches = [x for x in xlsx.columns if search.match(x)]
        mat = matches[0]

        # Leitura das colunas do arquivo
        for i in xlsx.columns:
            tipo = xlsx[i].dtype
            if (i != mat) and (tipo == 'object' or tipo == 'int64' or tipo == 'int32'):
                xlsx[i] = xlsx[i].replace('.', ',')
                # Conversão das colunas para numérico
                xlsx[i] = to_numeric(xlsx[i], errors='ignore', downcast='float')

        # Leitura das colunas do arquivo
        for i in xlsx.columns:
            tipo = xlsx[i].dtype
            if tipo == 'object':
                for j in range(len(xlsx[i])):
                    # Altera de ponto para em branco
                    xlsx[i][j] = xlsx[i][j].replace('.', '')

        # Leitura das colunas do arquivo
        for i in xlsx.columns:
            tipo = xlsx[i].dtype
            if (tipo == 'float32' or tipo == 'float64') and (i == 'Latitude' or i == 'Longitude'):
                xlsx[i] = xlsx[i].astype('object')
                for j in range(len(xlsx[i])):
                    string = str(xlsx[i][j])
                    string = string.replace('.', '')
                    # Monta a string para conversão do numero de lat/lon
                    xlsx[i][j] = string[0:3] + '.' + string[3:]
                    # Converte para número
                xlsx[i] = to_numeric(xlsx[i], errors='ignore', downcast='float')

        # Cria geometria e converte DataFrame para GeoDataFrame
        gdf = GeoDataFrame(xlsx, geometry=points_from_xy(xlsx['Longitude'], xlsx['Latitude']))

        return gdf
