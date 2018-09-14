from django.db import models
from datetime import date   # TODO , timedelta
from django.contrib.auth.models import User
from .utils import ChoiceEnum

# Create your models here.


def get_validade_default():
    return date.today   # TODO + timedelta(days=365)


class Tipo(ChoiceEnum):
    COTISTA = 'Cotista'
    TRABALHADOR = 'Trabalhador'
    BOLSISTA = 'Bolsista'
    APOIADOR = 'Apoiador'
    PERMUTA = 'Permuta'


class Status(ChoiceEnum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    AVISO = 'Aviso Prévio'
    SUSPENSO = 'Suspenso'


class Partilha(ChoiceEnum):
    ATIBAIA = 'Atibaia'
    SAOPAULO = 'São Paulo'


class Pessoa(models.Model):
    prim_nome = models.CharField('Nome', max_length=50)  # TODO controlar duplicidade
    sobrenome = models.CharField('Sobrenome', max_length=100)
    dt_nascimento = models.DateField('Data de Nascimento')
    apelido = models.CharField('Apelido', max_length=50, unique=True, null=True, blank=True)
    rg = models.PositiveIntegerField('RG', null=True, blank=True)  # TODO RG formato validar dígito
    cpf = models.BigIntegerField('CPF', null=True, blank=True)     # TODO CPF formato validar dígito
    profissao = models.CharField('Profissão', max_length=300, null=True, blank=True)
    telefone = models.BigIntegerField('Telefone', null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True)

    def __str__(self):
        if self.apelido == '':
            return "%s %s - %s" % (self.prim_nome, self.sobrenome, self.pk)
        else:
            return self.apelido


class ComPessoa(models.Model):
    comentario = models.TextField(default='Insira seu comentário')  # TODO impedir edit
    # TODO arquivo = models.FileField
    user = models.ForeignKey(User,  # TODO obrigar a ser o usuário atual
                             related_name='compessoauser',
                             on_delete=models.PROTECT,
                             default=0)
    dt_com = models.DateTimeField(auto_now_add=True)
    fk_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='compessoa')

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ('dt_com',)


class Cota(models.Model):
    tipo = models.CharField('Tipo', choices=Tipo.choices(), default=Tipo.COTISTA, max_length=15)
    status = models.CharField('Status', choices=Status.choices(), default=Status.ATIVO, max_length=15)
    partilha = models.CharField('Partilha', choices=Partilha.choices(), default=Partilha.ATIBAIA, max_length=15)
    higieniza = models.BooleanField('Higieniza', default=False)
    dt_ini = models.DateField('Início', default=date.today)
    dt_validade = models.DateField('Validade', default=get_validade_default)  # TODO default = today + 1 ano
    # dt_ini_desliga = models.DateField TODO resultante
    # dt_ini_susp = models.DateField TODO resultante
    # dt_fim = models.DateField TODO resultante
    # dt_retira = models.DateField TODO resultante
    principal = models.ForeignKey(Pessoa,   # TODO validar/restringir q Pessoa escolhida tem rg/cpf
                                  related_name='cota',
                                  null=False,
                                  on_delete=models.PROTECT)
    outros = models.ManyToManyField(Pessoa,
                                    related_name='cota_outros',
                                    blank=True
                                    )     # TODO remover pessoa principal da lista

    def __str__(self):
        if Cota.objects.filter(principal=self.principal).count() == 1:
            return str(self.principal)
        else:
            return "%s - %s - %s" % (self.principal,
                                     self.get_tipo_display(),
                                     self.get_status_display()
                                     )


class ComCota(models.Model):
    comentario = models.TextField(default='Insira seu comentário')  # TODO impedir edit
    # TODO arquivo = models.FileField
    user = models.ForeignKey(User,  # TODO obrigar a ser o usuário atual
                             related_name='comcotauser',
                             on_delete=models.PROTECT,
                             default=0)
    dt_com = models.DateTimeField(auto_now_add=True)
    fk_cota = models.ForeignKey(Cota, related_name='comcota', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ('dt_com',)
