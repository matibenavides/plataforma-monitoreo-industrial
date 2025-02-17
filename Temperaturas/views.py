from django.shortcuts import render
from datetime import date
from Cloraciones.models import *
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


@login_required(login_url='inicio')
def mostrarTemperatura(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)

    datos = {
        'linea': linea,
    } 
    return render(request, "temperaturas/base/temperatura.html", datos)


@login_required(login_url='inicio')
def registrarTemperatura(request):
    if request.method == 'POST':


        # Recojo los datos para guardar en el Grupo de Temperatura

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)


        obser = request.POST['observacion']
        linea_id = Lineas.objects.get(id=request.POST['linea_id'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        trabajador = request.user.trabajador

        # Creo el grupo de temperatura
        grupotemp = GrupoTemperatura.objects.create(
            obs_grt = obser,
            dia_id = dia_obj,
            lineas_id = linea_id,
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




@login_required(login_url='inicio')
def mostrarListaTemperatura(request):
    busqueda = request.GET.get("buscar")
    grupoLista = GrupoTemperatura.objects.all().order_by('-id')

    if busqueda:
        grupoLista = grupoLista.filter(
            Q(turnos_id__nom_tur__icontains = busqueda) |
            Q(lineas_id__num_lin__icontains = busqueda) |
            Q(trabajador_id__nom_tra__icontains = busqueda) |
            Q(dia_id__dia_dia__icontains = busqueda) 
        ).distinct()

    grupo_modificado = []
    for grupo in grupoLista:
        grupo_modificado.append({
            "id":  grupo.id,
            "turno": grupo.turnos_id.nom_tur.upper(),
            "trabajador":f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            "fecha": grupo.dia_id,
            "linea": grupo.lineas_id.num_lin,
        })

    paginator = Paginator(grupo_modificado, 10)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1)

    datos = {
        'listas': listas,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
    }

    return render(request, "temperaturas/base/listatemperatura.html", datos)

