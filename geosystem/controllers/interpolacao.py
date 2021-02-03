from json import loads
from pandas import read_sql
from os.path import join, expanduser
from numpy.ma import masked_invalid
from warnings import filterwarnings
from geopandas import read_file, GeoSeries, GeoDataFrame, points_from_xy
from wradlib.ipol import Idw, Nearest, Linear, OrdinaryKriging
from matplotlib.pyplot import axis, figure, savefig

from geosystem.controllers.coordenadas import ConvertCoords
from geosystem.database.conexao import ConexaoOracle
from geosystem.maps.util import ListaHead

filterwarnings('ignore')


class Interpolacao:
    """
    Define as propriedades para gerar o gráfico com os dados
    """

    def __init__(self):
        pass

    def gridplot(self, ax, src, xtrg, ytrg):
        pm = ax.pcolormesh(xtrg, ytrg, self.reshape((len(xtrg), len(ytrg))))
        axis("tight")
        ax.scatter(src[:, 0], src[:, 1], facecolor="None", s=1000, marker='s')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    def interpolacao(self, src, trg, vals, vnum=10, pdi=4):
        if self == 'IDW':
            idw = Idw(src, trg, vnum, pdi)
            return idw(vals)
        elif self == 'Vizinhos':
            nn = Nearest(src, trg)
            return nn(vals)
        elif self == 'Linear':
            linear = Linear(src, trg)
            return masked_invalid(linear(vals))
        elif self == 'Krigagem':
            ok = OrdinaryKriging(src, trg)
            return ok(vals)

    def interpolacao_imagem(self, src, trg, vals, xtrg, ytrg, namefig, vnum=12, pdi=4):
        # self recebe o tipo da interpolacao. default = IDW
        interpolacao = Interpolacao.interpolacao(self, src, trg, vals, vnum, pdi)
        fig = figure(figsize=(5, 5), linewidth=None, frameon=False, dpi=None)
        ax = fig.add_subplot(111, label='_nolegend_')
        fig.subplots_adjust(left=0.0, right=1, top=1, bottom=0.0)
        Interpolacao.gridplot(interpolacao, ax, src, xtrg, ytrg)
        # namefig = ListaHead.get_random_string(4)
        savefig(join(expanduser('~'), 'geosystem', 'lote/') + namefig + '.png', transparent=True, pad_inches=0)

        return interpolacao



