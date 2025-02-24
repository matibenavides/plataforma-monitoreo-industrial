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

# Create your views here.

@login_required(login_url='inicio')
def mostrarPPM(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)
    

    datos = {
        'linea': linea,
    } 
    return render(request, "ppms/base/ppm.html", datos)

@login_required(login_url='inicio')
def registrarPPM(request,linea_id):

    linea = Lineas.objects.get(id=linea_id)
    if request.method == 'POST':

        

        # linea = Lineas.objects.get(id=request.POST['lineaop'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        trabajador = request.user.trabajador
        hora = request.POST['hora']

        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)
        #Solución, 'Cannot assign "'2025-02-23'": "PPM.dia_id" must be a "Dia" instance.'

        ppm = request.POST['ppm']
        phstr = request.POST['ph']

        ph = float(phstr) if phstr else None
        observacion = request.POST['observacion']

        ppm = PPM.objects.create(
            lineas_id=linea,
            trabajador_id=trabajador,
            turnos_id=turno,
            dia_id=dia_obj, 
            hor_ppm=hora,
            dat_ppm=ppm,
            phe_ppm=ph,
            obs_ppm=observacion,
        )


        messages.success(request, '¡Registro agregado correctamente!')
        

        return redirect('ppm', linea_id=linea.id)
    
    else:
       
        datos = {
            'linea': linea,
            
        }
    return render(request, 'ppms/base/ppm.html', datos)

    


