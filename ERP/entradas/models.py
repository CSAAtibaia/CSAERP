from django.db import models
from datetime import date
from cadastro.models import *    # TODO Pycharm n gosta mas funciona. W T F ?
# from ERP.cadastro.models import * # TODO migrations são feitas sem ERP. wtf?


# Pagamento < Assinatura < Cota
#             [Servico]


class Pagamento(models.Model):
    assinatura = models.ForeignKey(Assinatura,
                                   related_name='assinatura',
                                   null=False,
                                   on_delete=models.PROTECT)
    # TODO metodo retorne cota
    dt_ref = models.DateField('Referência')
    dt_real = models.DateField('Realizado')
    arquivo = models.CharField('Arquivo', max_length=100, blank=True, null=True)
    # TODO ARRAY vl , servico
    obs = models.CharField('Observações', max_length=100, blank=True, null=True)
    # TODO método vl total
