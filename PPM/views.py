from django.shortcuts import render, get_object_or_404
from datetime import date
from Cloraciones.models import *
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q

from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML

# Create your views here.

@login_required(login_url='inicio')
def mostrarPPM(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)
    

    datos = {
        'linea': linea,
    } 
    return render(request, "ppms/base/ppm.html", datos)