from re import compile
from pandas import read_sql, DataFrame
from os import system
from celery import shared_task
from os.path import join, expanduser
from geopandas import read_file, overlay
from decouple import config
from datetime import datetime

from .vertice import DefVertice
from .dataframe import CampoDataFrame, LimpaDataFrame
from .converting import Convertion
from .coordenadas import ConvertCoords

from geosystem.maps.util import RemoveAcento, ListaHead
from geosystem.database.conexao import ConexaoOracle
from geosystem.controllers.select import Talhao, JSON
from geosystem.controllers.talhao import RelationGeom
from geosystem.controllers.converting import Convertion

from geosystem.queries.lote import INSERT_LOTE_PONTOS, INSERT_INTER_LOTE
from geosystem.queries.talhao import INSERT_TALHAO, SELECT_TALHAO_ABRANGENCIA
from geosystem.queries.ambiental import AMB_INSERT_ATRIBUTO, AMB_INSERT_GEOM, AMB_PROCESSO
from geosystem.queries.interpolacao import \
    INSERT_INTERPOLACAO, CADASTRO_AUTOMATICO, \
    SELECT_INTERPOLACAO, ABRANGENCIA_AUTOMATICO


class InsertTable:
    def __init__(self, var):
        self.var = var

    def talhao(self, fazenda, safra, data_ini, data_fim=None):
        # self recebe o talhão
        """
        Função que realiza o insert do talhão no banco de dados
        @param fazenda: recebe o id da fazenda
        @param safra: recebe o ano safra
        @param data_ini: recebe a data inicial
        @param data_fim: recebe como data final a data na qual foi substituído por um novo registro. É definido como padrão 'None'
        @return: grava as informações no banco de dados
        """

        if data_fim is None:
            data_fim = 'NULL'
        df = read_file(join(expanduser('~'), 'geosystem', 'files/' + self + '.shp'))
        df = LimpaDataFrame.limpar(df)
        head = CampoDataFrame.talhao(df)
        campo = CampoDataFrame.valor(df)
        conn = ConexaoOracle.connection().connect()
        m = 0
        gdf = DefVertice.vertice(df)
        for k in range(len(gdf)):
            if head is None:
                tl = ''
            else:
                tl = gdf[head][k]
            json1 = ConvertCoords.coords_json(gdf, k)
            insert = INSERT_TALHAO
            query = insert % (tl, json1, fazenda, data_ini, data_fim, safra)
            query = RemoveAcento.remover(query)
            conn.execute(query)
        return f'Talhão {self} gravado com sucesso!'

    def interpolacao(self, interpolacao):
        """
        Função que realiza o insert da interpolação no banco de dados
        @param interpolacao: recebe o id da interpolação
        @return: grava as informações no banco de dados
        """
        df = read_file(join(expanduser('~'), 'geosystem', 'files/' + self + '.shp'))
        head = CampoDataFrame.talhao(df)
        fazenda = CampoDataFrame.fazenda(df)
        campo = CampoDataFrame.valor(df)
        conn = ConexaoOracle.connection().connect()
        m = 0
        gdf = DefVertice.vertice(df)
        for k in range(len(gdf)):
            if campo == 0:
                valor = 0
            else:
                valor = gdf[campo][k]
            if head is None:
                tl = ''
            else:
                tl = gdf[head][k]
            if fazenda is None:
                fz = ''
            else:
                fz = gdf[fazenda][k]
            json1 = ConvertCoords.coords_json(gdf, k)
            insert = INSERT_INTERPOLACAO
            query = insert % (interpolacao, valor, json1)
            query = RemoveAcento.remover(query)
            conn.execute(query)
        return f'Interpolação {self} gravada com sucesso!'

    def interpolacao_lote(self, namefig):
        """
        Função que realiza o insert da interpolação do lote no banco de dados
        @param self: recebe o id da interpolação
        @return: grava as informações no banco de dados
        """
        # df_tl = Talhao.df_talhao_lote(self)
        # talhao_id = df_tl['talhao_id'][0]
        # data = df_tl['data'][0]
        # df = Convertion.gerar_inter(talhao_id, data)
        df = read_file((join(expanduser('~'), 'geosystem', 'lote/shape/') + namefig + '.shp'))
        campo = CampoDataFrame.valor(df)
        conn = ConexaoOracle.connection().connect()
        session = ConexaoOracle.session(conn)
        gdf = df
        for k in range(len(gdf)):
            valor = gdf['valor'][k]
            json1 = ConvertCoords.coords_json(gdf, k)
            Q = INSERT_INTERPOLACAO % (self, valor, json1)
            query = RemoveAcento.remover(Q)
            session.execute(query)
            print(k)

        session.commit()

        return f'Interpolação do lote {self} gravada com sucesso!'

    def interseccao(self, interpolacao):
        df = read_file(join(expanduser('~'), 'geosystem', 'files/' + self + '.shp'))
        conn = ConexaoOracle.connection().connect()
        valor = CampoDataFrame.valor(df)
        gdf = df
        search = SELECT_TALHAO_ABRANGENCIA % interpolacao
        select = read_sql(search, con=conn)
        tl = ConvertCoords.char_to_geometry(select)
        shape = overlay(tl, gdf, how='intersection')
        shape = shape.rename(columns={valor: 'valor'})
        return shape

    def lote(self, lote_id):
        """
        Função que realiza o insert do lote no banco de dados
        @param lote_id: recebe o id do lote
        @return: grava as informações no banco de dados
        """
        head = ListaHead.list_head(self)
        floats = CampoDataFrame.floats(self)
        cont = 0
        cont_atr = len(floats)
        cont_pontos = len(self)
        search = compile(r'id')
        matches = [x for x in self[head] if search.match(x)]
        mat = matches[0]
        conn = ConexaoOracle.connection().connect()
        session = ConexaoOracle.session(conn)
        for k in range(len(self)):
            for i in range(len(floats)):
                query = INSERT_LOTE_PONTOS % (
                    lote_id, floats[i],
                    self[mat][k],
                    self['Latitude'][k],
                    self['Longitude'][k],
                    self[floats[i]][k])
                query = RemoveAcento.remover(query)
                session.execute(query)
                cont += 1
        session.commit()
        info = {"total": cont, "quantidade_atr": cont_atr, "pontos": cont_pontos, "atributos": floats}

        return info

    def load_shapefile(interpolacaoId, lote_id, atributo_id):
        dbuser = config('DATABASE_AGRICOLA')
        dbpassword = config('DATABASE_PASSWORD')
        conection_string = config('DATABASE_NAME')
        filepath = join(expanduser('~'), 'geosystem', 'lote/shape/')
        namefig = str(lote_id) + '-' + str(atributo_id)
        filename = namefig + '.shp'
        filecamp = filepath + filename
        table = ListaHead.get_random_string(5) + '_temp'

        code = """ogr2ogr --config OCI_FID id \
                -lco GEOMETRY_NAME=geom \
                -lco spatial_index="false" \
                -lco SRID=4326 \
                -lco DIM=2 \
                -lco DIMINFO_X="-180,180,.005"  -lco DIMINFO_Y="-90,90,.005" \
                -nln %s -f OCI OCI:%s/%s@%s:  %s""" % (table, dbuser, dbpassword, conection_string, filecamp)

        system(code)

        dt = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        try:
            conn = ConexaoOracle.connection()
            session = ConexaoOracle.session(conn)
            query = 'SELECT COUNT(1) CONT FROM ' + table.upper()
            select = read_sql(query, con=conn)
        except Exception as e:
            return 'ERRO' + str(e)
        else:
            query = INSERT_INTER_LOTE % (interpolacaoId, table.upper())
            droptable = "DROP TABLE %s" % (table.upper())
            session.execute(query)
            session.execute(droptable)
            session.commit()

            return f'Concluído - {table}'

    def insert_auto(self):
        # self recebe o loteId
        df = DataFrame(JSON.lote_json(self))
        for i in df.index:
            gera_interpolacao.delay(index=i, lote_id=self)
        return 'Concluído!'


    def insert_dados(table, path, versaoId):
        var = read_file(path, encoding='utf-8')
        head = ListaHead.list_head(var)
        con = ConexaoOracle.connection(user=1)

        for i in head:
            if var[i].dtype == 'object':
                tipo = 'VARCHAR2'
            elif var[i].dtype == 'float64' or var[i].dtype == 'float32' or var[i].dtype == 'int32' or var[i].dtype == 'int64':
                tipo = 'NUMBER'
            else:
                tipo = 'Não encontrado'
            insert = AMB_INSERT_ATRIBUTO % (i, tipo, table, versaoId)
            con.execute(insert)
        insert_g = AMB_INSERT_GEOM % (versaoId, table)
        con.execute(insert_g)

        querypl = AMB_PROCESSO % table
        con.execute(querypl)

    def load_tema(versaoId):
        dbuser = 'SAM_DEV'
        dbpassword = 'w8%AJW0ee4^b9s'
        conection_string = 'geosystem_high'
        filepath = join(expanduser('~'), 'geosystem', 'tema/')
        filename =  'versao-' + str(versaoId) + '.shp'
        filecamp = filepath + filename
        table = ListaHead.get_random_string(5) + '_temp'

        code = """ogr2ogr --config OCI_FID id \
                -lco GEOMETRY_NAME=geom \
                -lco spatial_index="false" \
                -lco SRID=4326 \
                -lco DIM=2 \
                -lco ENCODING=UTF-8 \
                -lco DIMINFO_X="-180,180,.005"  -lco DIMINFO_Y="-90,90,.005" \
                -nln %s -f OCI OCI:%s/%s@%s:  %s""" % (table, dbuser, dbpassword, conection_string, filecamp)

        system(code)

        table = table.upper()

        try:
            conn = ConexaoOracle.connection(user=1)
            query = 'SELECT COUNT(1) CONT FROM ' + table.upper()
            read_sql(query, con=conn)
        except Exception as e:
            return 'ERRO' + str(e)
        else:
            InsertTable.insert_dados(table, filecamp, versaoId)
            droptable = "DROP TABLE %s" % (table)
            conn.execute(droptable)

            return f'Concluído - {table}'

