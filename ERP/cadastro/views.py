from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Cota

def index(request):
    lista_cotas = Cota.objects.order_by('-dt_ini')
    output = ', '.join([c.cota_text for c in lista_cotas])
    return HttpResponse(output)
