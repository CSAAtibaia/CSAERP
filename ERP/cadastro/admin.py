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
    fields = ['comentario']     # TODO , 'arquivo', 'user'
    model = ComPessoa
    extra = 0
    # TODO obrigar a ser o usuário atual
    # TODO impedir edit

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ["comentario"]
    #     else:
    #         return []
    # def get_formset(self, request, obj=None, **kwargs):
    #   self.form.base_fields['autor'].initial = request.user.id


class CotaInLine(admin.TabularInline):
    fields = ['tipo', 'status', 'partilha', 'dt_ini', 'dt_validade']
    model = Cota
    extra = 0


class PessoaAdmin(admin.ModelAdmin):
    inlines = [CotaInLine, ComPessoaInLine, EnderecoInline]


class ComCotaInLine(admin.TabularInline):
    fields = ['comentario', 'autor']     # TODO , 'arquivo', 'user'
    model = ComCota
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            initial.append({
                'autor': request.user,
            })
        formset = super(ComCotaInLine, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset

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
