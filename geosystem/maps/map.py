from re import compile
from os.path import join, expanduser
from json import loads
from shapely.geometry import box

from folium import Map, LayerControl
from folium.plugins import MousePosition, FloatImage
from folium.features import GeoJsonTooltip, GeoJson
from folium.vector_layers import Circle
from folium.raster_layers import TileLayer

from pandas import DataFrame, read_sql
from geopandas import GeoSeries, read_file

from .util import ListaHead, RemoveAcento

from geosystem.colors.color import PaletaColor
from geosystem.database.conexao import ConexaoOracle
from geosystem.controllers.dataframe import CampoDataFrame
from geosystem.controllers.insert import InsertTable
from geosystem.controllers.select import Talhao
from geosystem.controllers.converting import Convertion
from geosystem.controllers.coordenadas import ConvertCoords

from geosystem.queries.ambiental import \
    SELECT_AMB_GEOMETRIA, \
    SELECT_AMB_POLIGONO, \
    SELECT_AMB_LINHA, \
    SELECT_AMB_PONTO


class CreateMap:

    def __init__(self):
        pass

    def style_tema(tema):
        conn = ConexaoOracle.connection(user=1)
        # tema = 1
        geom = SELECT_AMB_GEOMETRIA % tema
        tipo = read_sql(geom, con=conn)
        tipo = tipo['tipo_geometria'][0]

        if tipo == 'PL':
            poly = SELECT_AMB_POLIGONO % tema
            config = read_sql(poly, con=conn)
            conf = config.to_json(orient="records")
            conf = loads(conf)
            conf = conf[0]

            return lambda features: {
                "fillColor": conf['cor_fundo'],
                "fillOpacity": conf['opacidade'],
                "color": conf['cor_linha'],
                "weight": int(conf['tamanho_linha']),
                "dashArray": conf['tipo_linha'],
            }
        elif tipo == 'LH':
            lin = SELECT_AMB_LINHA % tema
            config = read_sql(lin, con=conn)
            conf = config.to_json(orient="records")
            conf = loads(conf)
            conf = conf[0]
            return lambda features: {
                "color": conf['cor_linha'],
                "weight": conf['tamanho_linha'],
                "dashArray": conf['tipo_linha']
            }
        elif tipo == 'PT':
            pont = SELECT_AMB_PONTO % tema
            config = read_sql(pont, con=conn)
            conf = config.to_json(orient="records")
            conf = loads(conf)
            if config['tipo_ponto'] == 'C':
                return lambda features: {
                    "fillColor": conf['cor_ponto'],
                    "radius": conf['tamanho_ponto'],
                }
            else:
                return lambda features: {
                    "markerColor": config['cor_ponto'],
                }

    def style_json(tema):
        conn = ConexaoOracle.connection(user=1)
        # tema = 1
        geom = SELECT_AMB_GEOMETRIA % tema
        tipo = read_sql(geom, con=conn)
        tipo = tipo['tipo_geometria'][0]

        if tipo == 'PL':
            poly = SELECT_AMB_POLIGONO % tema
            config = read_sql(poly, con=conn)
            conf = config.to_json(orient="records")
            conf = loads(conf)
            conf = conf[0]
            return conf
        elif tipo == 'LH':
            lin = SELECT_AMB_LINHA % tema
            config = read_sql(lin, con=conn)
            conf = config.to_json(orient="records")
            conf = loads(conf)
            conf = conf[0]
            return conf
        elif tipo == 'PT':
            pont = SELECT_AMB_PONTO % tema
            config = read_sql(pont, con=conn)
            conf = config.to_json(orient="records")
            conf = loads(conf)
            return conf

    def style_function(self, dfdict):
        return lambda features: {
            "fillColor": self(dfdict[features['properties']['index']]),
            "color": "black",
            'weight': 0.0,
            "fillOpacity": 0.4,
        }

    def table_html(self, num=0):
        html = ''
        head = ListaHead.list_head(self)
        floats = CampoDataFrame.floats(self)
        search = compile(r'id')
        matches = [x for x in self[head] if search.match(x)]
        mat = matches[0]
        valores = []
        jhead = []
        df1 = []
        div = 5
        qtd = int(len(floats) / div) + 1

        for i in range(qtd):
            x = i * div
            if i != div:
                y = x + div
            else:
                y = None

            id_amostra = DataFrame(self[mat]).reset_index()
            go = (DataFrame(self[floats[x:y]]).reset_index())
            joins = id_amostra.set_index('index').join(go.set_index('index'))
            jhead.append(ListaHead.list_head(joins))
            df_tipo = joins[jhead[i]]
            valores.append(df_tipo)

        for j in range(len(valores)):
            df1.append(DataFrame(valores[j][jhead[j]]))

        for i in range(len(df1)):
            ht = df1[i].loc[num:num]
            html += ht.to_html(classes='table table-sm table-striped table-responsive-md small text-right', border=0,
                               index=False, col_space=0, decimal=',')

        return html

    # Cria Mapa dinamicammente
    def gerar_alt(self, title, atributoId):
        title = RemoveAcento.format_title(title)
        shape_reset = self.reset_index()  # Cria coluna de index
        var2 = shape_reset  # Cria copia do shape com index
        head = ListaHead.list_head(shape_reset)  # Lista itens do shape
        head3 = ListaHead.list_index(var2)  # Lista itens do shape com index
        df_dict = var2.set_index(head3[0])['valor']  # Cria lista de valores
        union = shape_reset.unary_union  # Union das geometria
        centro = GeoSeries(union.centroid)  # Extraindo o centroide da union
        longitude = centro.map(lambda p: p.x)  # Extraindo Longitude do centroide
        latitude = centro.map(lambda p: p.y)  # Extraindo Latitude do centroide
        var = shape_reset.to_json()  # Convertendo o ShapeFile em JSON

        colormap = PaletaColor.paleta_map(atributoId)

        # Cria mapa básico
        m = Map(
            location=[latitude, longitude],
            zoom_start=15,
            tiles='OpenStreetMap',
            control_scale=True
        )

        # Logo Scheffer
        url = 'http://sda/arquivos/scheffer.png'
        FloatImage(url, bottom=5, left=75).add_to(m)

        # Visualização do Google Maps
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='Google Maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Visualização do Google Street
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='Google StreetView',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Formato de dados para localização
        formatter = "function(num) {return L.Util.formatNum(num, 3);};"

        # Geolocalização no ponteiro do mouse
        MousePosition(
            separator=' | ',
            empty_string='NaN',
            lng_first=True,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Tooltip com as informações das geometrias
        tooltip = GeoJsonTooltip(
            fields=head,
            aliases=head,
            localize=True,
            sticky=False,
            labels=True,
            style="box-shadow: 1px 1px 5px; font-family: Arial, Helvetica, sans-serif;",
            max_width=800,
        )

        GeoJson(
            var,
            name=title,
            style_function=CreateMap.style_function(colormap, df_dict),
            tooltip=tooltip,
        ).add_to(m)

        # Legenda de cores
        m.add_child(colormap)
        # Botão de controle de camadas
        LayerControl().add_to(m)
        # Diretório do mapa
        m.save(join(expanduser('~'), 'geosystem', 'mapas/') + title + '.html')

    # Cria Mapa dinamicammente
    def gerar_point(self, title):
        shape_reset = self.reset_index()  # Cria coluna de index
        list_points = ConvertCoords.points(shape_reset)
        var2 = shape_reset  # Cria cópia do shape com index
        head = ListaHead.list_head(shape_reset)  # Lista itens do shape
        head3 = ListaHead.list_index(var2)  # Lista itens do shape com index
        search = compile(r'id')
        matches = [x for x in self[head] if search.match(x)]
        mat = matches[0]
        df_dict = var2.set_index(head3[0])[mat]  # Cria lista de valores
        union = shape_reset.unary_union  # Union das geometria
        centro = GeoSeries(union.centroid)  # Extraindo o centroide da union
        longitude = centro.map(lambda p: p.x)  # Extraindo Longitude do centroide
        latitude = centro.map(lambda p: p.y)  # Extraindo Latitude do centroide
        var = shape_reset.to_json()  # Convertendo o ShapeFile em JSON

        # Cria mapa básico
        m = Map(
            location=[latitude, longitude],
            zoom_start=15,
            tiles='OpenStreetMap',
            control_scale=True
        )

        # Logo Scheffer
        url = 'http://sda/arquivos/scheffer.png'
        FloatImage(url, bottom=5, left=75).add_to(m)

        # Visualização do Google Maps
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='Google Maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Visualização do Google Street
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='Google StreetView',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Formato de dados para localização
        formatter = "function(num) {return L.Util.formatNum(num, 3);};"

        # Geolocalização no ponteiro do mouse
        MousePosition(
            separator=' | ',
            empty_string='NaN',
            lng_first=True,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        for i in range(len(list_points)):
            j = i + 1
            df_tipo = shape_reset[i:j]
            df_shape = DataFrame(df_tipo)

            html = CreateMap.table_html(df_shape, i)

            Circle(
                (list_points[i][0], list_points[i][1]),
                radius=20,
                tooltip=html,
                fill=True,
                fillOpacity=0.5,
                fillColor="darkblue",
                icon_color="darkblue",
                color="darkblue",
            ).add_to(m)

        # Controle de camadas
        LayerControl().add_to(m)
        # Diretório do mapa
        m.save(join(expanduser('~'), 'geosystem', 'mapas/') + title + '.html')

    def gera_lote(self, data, df, atributoId):
        # self recebe o id do talhao

        g = df
        t = atributoId

        shape_reset = g.reset_index()  # Cria coluna de index
        var2 = shape_reset  # Cria cópia do shape com index
        h = ListaHead.list_head(shape_reset)  # Lista itens do shape
        head3 = ListaHead.list_index(var2)  # Lista itens do shape com index
        d = var2.set_index(head3[0])['valor']

        colormap = PaletaColor.paleta_map(atributoId)

        var = shape_reset.to_json()
        df_dict = d
        # colormap = color
        title = 'interpolacao-' + str(t)
        head = h

        df_talhao = Talhao.df_talhao(self, data)
        union = df_talhao.unary_union  # Union das geometria
        centro = GeoSeries(union.centroid)  # Extraindo o centroide da union
        longitude = centro.map(lambda p: p.x)  # Extraindo Longitude do centroide
        latitude = centro.map(lambda p: p.y)

        # Cria mapa básico
        m = Map(
            location=[latitude, longitude],
            zoom_start=15,
            tiles='OpenStreetMap',
            control_scale=True
        )

        # Logo Scheffer
        url = 'http://sda/arquivos/scheffer.png'
        FloatImage(url, bottom=5, left=75).add_to(m)

        # Visualização do Google Maps
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='Google Maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Visualização do Google Street
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='Google StreetView',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Formato de dados para localização
        formatter = "function(num) {return L.Util.formatNum(num, 3);};"

        # Geolocalização no ponteiro do mouse
        MousePosition(
            separator=' | ',
            empty_string='NaN',
            lng_first=True,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Tooltip com as informações das geometrias
        tooltip = GeoJsonTooltip(
            fields=head,
            aliases=head,
            localize=True,
            sticky=False,
            labels=True,
            style="box-shadow: 1px 1px 5px; font-family: Arial, Helvetica, sans-serif;",
            max_width=800,
        )

        GeoJson(  # Add dados, titulo, cor e balão de informações das geometrias
            var,
            name=title,
            style_function=CreateMap.style_function(colormap, df_dict),
            tooltip=tooltip,
        ).add_to(m)

        # Legenda de cores
        m.add_child(colormap)
        # Botão de controle de camadas
        LayerControl().add_to(m)
        # Diretório do mapa
        m.save(join(expanduser('~'), 'geosystem', 'mapas/') + title + '.html')

    # Cria Mapa dinamicammente
    def gerar(self, title, atributoId):
        # self recebe o dataframe
        shape_reset = self.reset_index()  # Cria coluna de index
        var2 = shape_reset  # Cria cópia do shape com index
        head = ListaHead.list_head(shape_reset)  # Lista itens do shape
        head3 = ListaHead.list_index(var2)  # Lista itens do shape com index
        df_dict = var2.set_index(head3[0])['valor']  # Cria lista de valores
        union = shape_reset.unary_union  # Union das geometria
        centro = GeoSeries(union.centroid)  # Extraindo o centroide da union
        longitude = centro.map(lambda p: p.x)  # Extraindo Longitude do centroide
        latitude = centro.map(lambda p: p.y)  # Extraindo Latitude do centroide
        var = shape_reset.to_json()  # Convertendo o ShapeFile em JSON

        colormap = PaletaColor.paleta_map(atributoId)

        # Cria mapa básico
        m = Map(
            location=[latitude, longitude],
            zoom_start=15,
            tiles='OpenStreetMap',
            control_scale=True
        )

        # Logo Scheffer
        url = 'http://sda/arquivos/scheffer.png'
        FloatImage(url, bottom=5, left=75).add_to(m)

        # Visualização do Google Maps
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='Google Maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Visualização do Google Street
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='Google StreetView',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Formato de dados para localização
        formatter = "function(num) {return L.Util.formatNum(num, 3);};"

        # Geolocalização no ponteiro do mouse
        MousePosition(
            separator=' | ',
            empty_string='NaN',
            lng_first=True,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Tooltip com as informações das geometrias
        tooltip = GeoJsonTooltip(
            fields=head,
            aliases=head,
            localize=True,
            sticky=False,
            labels=True,
            style="box-shadow: 1px 1px 5px; font-family: Arial, Helvetica, sans-serif;",
            max_width=800,
        )

        GeoJson(
            var,
            name=title,
            style_function=CreateMap.style_function(colormap, df_dict),
            tooltip=tooltip,
        ).add_to(m)

        # Legenda de cores
        m.add_child(colormap)
        # Botão de controle de camadas
        LayerControl().add_to(m)
        # Diretório do mapa
        m.save(join(expanduser('~'), 'geosystem', 'mapas/') + title + '.html')

    def gerar_tema(tema):
        self = read_file(join(expanduser('~'), 'geosystem', 'tema/') + f'versao-{tema}.shp')
        # self recebe o dataframe
        shape_reset = self.reset_index()  # Cria coluna de index
        head = ListaHead.list_head(shape_reset)  # Lista itens do shape
        bounds = shape_reset.total_bounds
        p1 = box(bounds[0], bounds[1], bounds[2], bounds[3])
        centro = GeoSeries(p1.centroid)
        longitude = centro.map(lambda p: p.x)  # Extraindo Longitude do centroide
        latitude = centro.map(lambda p: p.y)  # Extraindo Latitude do centroide
        var = shape_reset.to_json()  # Convertendo o ShapeFile em JSON

        # Cria mapa básico
        m = Map(
            location=[latitude, longitude],
            zoom_start=7,
            tiles='OpenStreetMap',
            control_scale=True
        )

        # Logo Scheffer
        url = 'http://sda/arquivos/scheffer.png'
        FloatImage(url, bottom=5, left=75).add_to(m)

        # Visualização do Google Maps
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='Google Maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Visualização do Google Street
        TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='Google StreetView',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True
        ).add_to(m)

        # Formato de dados para localização
        formatter = "function(num) {return L.Util.formatNum(num, 3);};"

        # Geolocalização no ponteiro do mouse
        MousePosition(
            separator=' | ',
            empty_string='NaN',
            lng_first=True,
            num_digits=20,
            prefix='Coordinates:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Tooltip com as informações das geometrias
        tooltip = GeoJsonTooltip(
            fields=head,
            aliases=head,
            localize=True,
            sticky=False,
            labels=True,
            style="box-shadow: 1px 1px 5px; font-family: Arial, Helvetica, sans-serif;",
            max_width=800,
        )

        GeoJson(
            var,
            name='versao-' + str(tema),
            style_function=CreateMap.style_tema(tema),
            tooltip=tooltip,
        ).add_to(m)

        LayerControl().add_to(m)
        m.save(join(expanduser('~'), 'geosystem', 'tema/') + 'versao-' + str(tema) + '.html')

    # Gera mapa de forma resumida
    def generate_map(self, atributoId):
        # self recebe o nome do arquivo ~/files
        origem = (join(expanduser('~'), 'geosystem', 'files/') + self + '.shp')  # Pasta de origem
        shape = read_file(origem)  # Leitura do arquivo
        title = self  # Extraindo título do Arquivo

        return CreateMap.gerar(shape, title, atributoId)  # Executando Função para gerar mapa

    def view_map(self, interId, atributoId):  # Gera mapa de forma resumida
        # self recebe o nome do arquivo
        origem = (join(expanduser('~'), 'geosystem', 'files/') + self + '.shp')  # Pasta de origem
        shape = InsertTable.interseccao(self, interId)  # Leitura do arquivo, gerando a intersecção com o talhão
        title = self  # Extraindo titulo do Arquivo

        return CreateMap.gerar(shape, title, atributoId)  # Executando Função para gerar mapa

    def gera_multmap(self, talhaoId, data, tipo, atributoId):
        # self recebe o id do lote
        geom, nomefig = Convertion.gerar_imagem(self, talhaoId, atributoId, data, tipo)
        CreateMap.gera_lote(talhaoId, data, geom, atributoId)

        return 'O mapa foi gerado com êxito!'

    def tema_json(self):
        style = CreateMap.style_json(self)
        rd = read_file(join(expanduser('~'), 'geosystem', 'tema/') + f'versao-{self}.shp')
        var_json = rd.to_json()
        var_json = loads(var_json)
        return var_json, style
