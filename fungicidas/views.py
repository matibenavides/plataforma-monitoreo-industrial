from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from Cloraciones.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q

from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML




@login_required(login_url='inicio')
def mostrarFungicida(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)

    datos = {
        'linea': linea
    }

    return render(request, "fungicidas/base/fungicida.html", datos)


@login_required(login_url='inicio')
def registrarFungicida(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)
    if request.method == 'POST':

        
        especie = Especies.objects.get(id=request.POST['especie'])
        variedad = Variedad.objects.get(id=request.POST['variedad'])
        trabajador = request.user.trabajador

        hora = request.POST['hora']
        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)

        producto = Fungicidas.objects.get(id=request.POST['producto'])
        agua = request.POST['agua'] or 0
        cera = request.POST['cera'] or 0
        
        peso_inicial = request.POST['peso_inicial']
        peso_final = request.POST['peso_final']
        cc_producto = request.POST['cc_producto']

        observacion = request.POST['observacion']

        dosificacion = Dosificacion.objects.create(
            lineas_id = linea,
            trabajador_id = trabajador,
            especies_id = especie,
            variedad_id = variedad,
            fungicidas_id = producto,
            dia_id = dia_obj,
            hor_dos = hora,
            pei_dos = peso_inicial,
            pef_dos = peso_final,
            ccp_dos = cc_producto,
            agu_dos = agua,
            cer_dos = cera,
            obs_dos = observacion,
        )
        dosificacion.save()
        

        messages.success(request, '¡Registro agregado correctamente!')

        return redirect('fungicida', linea_id=linea.id)
    
    else:

        datos = {
            'linea': linea,
        }
    return render(request, 'fungicidas/base/fungicida.html', datos)
