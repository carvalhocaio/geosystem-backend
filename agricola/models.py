from django.contrib.gis.db import models


# Plano execução de procedures do sistema
class PlanoCadastro(models.Model):
    descricao = models.CharField(max_length=100)
    processo = models.CharField(max_length=100)
    parametro = models.CharField(max_length=40)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'plano_cadastro'


class PlanoExecucao(models.Model):
    plano = models.ForeignKey(PlanoCadastro, on_delete=models.CASCADE)
    parametro = models.IntegerField(default=0)
    data_agenda = models.DateField(null=True)
    data_processamento = models.DateField(null=True)
    processado = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='FILA')

    class Meta:
        db_table = 'plano_execucao'


class PlanoLog(models.Model):
    plano_execucao = models.ForeignKey(PlanoExecucao, on_delete=models.CASCADE)
    processado = models.CharField(max_length=40)
    parametro = models.CharField(max_length=30)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    quantidade_registro = models.IntegerField(default=0)
    observacao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'plano_log'

    def __str__(self):
        return self.plano_execucao


# SDP / Grids base para gerar o pixel
class Grid0(models.Model):
    nivel = models.IntegerField(default=0)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid0'
        verbose_name = 'Grid 0'


class Grid1(models.Model):
    grid0 = models.ForeignKey(Grid0, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=7)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid1'
        verbose_name = 'Grid 1'


class Grid2(models.Model):
    grid1 = models.ForeignKey(Grid1, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=9)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid2'
        verbose_name = 'Grid 2'


class Grid3(models.Model):
    grid2 = models.ForeignKey(Grid2, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=11)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid3'
        verbose_name = 'Grid 3'


class Grid4(models.Model):
    grid3 = models.ForeignKey(Grid3, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=13)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid4'
        verbose_name = 'Grid 4'


class Grid5(models.Model):
    grid4 = models.ForeignKey(Grid4, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=15)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid5'
        verbose_name = 'Grid 5'


class Grid6(models.Model):
    grid5 = models.ForeignKey(Grid5, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=17)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid6'
        verbose_name = 'Grid 6'


class Grid7(models.Model):
    grid6 = models.ForeignKey(Grid6, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=19)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid7'
        verbose_name = 'Grid 7'


class Grid8(models.Model):
    grid7 = models.ForeignKey(Grid7, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=21)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid8'
        verbose_name = 'Grid 8'


class Grid9(models.Model):
    grid8 = models.ForeignKey(Grid8, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=23)
    processado = models.BooleanField(default=False)
    geom = models.GeometryField()

    class Meta:
        db_table = 'grid9'
        verbose_name = 'Grid 9'


# SDP / Talhões
class TalhaoFazenda(models.Model):
    nome_fazenda = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_fazenda

    class Meta:
        db_table = 'talhao_fazenda'
        verbose_name = 'Fazenda'
        verbose_name_plural = 'Fazendas'


class TalhaoCadastro(models.Model):
    fazenda = models.ForeignKey(TalhaoFazenda, on_delete=models.CASCADE)
    nome_talhao = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome_talhao)

    class Meta:
        db_table = 'talhao_cadastro'
        verbose_name = 'Talhão'
        verbose_name_plural = 'Talhões'


class TalhaoGeometria(models.Model):
    talhao_cad = models.ForeignKey(TalhaoCadastro, on_delete=models.CASCADE)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    centroide = models.GeometryField()
    geom = models.GeometryField()
    area = models.FloatField()
    ano_safra = models.IntegerField()
    processado = models.BooleanField(default=False)
    data_processamento = models.DateField(null=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.geom

    class Meta:
        db_table = 'talhao_geom'


class TalhaoPixel(models.Model):
    talhao_geom = models.ForeignKey(TalhaoGeometria, on_delete=models.CASCADE)
    grid9 = models.ForeignKey(Grid9, on_delete=models.CASCADE)
    area = models.FloatField(default=0)
    percentual = models.FloatField(default=0)
    centroide = models.GeometryField(default=None)
    geom = models.GeometryField()

    class Meta:
        db_table = 'talhao_pixel'


# SDP / Paleta de Cores
class PaletaCadastro(models.Model):
    nome_paleta = models.CharField(max_length=100)
    padrao_sistema = models.BooleanField(default=False)
    observacao = models.TextField(max_length=500)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome_paleta)

    class Meta:
        db_table = 'paleta_cadastro'


