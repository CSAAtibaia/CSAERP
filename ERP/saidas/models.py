from django.db import models
from datetime import date
from cadastro.models import *    # TODO Pycharm n gosta mas funciona. W T F ?
# from ERP.cadastro.models import Cota, Pessoa # TODO migrations são feitas sem ERP. wtf?
# Create your models here.


class CentroDeCusto(models.Model):
    codigo = models.CharField('Código', max_length=11, unique=True)
    nome = models.CharField('Nome', max_length=50)

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    nome = models.CharField('Nome', max_length=50, unique=True)
    cnpj = models.BigIntegerField('CNPJ', null=True, blank=True, unique=True)
    contato = models.OneToOneField(Pessoa,
                                   verbose_name='contato',
                                   related_name='fornecedor',
                                   blank=True, null=True,
                                   on_delete=models.PROTECT)
    trabalhador = models.OneToOneField(Cota,
                                       verbose_name='trabalhador',
                                       related_name='fornecedor',
                                       blank=True, null=True,
                                       on_delete=models.PROTECT)

    def __str__(self):
        return self.nome


class Saida(models.Model):
    cdc = models.ForeignKey(CentroDeCusto,
                            on_delete=models.PROTECT,
                            )
    fornecedor = models.ForeignKey(Fornecedor,
                                   on_delete=models.PROTECT,)
    valor = models.DecimalField('Valor', max_digits=6, decimal_places=2)
    data = models.DateField('Data Ref', default=date.today)
    descricao = models.CharField('Descrição', max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s - %s - R$%d" % (self.fornecedor, str(self.data), self.valor)
