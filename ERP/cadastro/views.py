from django.shortcuts import render
from django.db.models import Count
# Create your views here.

from django.http import HttpResponse
from .models import Cota


def index(request):
    status = ['A', 'P']
    output = Cota.objects.filter(status__in=status) \
        .values('partilha', 'tipo') \
        .annotate(cotas=Count('tipo')) \
        .order_by('partilha', 'tipo')
    return HttpResponse(output)