class PaletaCor(models.Model):
    paleta = models.ForeignKey(PaletaCadastro, on_delete=models.CASCADE)
    valor_inicial = models.FloatField()
    valor_final = models.FloatField()
    complemento = models.CharField(max_length=100)
    hexadecimal = models.CharField(max_length=10)

    def __str__(self):
        return self.complemento

    class Meta:
        db_table = 'paleta_cor'


# SDP / Atributos
class AtributoCategoria(models.Model):
    nome_categoria = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_categoria

    class Meta:
        db_table = 'atributo_categoria'
        verbose_name = 'Categoria de Atributo'
        verbose_name_plural = 'Categorias de Atributo'


class AtributoCalculo(models.Model):
    nome_calculo = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_calculo

    class Meta:
        db_table = 'atributo_calculo'
        verbose_name = 'Cálculo de Atributo'
        verbose_name_plural = 'Cálculos de Atributo'


class AtributoCadastro(models.Model):
    categoria = models.ForeignKey(AtributoCategoria, on_delete=models.CASCADE)
    calculo = models.ForeignKey(AtributoCalculo, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    unidade_medida = models.CharField(max_length=20)
    enumeracao = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)
    apelido = models.CharField(max_length=50, null=True, blank=True)
    deletado = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'atributo_cadastro'
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'


class AtributoAlias(models.Model):
    atributo = models.ForeignKey(AtributoCadastro, on_delete=models.CASCADE)
    nome_alias = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome_alias

    class Meta:
        db_table = 'atributo_alias'
        indexes = [
            models.Index(fields=['atributo', 'nome_alias']),
        ]


class AtributoEnumeracao(models.Model):
    atributo = models.ForeignKey(AtributoCadastro, on_delete=models.CASCADE)
    valor = models.FloatField(default=0)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'atributo_enumeracao'
        verbose_name = 'Enumeração de Atributo'
        verbose_name_plural = 'Enumerações de Atributo'


class AtributoCor(models.Model):
    atributo = models.ForeignKey(AtributoCadastro, on_delete=models.CASCADE)
    paleta = models.ForeignKey(PaletaCadastro, on_delete=models.CASCADE)
    valor_inicial = models.BooleanField(default=True)
    valor_final = models.BooleanField(default=True)
    complemento = models.BooleanField(default=True)
    paleta_padrao = models.BooleanField(default=False)

    class Meta:
        db_table = 'atributo_cor'
        verbose_name = 'Atributo de Cor'
        verbose_name_plural = 'Atributos de Cor'


# SDP / Interpolação
class InterpolacaoTipo(models.Model):
    descricao = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'interpolacao_tipo'
        verbose_name = 'Tipo de Interpolação'
        verbose_name_plural = 'Tipos de Interpolação'


class InterpolacaoCadastro(models.Model):
    tipo_interpolacao = models.ForeignKey(InterpolacaoTipo, on_delete=models.CASCADE)
    atributo = models.ForeignKey(AtributoCadastro, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    data = models.DateField(auto_now_add=True)
    lancamento_pixel = models.BooleanField(default=True)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)
    processado = models.BooleanField(default=False)
    deletado = models.BooleanField(default=False)
    lote = models.BooleanField(default=False, null=False, blank=False)
    lote_id = models.IntegerField(default=None, null=True, blank=False)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        db_table = 'interpolacao_cadastro'
        verbose_name = 'Interpolação'
        verbose_name_plural = 'Interpolações'


class InterpolacaoAbrangencia(models.Model):
    interpolacao = models.ForeignKey(InterpolacaoCadastro, on_delete=models.CASCADE)
    talhao = models.ForeignKey(TalhaoCadastro, on_delete=models.CASCADE)

    class Meta:
        db_table = 'interpolacao_abrangencia'
        verbose_name = 'Abrangência de Interpolação'
        verbose_name_plural = 'Abrangências de Interpolações'


