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
    #Envia id de linea para mostrar en template.
    #Proposito por diferentes ids enviados por navbar.
    linea = Lineas.objects.get(id=linea_id)

    # Muestra listado de registros en el mismo template
    ppm = PPM.objects.all().order_by('-id')

    lista_formato = []
    for lista in ppm:
        lista_formato.append({
            'id': lista.id,
            'turno': lista.turnos_id.nom_tur.upper(),
            'linea': lista.lineas_id.num_lin,
            'trabajador': f"{lista.trabajador_id.nom_tra.capitalize()} {lista.trabajador_id.app_tra.capitalize()}",
            'hora': lista.hor_ppm,
            'ppm': lista.dat_ppm,
            'ph': lista.phe_ppm,
            'fecha': lista.dia_id.dia_dia.strftime('%d-%m-%Y'), # Formato (25-02-2025)
            'observacion': lista.obs_ppm,
        })
    
    paginator = Paginator(lista_formato, 10)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1)

    datos = {
        'listas': listas,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
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



@login_required(login_url='inicio')
def visualizarPPM(request, grupo_id):
    try:
        ppm = get_object_or_404(PPM, id=grupo_id)
        fecha = ppm.dia_id.dia_dia.strftime('%Y-%m-%d')
        turnos = Turnos.objects.all()
        linea = Lineas.objects.get(id=ppm.lineas_id.id)

        registros = PPM.objects.all().order_by('-id')

        lista_formato = []
        for lista in registros:
            lista_formato.append({
                'id': lista.id,
                'turno': lista.turnos_id.nom_tur.upper(),
                'linea': lista.lineas_id.num_lin,
                'trabajador': f"{lista.trabajador_id.nom_tra.capitalize()} {lista.trabajador_id.app_tra.capitalize()}",
                'hora': lista.hor_ppm,
                'ppm': lista.dat_ppm,
                'ph': lista.phe_ppm,
                'fecha': lista.dia_id.dia_dia.strftime('%d-%m-%Y'), # Formato (25-02-2025)
                'observacion': lista.obs_ppm,
            })
        
        paginator = Paginator(lista_formato, 10)
        pagina = request.GET.get("page") or 1
        listas = paginator.get_page(pagina)
        pagina_actual = int(pagina)
        paginas = range(1, listas.paginator.num_pages + 1)

        
        

        datos = {
            'pagina_actual': pagina_actual,
            'paginas': paginas,
            'listas': listas,
            'ppm': ppm,
            'fecha': fecha,
            'turnos': turnos,
            'linea': linea,
        }
        return render(request, 'ppms/form/actualizarppm.html', datos)
    except:
        datos = {
            'msg' : '¡Error, el registro no existe!',
            'sector' : 'Error'
        }
        return render(request, 'ppms/base/ppm.html', datos)
    


def actualizarPPM(request, grupo_id):
    try:
        ppm = PPM.objects.get(id=grupo_id)

        linea = Lineas.objects.get(id=request.POST['lineaop'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])

        hora = request.POST['hora']
        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)

        registro_ppm = request.POST['ppm']
        str_ph = request.POST['ph']
        registro_ph = float(str_ph) if str_ph else None

        observacion = request.POST['observacion']

        ppm.lineas_id = linea
        ppm.turnos_id = turno
        ppm.hor_ppm = hora
        ppm.dia_id = dia_obj
        ppm.dat_ppm = registro_ppm
        ppm.phe_ppm = registro_ph
        ppm.obs_ppm = observacion
        ppm.save()

        messages.success(request, '¡Registro actualizado correctamente!')

        return redirect('ppm', linea_id=linea.id)

    except:
        datos = {
            'linea': linea,
            
        }
    return render(request, 'ppms/base/ppm.html', datos)

