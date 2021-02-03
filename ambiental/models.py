from django.contrib.gis.db import models


class MapaTematico(models.Model):
    TIPO_GEOMETRIA = (
        ('PL', 'Polígono'),
        ('PT', 'Ponto'),
        ('LH', 'Linha'),
        (None, None)
    )
    TIPO_PONTO = (
        ('M', 'Marcador'),
        ('C', 'Círculo'),
        (None, None)
    )
    nome_mapa = models.VarCharField(max_length=50, blank=False, unique=True)
    observacao = models.VarCharField(max_length=200, blank=True, null=True)
    tipo_geometria = models.VarCharField(max_length=10, choices=TIPO_GEOMETRIA)
    cor_linha = models.VarCharField(max_length=10, default=None)
    tipo_linha = models.IntegerField(default=0)
    tamanho_linha = models.DecimalField(default=0, max_digits=15, decimal_places=6)
    cor_fundo = models.VarCharField(max_length=10, default=None)
    textura_fundo = models.VarCharField(max_length=40, default=None)
    opacidade = models.DecimalField(max_digits=3, decimal_places=2, default=1, null=True)
    cor_ponto = models.VarCharField(max_length=10, default=None)
    tipo_ponto = models.VarCharField(max_length=10, choices=TIPO_PONTO, default=None)
    tamanho_ponto = models.IntegerField(default=0)
    valido = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    deletado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_mapa

    class Meta:
        db_table = 'amb_mapa_tematico'


class VersaoTema(models.Model):
    mapa_tematico = models.ForeignKey(MapaTematico, on_delete=models.CASCADE)
    nome_revisao = models.VarCharField(max_length=30)
    data_cadastro = models.DateField(default=None, null=True)
    observacao = models.VarCharField(max_length=200)
    valido = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    deletado = models.BooleanField(default=False)
    processado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_revisao

    class Meta:
        unique_together = ('mapa_tematico', 'nome_revisao', 'data_cadastro')
        db_table = 'amb_versao_tema'


class Atributo(models.Model):
    versao_tema = models.ForeignKey(VersaoTema, on_delete=models.CASCADE)
    nome_atributo = models.VarCharField(max_length=50)
    tipo_dado = models.VarCharField(max_length=10)
    origem = models.VarCharField(max_length=50)
    visualizacao = models.BooleanField(default=0)
    deletado = models.BooleanField(default=0)

    def __str__(self):
        return self.nome_atributo

    class Meta:
        db_table = 'amb_atributo'
        unique_together = ('versao_tema', 'nome_atributo', 'tipo_dado')


class VersaoTemaGeometria(models.Model):
    versao_tema = models.ForeignKey(VersaoTema, on_delete=models.CASCADE)
    item = models.IntegerField(default=0)
    geom = models.GeometryField()

    def __int__(self):
        return self.item

    class Meta:
        db_table = 'amb_versao_tema_geom'
        unique_together = ('versao_tema', 'item')


class VersaoTemaAtributoGeometria(models.Model):
    versao_tema_geom = models.ForeignKey(VersaoTemaGeometria, on_delete=models.CASCADE)
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)
    texto = models.VarCharField(max_length=200, default=None, null=True)
    numero = models.DecimalField(max_digits=15, decimal_places=6, default=None, null=True)
    data = models.DateField(default=None, null=True)

    class Meta:
        db_table = 'amb_versao_tema_atr_geom'
        unique_together = ('versao_tema_geom', 'atributo')

# class Tema(models.Model):
#     nome_tema = models.CharField(max_length=40)
#     observacao = models.TextField
#
#     class Meta:
#         db_table = "tema"
#         verbose_name = "Tema"
#         verbose_name_plural = "Temas"
#
#     def __str__(self):
#         return self.nome_tema
#
#
# class TemaLancamento(models.Model):
#     tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
#     descricao = models.CharField(max_length=50)
#     data_cadastro = models.DateField()
#     processado = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = "tema_lancamento"
#
#     def __str__(self):
#         return self.descricao
#
#
# class TemaGeometria(models.Model):
#     tema_lancamento = models.ForeignKey(TemaLancamento, on_delete=models.CASCADE)
#     item = models.IntegerField()
#     area = models.IntegerField()
#     distancia = models.IntegerField()
#     geometria = models.GeometryField()
#
#     class Meta:
#         db_table = "tema_geom"
#
#     def __int__(self):
#         return self.item
#
#
#
#
# class TemaValor(models.Model):
#     atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)
#     tema_geometria = models.ForeignKey(TemaGeometria, on_delete=models.CASCADE)
#     valor = models.IntegerField()
#     texto = models.CharField(max_length=300)
#     data = models.DateField()
#
#     class Meta:
#         db_table = "tema_valor"
#
#     def __int__(self):
#         return self.valor
#
#
# class Relatorio(models.Model):
#     nome_relatorio = models.CharField(max_length=100),
#     observacao = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "relatorio"
#         verbose_name = "Relatório"
#         verbose_name_plural = "Relatórios"
#
#     def __str__(self):
#         return self.nome_relatorio
#
#
# class RelatorioLancamento(models.Model):
#     relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE)
#     descricao = models.CharField(max_length=50),
#     data_cadastro = models.DateField()
#     user_cadastro = models.CharField(max_length=100, null=True, blank=True)
#     processado = models.BooleanField(default=0)
#
#     class Meta:
#         db_table = "relatorio_lancamento"
#
#     def __str__(self):
#         return self.descricao
#
#
# class TemaRelatorioBase(models.Model):
#     relatorio_lancamento = models.ForeignKey(RelatorioLancamento, on_delete=models.CASCADE)
#     tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "tema_relatorio_base"
#
#     def __str__(self):
#         return self.relatorio_lancamento
#
#
# class TemaRelatorioCamada(models.Model):
#     tema_relario_base = models.ForeignKey(TemaRelatorioBase, on_delete=models.CASCADE)
#     tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "tema_relatorio_camada"
#
#     def __str__(self):
#         return self.tema_relario_base
#
#
# class RelatorioGeometria(models.Model):
#     relatorio_lancamento = models.ForeignKey(RelatorioLancamento, on_delete=models.CASCADE)
#     tema_relatorio_base = models.ForeignKey(TemaRelatorioBase, on_delete=models.CASCADE)
#     tema_relatorio_camada = models.ForeignKey(TemaRelatorioCamada, on_delete=models.CASCADE)
#     tema_geometria_camada = models.ForeignKey(TemaGeometria, on_delete=models.CASCADE)
#     area = models.IntegerField()
#     percentual = models.IntegerField()
#     geometria = models.GeometryField()
#
#     class Meta:
#         db_table = "relatorio_geometria"
#
#     def __int__(self):
#         return self.area
