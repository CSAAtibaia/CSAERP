# Register your models here.
from django.contrib import admin
from .models import Pessoa, Cota, ComCota, ComPessoa


class ComPessoaInLine(admin.TabularInline):
    fields = ['comentario'] # TODO , 'arquivo'
    model = ComPessoa
    extra = 0


class PessoaAdmin(admin.ModelAdmin):
    inlines = [ComPessoaInLine]


class ComCotaInLine(admin.TabularInline):
    fields = ['comentario'] # TODO , 'arquivo'
    model = ComCota
    extra = 0


class CotaAdmin(admin.ModelAdmin):
    inlines = [ComCotaInLine]


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Cota, CotaAdmin)
