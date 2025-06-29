from django.shortcuts import render, get_object_or_404, redirect
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
def mostrarTemperatura(request, linea_id):
    try:
        linea = Lineas.objects.get(id=linea_id)
        if linea.id not in [1,3]:
            messages.error(request, 'El id debe ser referente a las líneas de trabajo')
            return redirect('menu')
        
        datos = {
        'linea': linea,
        }
        return render(request, "temperaturas/base/temperatura.html", datos)
    except Lineas.DoesNotExist:
        messages.error(request, 'La línea especificada no existe')
        return redirect('menu')
        

    

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

        #Registro en Historial
        descripcion_historial = (
            f"Temperatura - Turno {turno.nom_tur} - L{linea_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = grupotemp,
            descripcion = descripcion_historial
        )

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

        messages.success(request, '¡Formulario agregado!')
        return redirect('temperatura', linea_id=linea_id.id)

    return redirect('menu')




@login_required(login_url='inicio')
def mostrarListaTemperatura(request):
    busqueda = request.GET.get("buscar")
    campo = request.GET.get("campo")
    lista = GrupoTemperatura.objects.all().order_by('-id')

    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        lista = GrupoTemperatura.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        lista = GrupoTemperatura.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

    if campo:
        if campo == "turno":
            try:
                turno_nom = busqueda
                if turno_nom not in ['A', 'B', 'a', 'b']:
                    messages.error(request, '¡El turno debe ser A, B!')
                    return redirect('listatemperatura')
                lista = GrupoTemperatura.objects.filter(turnos_id__nom_tur__iexact=busqueda)
            except ValueError:
                messages.error(request, '¡En filtro de Turnos, solo se acepta A o B!')
                return redirect('listatemperatura')
        elif campo == "linea":
            try:
                linea_num = int(busqueda)
                if linea_num not in [11, 5]:
                    messages.error(request, '¡La línea debe ser 11 o 5!')
                    return redirect('listatemperatura')
                lista = GrupoTemperatura.objects.filter(lineas_id__num_lin__exact=busqueda)
            except ValueError:
                messages.error(request, '¡El valor de línea debe ser un número!')
                return redirect('listatemperatura')
        elif campo == "trabajador":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                return redirect('listatemperatura')
            lista = GrupoTemperatura.objects.filter(
                    Q(trabajador_id__nom_tra__icontains=busqueda) | 
                    Q(trabajador_id__app_tra__icontains=busqueda)
                ).distinct()
        elif campo == "fecha":
            try:
                fecha = busqueda.split('-')
                if len(fecha) != 3:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                    return redirect('listatemperatura')
                
                lista = GrupoTemperatura.objects.filter(dia_id__dia_dia__exact=busqueda)
            except:
                messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
        elif campo == "observacion":
            lista = GrupoTemperatura.objects.filter(obs_grp__icontains=busqueda)
        else:
            lista = GrupoTemperatura.objects.all().order_by('-id')
            messages.error(request, '¡Campo de búsqueda inexistente!')
            return redirect('listatemperatura')
            

    lista_formato = []
    for grupo in lista:
        lista_formato.append({
            'id': grupo.id,
            'turno': grupo.turnos_id.nom_tur.upper(),
            'linea': grupo.lineas_id.num_lin,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'fecha': grupo.dia_id.dia_dia.strftime('%Y-%m-%d'),
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
    }
    return render(request, "temperaturas/base/listatemperatura.html",datos)


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

    
    except Exception as e:
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listatemperatura')


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

        #Registro en Historial
        descripcion_historial = (
            f"Temperatura - Turno {turno.nom_tur} - L{grupoupdate.lineas_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'EDICIÓN',
            content_object = grupoupdate,
            descripcion = descripcion_historial
        )

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

        messages.success(request, '¡Registro actualizado correctamente!')
        return redirect('listatemperatura')

    except Exception as e:
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listatemperatura')
    

@login_required(login_url='inicio')
def eliminarTemperatura(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoTemperatura, pk=grupo_id)

        #Registro en Historial
        descripcion_historial = (
            f"Temperatura - Turno {grupo.turnos_id.nom_tur} - L{grupo.lineas_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = grupo,
            descripcion = descripcion_historial
        )

        grupo.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('listatemperatura')


    except Exception as e:
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listatemperatura')
    

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

    except Exception as e:
        messages.error(request, f'¡Error, el PDF no existe! {e}')
        return redirect('listatemperatura')
