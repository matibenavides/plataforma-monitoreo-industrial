from django.shortcuts import render
from datetime import date
from Cloraciones.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='inicio')
def mostrarTemperatura(request):
    return render(request, "temperaturas/base/temperatura.html")


@login_required(login_url='inicio')
def registrarTemperatura(request):
    if request.method == 'POST':


        # Recojo los datos para guardar en el Grupo de Temperatura

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)


        obser = request.POST['observacion']
        linea = Lineas.objects.get(id=1)
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        trabajador = Trabajador.objects.get(id=1)

        # Creo el grupo de temperatura
        grupotemp = GrupoTemperatura.objects.create(
            obs_grt = obser,
            dia_id = dia_obj,
            lineas_id = linea,
            turnos_id = turno,
            trabajador_id = trabajador
        )
        grupotemp.save()

        # Guardo registros de temperatura a partir de 11 columnas de tablatemperatura.html
        for i in range(1, 12):
            hora = request.POST.get(f'hora_{i}') or None
            pulen = request.POST.get(f'pul_{i}')
            aguva = request.POST.get(f'agu_{i}')
            ambca = request.POST.get(f'amb_{i}')
            estfu = request.POST.get(f'est_{i}')

            # Los campos string, los convierto a flotante y acepto None (Null)
            pul = float(pulen) if pulen else None
            agu = float(aguva) if aguva else None
            amb = float(ambca) if ambca else None
            est = float(estfu) if estfu else None

            # Guardo los registros de temperatura

            temperatura = Temperatura.objects.create(
                grupotem_id = grupotemp,
                hor_tem = hora,
                pul_tem = pul,
                agu_tem = agu,
                amb_tem = amb,
                est_tem = est
            )

            # Envio mensaje hacia el Toast de Confirmación

        datos = {
            'msg' : '¡Formulario agregado!',
            'sector' : 'Temperatura'
        }

    return render(request, 'temperaturas/base/temperatura.html', datos)





