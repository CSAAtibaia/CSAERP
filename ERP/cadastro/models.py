from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


TIPO = {('C', 'Cotista'),
        ('T', 'Trabalhador'),
        ('B', 'Bolsista'),
        ('A', 'Apoiador'),
        ('P', 'Permuta')}

STATUS = {('A', 'Ativo'),
          ('I', 'Inativo'),
          ('P', 'Aviso Prévio'),
          ('S', 'Suspenso')}

PARTILHA = {('A', 'Atibaia'),
            ('S', 'São Paulo')}


def get_validade_default():
    return True


class Pessoa(models.Model):     # TODO Obrigatoriedades
    prim_nome = models.CharField('Nome', max_length=50) # TODO controlar duplicidade
    sobrenome = models.CharField('Sobrenome', max_length=100)
    dt_nascimento = models.DateField('Data de Nascimento')
    apelido = models.CharField('Apelido', max_length=50, unique=True, null=True)
    rg = models.PositiveIntegerField('RG')  # TODO RG formato validar dígito
    cpf = models.BigIntegerField('CPF')     # TODO CPF formato validar dígito
    profissao = models.CharField('Profissão', max_length=300, null=True)
    telefone = models.BigIntegerField('Telefone', null=True)
    email = models.EmailField('E-mail', null=True)

    def __str__(self):
        if self.apelido == '':
            return "%s %s - %s" % (self.prim_nome, self.sobrenome, self.pk)
        else:
            return self.apelido


class ComPessoa(models.Model):   # TODO inserir no admin de pessoa
    comentario = models.CharField(max_length=255, default='Insira seu comentário')  # TODO impedir edit
    user = models.ForeignKey(User, related_name='compessoauser', on_delete=models.PROTECT, default=0)
    dt_com = models.DateTimeField(auto_now_add=True)
    fk_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='compessoa')

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ('dt_com',)


class Cota(models.Model):       # TODO refazer __str__
    tipo = models.CharField(choices=TIPO, max_length=50)
    status = models.CharField(choices=STATUS, max_length=50)
    partilha = models.CharField(choices=PARTILHA, max_length=50)
    higieniza = models.BooleanField(default=False)
    dt_ini = models.DateField(default=date.today)
    # dt_ini_desliga = models.DateField TODO resultante
    # dt_ini_susp = models.DateField TODO resultante
    # dt_fim = models.DateField TODO resultante
    dt_validade = models.DateField
    # dt_retira = models.DateField TODO resultante
    principal = models.ForeignKey(Pessoa, related_name='cota', null=False, on_delete=models.PROTECT)
    # TODO implementar pessoa principal obrigatória
    outros = models.ManyToManyField(Pessoa,
                                    related_name='cota_outros',
                                    null=True)     # TODO remover pessoa principal da lista

    def __str__(self):
        if Cota.objects.filter(principal__apelido=self.principal).count() == 1:
            return self.principal
        else:   # TODO mudar para a desc de tipo e status
            return "%s - %s - %s" %(self.principal, self.tipo, self.status)


class ComCota(models.Model):     # TODO inserir no admin de Cota
    comentario = models.CharField(max_length=255, default='Insira seu comentário')  # TODO impedir edit
    user = models.ForeignKey(User, related_name='comcotauser', on_delete=models.PROTECT, default=0)
    dt_com = models.DateTimeField(auto_now_add=True)
    fk_cota = models.ForeignKey(Cota, related_name='comcota', on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ('dt_com',)
