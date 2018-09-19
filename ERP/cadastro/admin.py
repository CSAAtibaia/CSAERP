# Register your models here.
from django.contrib import admin
from .models import *


class EnderecoInline(admin.StackedInline):
    fields = ['tp_logradouro',
              'logradouro',
              'numero',
              'bairro',
              'cidade',
              'uf',
              'cep',
              ]
    model = Endereco
    extra = 1


class ComPessoaInLine(admin.TabularInline):
    fields = ['comentario']     # TODO , 'arquivo', 'user'
    model = ComPessoa
    extra = 0


class CotaInLine(admin.TabularInline):
    fields = ['tipo', 'status', 'partilha', 'dt_ini', 'dt_validade']
    model = Cota
    extra = 0


class PessoaAdmin(admin.ModelAdmin):
    inlines = [CotaInLine, ComPessoaInLine, EnderecoInline]


class ComCotaInLine(admin.TabularInline):
    fields = ['comentario']     # TODO , 'arquivo', 'user'
    model = ComCota
    extra = 0


class AssinaturaInline(admin.TabularInline):
    model = Assinatura
    extra = 0


class CotaAdmin(admin.ModelAdmin):  # TODO adicionar tipo, status e partilha na listview
    inlines = [ComCotaInLine, AssinaturaInline]


class PartilhaAdmin(admin.ModelAdmin):  # TODO adicionar tipo, status e partilha na listview
    inlines = [EnderecoInline]


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Cota, CotaAdmin)
admin.site.register(Servico)
admin.site.register(Partilha, PartilhaAdmin)
