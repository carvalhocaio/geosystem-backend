from pandas import read_sql, DataFrame
from branca.colormap import linear, LinearColormap
from geosystem.database.conexao import ConexaoOracle

from geosystem.queries.paleta import PALETA_ATRIBUTO


class PaletaColor:

    def __init__(self):
        pass

    def paleta(self=None, atributo=''):

        select = PALETA_ATRIBUTO

        if self is None and atributo == '':
            boolean = False
            select = ''
        elif self is None and atributo != '':
            boolean = True
            select = select % atributo
        elif self is not None and atributo != '':
            boolean = True
            select = select % self
        else:
            boolean = True
            select = select % self

        return select, boolean

    def gera_paleta(self, boolean):
        if boolean:
            select = read_sql(self, con=ConexaoOracle.connection())
            index = []
            cor = []
            for i in select.index:
                index.append(select['valor_inicial'][i])
                index.append(select['valor_final'][i])
                cor.append(select['hexadecimal'][i])
                cor.append(select['hexadecimal'][i])
            index = DataFrame(index)
            index = index[0]
            nome = select['nome_paleta'][0]
        
        return nome, index, cor

    def color_map(self, lista, color=''):
        if self == 'VERMELHO':
            colormap = linear.Reds_09.scale(
                lista.min(),
                lista.max()
            )
        elif self == 'AZUL':
            colormap = linear.Blues_09.scale(
                lista.min(),
                lista.max()
            )
        elif self == 'VERDE':
            colormap = linear.BuGn_09.scale(
                lista.min(),
                lista.max()
            )
        elif self == 'RED-YEL-GRE':
            colormap = linear.RdYlGn_11.scale(
                lista.min(),
                lista.max()
            )
        elif self == 'RED-BLU':
            colormap = linear.RdBu_09.scale(
                lista.min(),
                lista.max()
            )
        elif self == 'VIRIDIS':
            colormap = linear.viridis.scale(
                lista.min(),
                lista.max()
            )
        elif self == 'SPECTRAL':
            colormap = linear.Spectral_09.scale(
                lista.min(),
                lista.max()
            )
        else:
            colormap = LinearColormap(
                color,
                index=lista,
                vmin=lista.min(),
                vmax=lista.max()
            )
            colormap.to_step(
                n=len(color),
                data=lista,
                method='quantiles',
                round_method='float'
            )

        return colormap

    def paleta_map(self):
        select, boll = PaletaColor.paleta(atributo=self)
        nome, lista_index, lista_cor = PaletaColor.gera_paleta(select, boll)
        color = PaletaColor.color_map(nome, lista_index, lista_cor)
        return color
