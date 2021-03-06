from django.db import models
from .fields import UniqueBooleanField
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from .utils import ChoiceEnum, validador_cpf, validador_rg

# Create your models here.

ANO = 365
MES = 30
SEMESTRE = 180


def get_validade_default(x):
    date_x = datetime.now() + timedelta(days=x)
    return date_x


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


class Frenquencia(ChoiceEnum):
    SEMANAL = 'Semanal'
    MENSAL = 'Mensal'
    BIMESTRAL = 'Bimestral'
    TRIMESTRAL = 'Trimestral'
    SEMESTRAL = 'Semestral'
    ANUAL = 'Anual'


class Partilha(models.Model):
    nome = models.CharField('Nome', max_length=25, unique=True)
    padrao = UniqueBooleanField('Padrão', default=False, null=False)

    def __str__(self):
        return self.nome


def partilhapadrao():
    return Partilha.objects.filter(padrao=True)


class Pessoa(models.Model):
    prim_nome = models.CharField('Nome', max_length=50)
    sobrenome = models.CharField('Sobrenome', max_length=100)
    dt_nascimento = models.DateField('Data de Nascimento')
    apelido = models.CharField('Apelido', max_length=50, unique=True, null=True, blank=True)
    rg = models.PositiveIntegerField('RG',
                                     validators=[validador_rg],
                                     null=True,
                                     blank=True,
                                     unique=True)
    cpf = models.BigIntegerField('CPF',
                                 validators=[validador_cpf],
                                 null=True, blank=True, unique=True)
    profissao = models.CharField('Profissão', max_length=300, null=True, blank=True)
    telefone = models.BigIntegerField('Telefone', null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True, unique=True)
    user = models.OneToOneField(User,
                                related_name='pessoa',
                                blank=True, null=True,
                                on_delete=models.PROTECT)

    def __str__(self):
        if self.apelido != '':
            return self.apelido
        elif self.user != '':
            return self.user
        else:
            return "%s %s - %s" % (self.prim_nome, self.sobrenome, self.pk)


class Endereco(models.Model):
    tp_logradouro = models.CharField('Tipo', max_length=25, default='Rua')
    logradouro = models.CharField('Logradouro', max_length=255, default='Rua')
    numero = models.PositiveIntegerField('Número')
    complemento = models.CharField('Complemento', max_length=255, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=255)
    cidade = models.CharField('Cidade', max_length=255)
    uf = models.CharField('UF', max_length=2)
    cep = models.PositiveIntegerField('CEP')   # TODO display {{ value|stringformat:"04d" }}
    # TODO CEP preencher o resto
    pessoa = models.OneToOneField(Pessoa,
                                  related_name='endereco',
                                  blank=True, null=True,
                                  on_delete=models.PROTECT)
    partilha = models.OneToOneField(Partilha,
                                    related_name='endereco',
                                    blank=True, null=True,
                                    on_delete=models.PROTECT)

    def __str__(self):
        return str(self.pk)


class ComPessoa(models.Model):
    comentario = models.TextField(default='Insira seu comentário')
    # TODO arquivo = models.FileField
    fk_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='compessoa')

    def __str__(self):
        return self.comentario


class Servico(models.Model):
    servico = models.CharField('Serviço', max_length=100, unique=True)
    descricao = models.CharField('Descrição', max_length=255, null=True, blank=True)
    valor = models.DecimalField('Valor', max_digits=6, decimal_places=2)
    frequencia = models.CharField('Frequência',
                                  max_length=15,
                                  choices=Frenquencia.choices(),
                                  default=Frenquencia.MENSAL)
    valor_adesao = models.DecimalField('Valor Adesão', max_digits=6, decimal_places=2, blank=True, null=True)
    max_adesao = models.PositiveIntegerField('Max', blank=True, null=True)
    email = models.EmailField('E-Mail', null=True, blank=True)
    referencia = models.CharField('Referência', max_length=100, unique=True, blank=True, null=True)
    duracao_padrao = models.PositiveSmallIntegerField('Duração', blank=True, null=True)

    def __str__(self):
        return self.servico


class Cota(models.Model):
    tipo = models.CharField('Tipo', choices=Tipo.choices(), default=Tipo.COTISTA, max_length=15)
    status = models.CharField('Status', choices=Status.choices(), default=Status.ATIVO, max_length=15)
    partilha = models.ForeignKey(Partilha,
                                 related_name='cota',
                                 null=False,
                                 on_delete=models.PROTECT)
    higieniza = models.BooleanField('Higieniza', default=False)
    dt_ini = models.DateField('Início', default=date.today)
    dt_validade = models.DateField('Validade',
                                   #    default=get_validade_default(ANO),
                                   )
    # dt_ini_desliga = models.DateField TODO resultante
    # dt_ini_susp = models.DateField TODO resultante
    # dt_fim = models.DateField TODO resultante
    # dt_retira = models.DateField TODO resultante
    principal = models.ForeignKey(Pessoa,   # TODO validar/restringir q Pessoa escolhida tem rg/cpf
                                  # limit_choices_to=Pessoa.objects.filter(rg > 0 | cpf > 0),
                                  related_name='cota',
                                  null=False,
                                  on_delete=models.PROTECT)
    outros = models.ManyToManyField(Pessoa,
                                    related_name='cota_outros',
                                    blank=True
                                    )

    def __str__(self):
        if Cota.objects.filter(principal=self.principal).count() == 1:
            return str(self.principal)
        else:
            return "%s - %s - %s" % (self.principal,
                                     self.get_tipo_display(),
                                     self.get_status_display()
                                     )


class ComCota(models.Model):
    comentario = models.TextField(default='Insira seu comentário')
    # TODO arquivo = models.FileField
    fk_cota = models.ForeignKey(Cota, related_name='comcota', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario


class Assinatura(models.Model):
    cota = models.ForeignKey(Cota,
                             related_name='assinatura',
                             null=False,
                             on_delete=models.PROTECT)
    servico = models.ForeignKey(Servico,
                                related_name='assinatura',
                                null=False,
                                on_delete=models.PROTECT)
    dt_ini = models.DateField('Início', default=date.today)
    dt_validade = models.DateField('Validade',
                                   #    default=get_validade_default(ANO),
                                   )
    obs = models.TextField('Observações', blank=True, null=True)
    # TODO auth token para verificação & validação
    # TODO método cobrança

    def __str__(self):
        return "%s - %s" % (str(self.cota), str(self.pk))
