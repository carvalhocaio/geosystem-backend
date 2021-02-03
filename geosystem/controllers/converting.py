from gdal import Open, FPolygonize
from os.path import join, expanduser
from rasterio import open as rast_open
from osgeo.osr import SpatialReference
from osgeo.ogr import GetDriverByName, FieldDefn, OFTReal
from shapely.geometry import LineString

from pandas import DataFrame
from geopandas import overlay, read_file, GeoDataFrame
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

from geosystem.maps.util import DelDist
from geosystem.controllers.select import Talhao, JSON
from geosystem.controllers.coordenadas import ConvertCoords
from geosystem.controllers.interpolacao import Interpolacao


class Convertion:
    """
    Define as propriedades da imagem
    """

    def __init__(self):
        pass

    def to_tif(self, lomin, lomax, lamin, lamax, file):
        west, south = lomin - 0.005, lomax + 0.005
        east, north = lamin - 0.005, lamax + 0.005
        line1 = LineString([[west, east], [south, east]])
        line2 = LineString([[west, north], [west, east]])
        dataset = rast_open(join(expanduser('~'), 'geosystem', 'lote/') + file + '.png', 'r')
        bands = 1
        data = self
        w = (line1.length / data.shape[0])
        h = (line2.length / data.shape[1])
        transform = (w, 0.0, west, 0.0, h * -1, north)
        crs = {'init': 'epsg:4326'}

        with rast_open(join(expanduser('~'), 'geosystem', 'lote/') + file + '.tif', 'w', driver='GTiff',
                       width=data.shape[0], height=data.shape[1],
                       count=1, dtype=data.dtype, nodata=0,
                       transform=transform, crs=crs) as dst:
            dst.write(data, indexes=bands)

    def to_shapefile(self, paste):
        # self recebe o arquivo shapefile
        # DelDist.Pasta(paste)
        ds = Open(join(expanduser('~'), 'geosystem', 'lote/') + self + '.tif')
        prj = ds.GetProjection()
        srcband = ds.GetRasterBand(1)
        dst_layername = self
        drv = GetDriverByName("ESRI Shapefile")
        dst_ds = drv.CreateDataSource(join(expanduser('~'), 'geosystem', 'lote/') + paste)
        srs = SpatialReference(wkt=prj)
        dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
        raster_field = FieldDefn("valor", OFTReal)
        raster_field.SetWidth(12)
        raster_field.SetPrecision(2)
        dst_layer.CreateField(raster_field)
        FPolygonize(srcband, None, dst_layer, 0, [])

        del ds, srcband, dst_ds, dst_layer

    def intersection(self, inter):
        # self recebe o dataframe do talhao
        inter = inter.dissolve(by='valor', aggfunc='max', as_index=False)
        return overlay(self, inter, how='intersection')

    def gerar_imagem(self, talhaoId, atributoId, data, tipo):
        # self recebe o id do lote
        df_talhao = Talhao.df_talhao(talhaoId, data)
        lomax, lomin, lamax, lamin = ConvertCoords.coords_talhao(talhaoId, data)
        df = JSON.df_lote(self, atributoId)
        namefig = str(self) + '-' + str(atributoId)
        src, trg, xtrg, ytrg, vals = ConvertCoords.coords_proj(df, lomax, lomin, lamax, lamin)
        interpolacao = Interpolacao.interpolacao_imagem(tipo, src, trg, vals, xtrg, ytrg, namefig)
        mxinter = interpolacao.reshape(360, 360)[::-1]
        Convertion.to_tif(mxinter, lomin, lomax, lamin, lamax, namefig)
        Convertion.to_shapefile(namefig, 'shape')
        df_inter = read_file(join(expanduser('~'), 'geosystem', 'lote/shape/') + namefig + '.shp')
        # intersec = Convertion.intersection(df_talhao, df_inter)
        # intersec = Convertion.explode(intersec)
        intersec = overlay(df_talhao, df_inter, how='intersection')
        intersec = intersec.dissolve(by='valor', aggfunc='max', as_index=False)
        # intersec = Convertion.explode(intersec)
        intersec.to_file((join(expanduser('~'), 'geosystem', 'lote/shape/') + namefig + '.shp'), driver='ESRI Shapefile')
        # intersec['atributo'] = atributoId
        # valor = DataFrame([1.0])
        # valor = valor[0]
        # cor = ''

        return intersec

    def explode(self):
        # self recebe indf
        outdf = GeoDataFrame(columns=self.columns)
        for idx, row in self.iterrows():
            if type(row.geometry) == Polygon:
                outdf = outdf.append(row, ignore_index=True)
            if type(row.geometry) == MultiPolygon:
                multdf = GeoDataFrame(columns=self.columns)
                recs = len(row.geometry)
                multdf = multdf.append([row] * recs, ignore_index=True)
                for geom in range(recs):
                    multdf.loc[geom, 'geometry'] = row.geometry[geom]

                outdf = outdf.append(multdf, ignore_index=True)
        return outdf

    # interseccao
    def gerar_inter(self, data):
        # self recebe o id do talhão
        df_talhao = Talhao.df_talhao(self, data)
        df_inter = read_file(join(expanduser('~'), 'geosystem', 'lote/shape/') + 'Shape.shp')
        intersec = overlay(df_talhao, df_inter, how='intersection')
        intersec = intersec.dissolve(by='valor', aggfunc='max', as_index=False)
        intersec = Convertion.explode(intersec)

        return intersec
