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


@login_required(login_url='inicio')
def visualizarTemperatura(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoTemperatura, pk=grupo_id)
        registros_temperatura = Temperatura.objects.filter(grupotem_id = grupo).order_by('id')

        turnos = Turnos.objects.all()
        fecha = grupo.dia_id.dia_dia.strftime("%Y-%m-%d")
        observacion = grupo.obs_grt

        datos = {
            'grupo': grupo,
            'registros_temperatura': registros_temperatura,
            'turnos': turnos,
            'fecha': fecha,
            'observacion': observacion
        }

        return render(request, 'temperaturas/form/registroTemperatura.html', datos)

    
    except:
        datos = {
            'msg' : '¡Error, el formulario no existe!',
            'sector' : 'Error'
        }

        return render(request, 'temperaturas/base/temperatura.html', datos)


@login_required(login_url='inicio')
def actualizarTemperatura(request, grupo_id):
    try:
        grupo= get_object_or_404(GrupoTemperatura, pk=grupo_id)
        fecha = request.POST['fecha']
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        observacion = request.POST['observacion']

        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)

        grupoupdate = GrupoTemperatura.objects.get(id=grupo_id)

        grupoupdate.dia_id = dia_obj
        grupoupdate.turnos_id = turno
        grupoupdate.obs_grt = observacion
        grupoupdate.save()

        for i in range(1, 12):

            registro_id = request.POST.get(f'temperatura_id_{i}')

            if registro_id:
                registro = Temperatura.objects.get(id=registro_id)

                hora = request.POST.get(f'hora_{i}') or None
                pulen = request.POST.get(f'pul_{i}')
                aguva = request.POST.get(f'agu_{i}')
                ambca = request.POST.get(f'amb_{i}')
                estfu = request.POST.get(f'est_{i}')

                pul = float(pulen) if pulen else None
                agu = float(aguva) if aguva else None
                amb = float(ambca) if ambca else None
                est = float(estfu) if estfu else None

                registro.hor_tem = hora
                registro.pul_tem = pul
                registro.agu_tem = agu
                registro.amb_tem = amb
                registro.est_tem = est
                registro.save()

        #-- Reutilización de código para mostrar listado con los registros, nuevamente
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
            'msg' : '¡Los registros de Temperatura han sido actualizado!',
            'sector' : 'Formulario',
            'listas': listas,
            'paginas': paginas,
            'pagina_actual': pagina_actual  
        }
        return render(request, 'temperaturas/base/listatemperatura.html', datos)

    except Exception as e:
        print(f'Error al actualizar: {e}')
        datos = {
            'msg' : '¡Error, el formulario de temperatura, no pudo actualizar!',
            'sector' : 'Error'
        }
        return render(request, 'temperaturas/base/temperatura.html', datos)
    

@login_required(login_url='inicio')
def eliminarTemperatura(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoTemperatura, pk=grupo_id)
        grupo.delete()
        
        #-- Reutilización de código para mostrar listado con los registros, nuevamente
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
            'msg' : (f'¡Formulario eliminado!'),
            'sector' : 'Eliminado',
            'listas': listas,
            'paginas': paginas,
            'pagina_actual': pagina_actual
        }
        return render(request, 'temperaturas/base/listatemperatura.html', datos)


    except:
        #-- Reutilización de código para mostrar listado con los registros, nuevamente
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
            'msg' : (f'Error el Formulario, no existe.'),
            'sector' : 'Error',
            'listas': listas,
            'paginas': paginas,
            'pagina_actual': pagina_actual
        }
        return render(request, 'temperaturas/base/listatemperatura.html', datos)
    

@login_required(login_url='inicio')
def DescargarPDFTemperatura(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoTemperatura, pk=grupo_id)
        registros_temperatura = Temperatura.objects.filter(grupotem_id=grupo)

        turnos = Turnos.objects.all()
        # registro.pul_tem.replace(None, '-')

        for registro in registros_temperatura:
            if registro.hor_tem is None:
                registro.hor_tem = '-'
            if registro.pul_tem is None:
                registro.pul_tem = '-'
            if registro.agu_tem is None:
                registro.agu_tem = '-'
            if registro.amb_tem is None:
                registro.amb_tem = '-'
            if registro.est_tem is None:
                registro.est_tem = '-'
            
        #PDF
        template = get_template('temperaturas/form/descargarpdfTemp.html')
        #Renderiza los datos
        html = template.render({
            'grupo': grupo,
            'registros_temperatura': registros_temperatura,
            'turnos': turnos,

        })
        #Respuesta tipo pdf
        response = HttpResponse(content_type='application/pdf')

        #Damos nombre al archivo
        filename = f'Temperatura_L{grupo.lineas_id.num_lin}_{grupo.trabajador_id.nom_tra}_{grupo.dia_id.dia_dia}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response

    except:
        datos = {
            'msg' : '¡Error, el PDF no existe!',
            'sector' : 'Error'
        }
        return render(request, 'temperaturas/base/temperatura.html', datos)
