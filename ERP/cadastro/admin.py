# Register your models here.
from django.contrib import admin
from .models import Pessoa, Cota, ComCota, ComPessoa


class ComCotaInLine(admin.StackedInline):
    fields = ['comentario']
    model = ComCota
    extra = 0


class CotaAdmin(admin.ModelAdmin):
    inlines = [ComCotaInLine]


admin.site.register(Pessoa)
admin.site.register(Cota, CotaAdmin)