class InterpolacaoTalhao(models.Model):
    interpolacao = models.ForeignKey(InterpolacaoCadastro, on_delete=models.CASCADE)
    talhao = models.ForeignKey(TalhaoCadastro, on_delete=models.CASCADE)
    valor = models.IntegerField(default=0)

    def __int__(self):
        return self.valor

    class Meta:
        db_table = 'interpolacao_talhao'
        verbose_name = 'Interpolação de Talhão'
        verbose_name_plural = 'Interpolações de Talhões'


class InterpolacaoPonto(models.Model):
    interpolacao = models.ForeignKey(InterpolacaoCadastro, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    valor = models.FloatField()
    geom = models.GeometryField()

    class Meta:
        db_table = 'interpolacao_ponto'
        verbose_name = 'Ponto para Interpolação'
        verbose_name_plural = 'Pontos para Interpolação'


class InterpolacaoGeometria(models.Model):
    interpolacao = models.ForeignKey(InterpolacaoCadastro, on_delete=models.CASCADE)
    valor = models.FloatField(default=0)
    geom = models.GeometryField()

    class Meta:
        db_table = 'interpolacao_geom'


class InterpolacaoPixel(models.Model):
    interpolacao = models.ForeignKey(InterpolacaoCadastro, on_delete=models.CASCADE)
    talhao_pixel = models.ForeignKey(TalhaoPixel, on_delete=models.CASCADE)
    valor = models.FloatField(default=0)

    class Meta:
        db_table = 'interpolacao_pixel'


class InterpolacaoLote(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False)
    data = models.DateField(auto_now_add=True)
    tipo_interpolacao = models.ForeignKey(InterpolacaoTipo, on_delete=models.CASCADE)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)
    deletado = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'interpolacao_lote'


class InterpolacaoLotePonto(models.Model):
    interpolacao_lote = models.ForeignKey(InterpolacaoLote, on_delete=models.CASCADE)
    atributo = models.CharField(max_length=50, null=True, blank=True, default=None)
    atributo = models.ForeignKey(AtributoCadastro, on_delete=models.CASCADE, null=True, blank=True)
    ponto_coleta = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    valor = models.FloatField(default=0)

    class Meta:
        db_table = 'interpolacao_lote_pontos'


# SDP / Formulas
class FormulaCadastro(models.Model):
    nome_formula = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_formula

    class Meta:
        db_table = 'formula_cadastro'
        verbose_name = 'Fórmula'
        verbose_name_plural = 'Fórmulas'


# SDP / Versão
class VersaoCadastro(models.Model):
    descricao = models.CharField(max_length=100)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    valido = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'versao_cadastro'


class VersaoAbrangencia(models.Model):
    versao = models.ForeignKey(VersaoCadastro, on_delete=models.CASCADE)
    talhao = models.ForeignKey(TalhaoCadastro, on_delete=models.CASCADE)

    class Meta:
        db_table = 'versao_abrangencia'


class VersaoAtributo(models.Model):
    versao = models.ForeignKey(VersaoCadastro, on_delete=models.CASCADE)
    atributo = models.ForeignKey(AtributoCadastro, on_delete=models.CASCADE)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    ativo = models.BooleanField(default=True)
    processado = models.BooleanField(default=False)

    class Meta:
        db_table = 'versao_atributo'


class VersaoPixel(models.Model):
    versao_atributo = models.ForeignKey(VersaoAtributo, on_delete=models.CASCADE)
    talhao = models.ForeignKey(TalhaoCadastro, on_delete=models.CASCADE)
    talhao_pixel = models.ForeignKey(TalhaoPixel, on_delete=models.CASCADE)
    valor = models.FloatField()

    class Meta:
        db_table = 'versao_pixel'


class VersaoGeometria(models.Model):
    versao_atributo = models.ForeignKey(VersaoAtributo, on_delete=models.CASCADE)
    valor = models.FloatField()
    geom = models.GeometryField()

    class Meta:
        db_table = 'versao_geom'
