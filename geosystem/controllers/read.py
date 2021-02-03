from os.path import splitext
from geopandas import read_file, GeoSeries

from .coordenadas import ConvertCoords


class ReadGeom:
    """
    Define as propriedades da leitura de geometria
    """

    def __init__(self):
        pass

    def df_extensao(self):
        return splitext(self)[1]

    def df_gdf(self):
        extensao = ReadGeom.df_extensao(self)
        if extensao == '.csv':
            gdf = ConvertCoords.ler_csv(self)
        elif extensao == '.shp':
            gdf = read_file(self)
            gs = GeoSeries(gdf['geometry'])
            longitude = gs.map(lambda p: p.x)
            latitude = gs.map(lambda p: p.y)
            gdf['Latitude'] = latitude
            gdf['Longitude'] = longitude
        elif extensao == '.xlsx':
            gdf = ConvertCoords.ler_xlsx(self)
        else:
            gdf = 'Extensão não corresponde com a esperada!'

        return gdf
