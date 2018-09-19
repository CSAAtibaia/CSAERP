from django.shortcuts import render
from django.db.models import Count
# Create your views here.

from django.http import HttpResponse
from .models import Cota


# TODO assinatura: somente um serviço / tipo / cota ativo
# TODO comentários: obrigar a ser o usuário atual
# TODO comentários: impedir edit
# TODO Cota: remover pessoa principal da lista outros

def index(request):
    status = ['A', 'P']
    output = Cota.objects.filter(status__in=status) \
        .values('partilha', 'tipo') \
        .annotate(cotas=Count('tipo')) \
        .order_by('partilha', 'tipo')
    return HttpResponse(output)