@shared_task
def gera_interpolacao(index, lote_id):
    dataframe = DataFrame(JSON.lote_json(lote_id))
    con = ConexaoOracle.connection()
    # Cadastra a interpoação
    insert = CADASTRO_AUTOMATICO % (
        dataframe['TIPO_ID'][index], dataframe['ATRIBUTO_ID'][index], dataframe['ID'][index],
        dataframe['ATRIBUTO_ID'][index], dataframe['DATA'][index], dataframe['ID'][index])
    con.execute(insert)
    # busca o id inserido
    select = SELECT_INTERPOLACAO % (dataframe['ID'][index], dataframe['ATRIBUTO_ID'][index])
    interId = read_sql(select, con=con)
    interId = interId['id'][0]
    # Relaciona o lote e atributo com o talhão e realiza a abrangencia
    var = DataFrame(RelationGeom.relate(dataframe['ID'][index], dataframe['ATRIBUTO_ID'][index]))
    # id do talhão
    talhao = var['talhao_id'][0]
    # insere o talhão e o id da interpoação na tabela de abrangencia
    insert_abr = ABRANGENCIA_AUTOMATICO % (talhao, interId)
    con.execute(insert_abr)
    # Gera imagem e cria o shapefile
    interset = Convertion.gerar_imagem(lote_id, talhao, dataframe['ATRIBUTO_ID'][index], dataframe['DATA'][index], 'IDW')
    # insere o id da interpolação, valor e geometria na tabela de interpolação geon
    InsertTable.load_shapefile(interId, lote_id, dataframe['ATRIBUTO_ID'][index])
    # marca como processado o lote e atributo
    update = """UPDATE INTERPOLACAO_LOTE_PONTOS SET PROCESSADO = 1
                WHERE ATRIBUTO_ID = %s AND INTERPOLACAO_LOTE_ID = %s""" % (dataframe['ATRIBUTO_ID'][index], lote_id)
    con.execute(update)
