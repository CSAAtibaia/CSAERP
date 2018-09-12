# Register your models here.
from django.contrib import admin

from .models import Pessoa, Cota

admin.site.register(Pessoa)
admin.site.register(Cota)
