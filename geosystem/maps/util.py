from os import listdir, remove
from os.path import expanduser, join

from re import sub
from shutil import rmtree
from celery import shared_task
from unicodedata import normalize

import random
import string


class RemoveAcento:
    """
    Remove oa acentos e caracteres especiais
    """

    def __init__(self, var):
        self.var = var

    def remover(self):
        self = normalize("NFD", self)
        self = self.encode("ascii", "ignore")
        self = self.decode("utf-8")
        return self

    def format_title(self):
        self = sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', self)
        self = RemoveAcento.remover(self)
        self = self.upper()
        return self


class ListaHead:
    def __init__(self, var):
        self.var = var

    def list_head(self):  # Lista itens do GeoDataFrame
        self = list(self)
        geom_fil = 'geom'
        geometry_fil = 'geometry'
        index_fil = 'index'
        self = list(filter(lambda a: a != geom_fil, self))
        self = list(filter(lambda a: a != geometry_fil, self))
        self = list(filter(lambda a: a != index_fil, self))
        return self

    def list_index(self):  # Lista cabeçalho do DataFrame/GeoDataFrame
        self = list(self)
        geom_fil = 'geom'
        geometry_fil = 'geometry'
        self = list(filter(lambda a: a != geom_fil, self))
        self = list(filter(lambda a: a != geometry_fil, self))
        return self

    def get_random_string(length):
        # Random string with the combination of lower and upper case
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        print("Random string is:", result_str.lower())
        return result_str.lower()


class DelDist:
    def __init__(self, var):
        self.var = var

    def Pasta(self):
        path = join(expanduser('~'), 'geosystem', 'lote/')
        diri = listdir(path)
        for file in diri:
            if file == self:
                rmtree(path + '/' + file)

    def Arquivo(self):
        path = join(expanduser('~'), 'geosystem', 'lote')
        diri = listdir(path)
        for file in diri:
            if file == self:
                remove(path + '/' + file)


class FileSearch:
    def __init__(self):
        pass

    def search(self):
        path = join(expanduser('~'), 'geosystem', 'lote/')
        diri = listdir(path)
        files = []

        for file in diri:
            if file.find(self) == 0:
                files.append(file)

        if len(files) > 1:
            return self + '.shp'
        else:
            return files[0]

    def file(self=None):
        path = join(expanduser('~'), 'geosystem', 'lote/' + self)
        diri = listdir(path)
        files = []

        for file in diri:
            files.append(file)
        return files


@shared_task
def deleta_diretorio():
    try:
        f = FileSearch.file()
        for i in f:
            if i != 'shape':
                DelDist.Arquivo(i)
            else:
                pasta = FileSearch.file('/' + i)
                for j in pasta:
                    DelDist.Arquivo(j)
    except:
        return 'Não houveram arquivos para serem deletados'
    else:
        return 'Os arquivos foram deletados'
