import geopandas


class DefVertice:
    """
    Define as propriedades do vértice da geometria
    """
    def __init__(self):
        pass

    def valida(self):
        sv = self
        n_vertices = []
        v_valida = []
        v_tipo = []
        lista_r = []
        n_total_externo = []
        n_total_interno = []
        n1 = 0

        for i, row in sv.iterrows():
            multi = row.geometry.type.startswith("Multi")
            lista_r.append(multi)
            if multi:
                for part in row.geometry:
                    n += len(part)
                    interior_coords = []
                    for interior in row.geometry.interiors:
                        interior_coords += interior.coords[:]
                    n1 = len(interior_coords)
                    v = n + n1
                    if v > 750:
                        v_valida.append(1)
                        tipo = sv['geometry'][i].type
                        v_tipo.append(tipo)
                    else:
                        v_valida.append(0)
                        tipo = sv['geometry'][i].type
                        v_tipo.append(tipo)
            else:
                n = len(row.geometry.exterior.coords)
                interior_coords = []
                for interior in row.geometry.interiors:
                    interior_coords += interior.coords[:]
                n1 = len(interior_coords)
                v = n + n1
                if v > 750:
                    v_valida.append(1)
                    tipo = sv['geometry'][i].type
                    v_tipo.append(tipo)
                else:
                    v_valida.append(0)
                    tipo = sv['geometry'][i].type
                    v_tipo.append(tipo)
            n_vertices.append(v)
            n_total_externo.append(n)
            n_total_interno.append(n1)

        sv['vertices'] = n_vertices
        sv['externo'] = n_total_externo
        sv['interna'] = n_total_interno
        sv['valida'] = v_valida
        sv['tipo'] = v_tipo

        return sv

    def limpa_vertice(self, ver=0.00000005):
        sv = self
        for i in range(len(self)):
            if sv['valida'][i] == 1:
                geo = sv['geometry'][i].simplify(ver)
                sv.loc[i, 'geometry'] = geo

        return self

    def vertice(self):
        sv = self
        cont = 0
        soma = 0
        if self['geometry'][0].type == 'Polygon':
            while soma >= 0:
                for v3 in range(10):
                    v1 = 10 - cont
                    v2 = DefVertice.valida(sv)
                    x = DefVertice.limpa_vertice(v2, v3 / 10 ** v1)
                    y = DefVertice.valida(x)
                    soma = y['valida'].sum()
                if soma == 0:
                    break
                cont = cont + 1
            return y
        else:
            return self
