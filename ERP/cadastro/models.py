from django.db import models
from datetime import date
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
    prim_nome = models.CharField('Nome', max_length=50)
    sobrenome = models.CharField('Sobrenome', max_length=100)
    dt_nascimento = models.DateField('Data de Nascimento')
    apelido = models.CharField('Apelido', max_length=50)
    rg = models.PositiveIntegerField('RG')  # TODO RG formato validar dígito
    cpf = models.BigIntegerField('CPF')     # TODO CPF formato validar dígito
    profissao = models.CharField('Profissão', max_length=300)
    telefone = models.BigIntegerField('Telefone')
    email = models.EmailField('E-mail')

    def __str__(self):
        if self.apelido == '':
            return "%s %s - %s" % (self.prim_nome, self.sobrenome, self.pk)
        else:
            return self.apelido


class ComPessoa(models.Model): # TODO inserir no admin de pessoa
    comentario = models.CharField
    #user
    dt_com = models.DateTimeField(auto_now_add=True)
    fk_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ('dt_com',)


class Cota(models.Model):
    tipo = models.CharField(choices=TIPO, max_length=50)
    status = models.CharField(choices=STATUS, max_length=50)
    partilha = models.CharField(choices=PARTILHA, max_length=50)
    higieniza = models.BooleanField(default=False)
    dt_ini = models.DateField(default=date.today)
    dt_ini_desliga = models.DateField
    dt_ini_susp = models.DateField
    dt_fim = models.DateField
    dt_validade = models.DateField
    dt_retira = models.DateField
    principal = Pessoa      # TODO implementar pessoa principal obrigatória
    outros = models.ManyToManyField(Pessoa) # TODO remover pessoa principal da lista


class ComCota(models.Model): # TODO inserir no admin de Cota
    comentario = models.CharField
    #user
    dt_com = models.DateTimeField(auto_now_add=True)
    fk_cota = models.ForeignKey(Cota, on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario

    class Meta:
        ordering = ('dt_com',)
