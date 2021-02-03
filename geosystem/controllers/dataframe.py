from geosystem.maps.util import ListaHead


class CampoDataFrame:
    """
    Define as propriedades do DataFrame
    """

    def __init__(self, var):
        self.var = var

    def talhao(self):
        head = ListaHead.list_head(self)
        for i in head:
            if i == 'Talhão':
                return i
                break
            elif i == 'Talhao':
                return i
                break
            elif i == 'TALHAO':
                return i
                break
            elif i == 'TALHÃO':
                return i
                break
            elif i == 'TL':
                return i
                break
            elif i == 'tl':
                return i
                break
            elif i == 'Tl':
                return i
                break

    def fazenda(self):
        head = ListaHead.list_head(self)
        for i in head:
            if i == 'Fazenda':
                return i
                break
            elif i == 'fazenda':
                return i
                break

    def valor(self):
        head = ListaHead.list_head(self)
        for i in head:
            tipo = self[head][i].dtype
            if tipo == 'float64':
                return i
            else:
                return 0

    def floats(self):
        head = ListaHead.list_head(self)
        h_float = []
        for h in head:
            if (h.upper() != 'LATITUDE' and h.upper() != 'LONGITUDE') and (
                    self[h].dtype == 'float64' or self[h].dtype == 'float32'):
                h_float.append(h)
        return h_float


class LimpaDataFrame:
    def __init__(self, var):
        self.var = var

    def limpar(self):
        remover = [
            'Alagado',
            'Barracao',
            'Corredor',
            'Estrada',
            'Eucalipto',
            'Mata',
            'Nascente',
            'Pasto',
            'Piquete',
            'Pista',
            'Pista 202 BO',
            'Sede',
            'Sede RD',
            'Tirrapeli'
        ]
        for i in range(len(remover)):
            talhao = CampoDataFrame.talhao(self)
            fill = self[talhao] != remover[i]
            self = self[fill]
        fill = self[talhao].notnull()
        self = self[fill]
        self = self.reset_index()
        self = self.drop(['index'], axis=1)
        return self
