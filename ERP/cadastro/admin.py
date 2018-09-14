# Register your models here.
from django.contrib import admin
from .models import *


class ComPessoaInLine(admin.TabularInline):
    fields = ['comentario']     # TODO , 'arquivo'
    model = ComPessoa
    extra = 0


class CotaInLine(admin.TabularInline):
    fields = ['tipo', 'status', 'partilha', 'dt_ini', 'dt_validade']
    model = Cota
    extra = 0


class PessoaAdmin(admin.ModelAdmin):
    inlines = [CotaInLine, ComPessoaInLine]


class ComCotaInLine(admin.TabularInline):
    fields = ['comentario']     # TODO , 'arquivo'
    model = ComCota
    extra = 0


class AssinaturaInline(admin.TabularInline):
    model = Assinatura
    extra = 0


class CotaAdmin(admin.ModelAdmin):  # TODO adicionar tipo, status e partilha na listview
    inlines = [ComCotaInLine, AssinaturaInline]


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Cota, CotaAdmin)
admin.site.register(Servico)
