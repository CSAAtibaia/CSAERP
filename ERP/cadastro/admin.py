# Register your models here.
from django.contrib import admin
from django.utils.functional import curry
from .models import *


class EnderecoInline(admin.StackedInline):
    fields = [('tp_logradouro',
              'logradouro',),
              ('numero',
              'complemento',),
              ('bairro',
              'cidade',
              'uf',),
              'cep',
              ]
    model = Endereco
    extra = 1


class ComPessoaInLine(admin.TabularInline):
    # TODO , 'arquivo', 'user'
    model = ComPessoa
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class CotaInLine(admin.TabularInline):
    fields = ['tipo', 'status', 'partilha', 'dt_ini', 'dt_validade']
    model = Cota
    extra = 0


class PessoaAdmin(admin.ModelAdmin):
    inlines = [CotaInLine, ComPessoaInLine, EnderecoInline]


class ComCotaInLine(admin.TabularInline):
    # TODO , 'arquivo', 'user'
    model = ComCota
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class AssinaturaInline(admin.TabularInline):
    model = Assinatura
    extra = 0


class CotaAdmin(admin.ModelAdmin):  # TODO adicionar tipo, status e partilha na listview
    inlines = [ComCotaInLine, AssinaturaInline]

    # default=Partilha.objects.filter(padrao=True),    # TODO colocar na view


class PartilhaAdmin(admin.ModelAdmin):  # TODO adicionar tipo, status e partilha na listview
    inlines = [EnderecoInline]
    fields = [('nome',
              'padrao')]


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Cota, CotaAdmin)
admin.site.register(Servico)
admin.site.register(Partilha, PartilhaAdmin)
