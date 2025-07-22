from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime as dt
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
    try:

        #Envia id de linea para mostrar en template.
        #Proposito por diferentes ids enviados por navbar.
        linea = Lineas.objects.get(id=linea_id)

        if linea.id not in [1,3]:
            messages.error(request, 'El id debe ser referente a las líneas de trabajo')
            return redirect('menu')
        
        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            ppm = PPM.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            ppm = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

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
                'fecha': lista.dia_id.dia_dia.strftime('%d-%m-%Y'),
                'observacion': lista.obs_ppm,
            })
        
        paginator = Paginator(lista_formato, 15)
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
    except Lineas.DoesNotExist:
        messages.error(request, '¡Error, línea inexistente!')
        return redirect('menu')

@login_required(login_url='inicio')
def registrarPPM(request,linea_id):

    linea = Lineas.objects.get(id=linea_id)
    if request.method == 'POST':

        

        
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        trabajador = request.user.trabajador
        hora = request.POST['hora']

        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)
        

        ppme = request.POST['ppm']
        phstr = request.POST['ph']

        ph = float(phstr) if phstr else None
        observacion = request.POST['observacion']

        ppm = PPM.objects.create(
            lineas_id=linea,
            trabajador_id=trabajador,
            turnos_id=turno,
            dia_id=dia_obj, 
            hor_ppm=hora,
            dat_ppm=ppme,
            phe_ppm=ph,
            obs_ppm=observacion,
        )

        #Registro en Historial
        descripcion_historial = (
            f"PPM - {ppme} - L{linea.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = ppm,
            descripcion = descripcion_historial
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

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            registros = PPM.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            registros = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

        

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
                'fecha': lista.dia_id.dia_dia.strftime('%d-%m-%Y'),
                'observacion': lista.obs_ppm,
            })
        
        paginator = Paginator(lista_formato, 15)
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
    
    except Exception as e:
        
        linea = Lineas.objects.first()

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('ppm', linea_id=linea.id)
    

@login_required(login_url='inicio')
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

        #Registro en Historial
        descripcion_historial = (
            f"PPM - {registro_ppm} - L{linea.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'EDICIÓN',
            content_object = ppm,
            descripcion = descripcion_historial
        )

        messages.success(request, '¡Registro actualizado correctamente!')

        return redirect('ppm', linea_id=linea.id)

    except:
        datos = {
            'linea': linea,
            
        }
    return render(request, 'ppms/base/ppm.html', datos)




@login_required(login_url='inicio')
def eliminarPPM(request, grupo_id):
    try:
        ppm = PPM.objects.get(id=grupo_id)
        linea = ppm.lineas_id

        #Registro en Historial
        descripcion_historial = (
            f"PPM - {ppm.dat_ppm} - L{ppm.lineas_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = ppm,
            descripcion = descripcion_historial
        )

        ppm.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('ppm', linea_id=linea.id)
    except Exception as e:
        
        linea = Lineas.objects.first()
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('ppm', linea_id=linea.id)

@login_required(login_url='inicio')
def eliminarPPMLista(request, grupo_id):
    try:
        ppm = PPM.objects.get(id=grupo_id)

        #Registro en Historial
        descripcion_historial = (
            f"PPM - {ppm.dat_ppm} - L{ppm.lineas_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = ppm,
            descripcion = descripcion_historial
        )

        ppm.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('listappm')
    except Exception as e:

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listappm')

    
    


@login_required(login_url='inicio')
def DescargarPDFPPM(request):
    try:
        
        

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            ppm = PPM.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            ppm = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')
        
        # Filtros
        turno_filter = request.GET.get('turno')
        linea_filter = request.GET.get('linea')
        trabajador_filter = request.GET.get('trabajador')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        ppm_min = request.GET.get('ppm_min')
        ppm_max = request.GET.get('ppm_max')
        ph_min = request.GET.get('ph_min')
        ph_max = request.GET.get('ph_max')

        if turno_filter:
            ppm = ppm.filter(turnos_id__nom_tur=turno_filter)
        if linea_filter:
            ppm = ppm.filter(lineas_id__num_lin=linea_filter)
        if trabajador_filter:
            ppm = ppm.filter(trabajador_id=trabajador_filter)
        if fecha_inicio:
            try:
                fecha_inicio_dt = dt.strptime(fecha_inicio, "%Y-%m-%d").date()
                ppm = ppm.filter(dia_id__dia_dia__gte=fecha_inicio_dt)
            except:
                pass
        if fecha_fin:
            try:
                fecha_fin_dt = dt.strptime(fecha_fin,"%Y-%m-%d").date()
                ppm = ppm.filter(dia_id__dia_dia__lte=fecha_fin_dt)
            except:
                pass
        if ppm_min:
            try:
                ppm = ppm.filter(dat_ppm__gte=int(ppm_min))
            except ValueError:
                pass
        if ppm_max:
            try:
                ppm = ppm.filter(dat_ppm__lte=int(ppm_max))
            except ValueError:
                pass
        if ph_min:
            try:
                ppm = ppm.filter(phe_ppm__gte=float(ph_min))
            except ValueError:
                pass
        if ph_max:
            try:
                ppm = ppm.filter(phe_ppm__lte=float(ph_max))
            except ValueError:
                pass
        
        # Formatear los datos para el PDF
        lista_formato = []
        for item in ppm:
            lista_formato.append({
                'id': item.id,
                'turno': item.turnos_id.nom_tur.upper(),
                'linea': item.lineas_id.num_lin,
                'trabajador': f"{item.trabajador_id.nom_tra.capitalize()} {item.trabajador_id.app_tra.capitalize()}",
                'hora': item.hor_ppm,
                'ppm': item.dat_ppm,
                'ph': item.phe_ppm,
                'fecha': item.dia_id.dia_dia.strftime('%d-%m-%Y'),
                'observacion': item.obs_ppm,
            })
        
        # Paginar con 15 registros por página (aplicando el filtro)
        pagina = request.GET.get("page") or 1
        paginator = Paginator(lista_formato, 15)
        listas = paginator.get_page(pagina)
        
        fecha_hoy = date.today().strftime('%d-%m-%Y')
        
        # Renderizar la plantilla para el PDF
        template = get_template('ppms/form/descargarpdfPPM.html')
        html = template.render({
            'listas': listas,
            'fecha_hoy': fecha_hoy,
        })
        
        response = HttpResponse(content_type='application/pdf')
        filename = f'PPM_Registro_Pagina{pagina}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response

    except Exception as e:
        linea = Lineas.objects.first()
        messages.error(request, f'Error al generar el PDF: {e}')
        return redirect('ppm', linea_id=linea.id)


@login_required(login_url='inicio')
def mostrarListaPPM(request):
    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        ppm_registros = PPM.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        ppm_registros = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')


    #Filtros
    turno_filter = request.GET.get('turno')
    linea_filter = request.GET.get('linea')
    trabajador_filter = request.GET.get('trabajador')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    ppm_min = request.GET.get('ppm_min')
    ppm_max = request.GET.get('ppm_max')
    ph_min = request.GET.get('ph_min')
    ph_max = request.GET.get('ph_max')

    if turno_filter:
        ppm_registros = ppm_registros.filter(turnos_id__nom_tur=turno_filter)
    if linea_filter:
        ppm_registros = ppm_registros.filter(lineas_id__num_lin=linea_filter)
    if trabajador_filter:
        ppm_registros = ppm_registros.filter(trabajador_id=trabajador_filter)
    if fecha_inicio:
        try:
            fecha_inicio_dt = dt.strptime(fecha_inicio, "%Y-%m-%d").date()
            ppm_registros = ppm_registros.filter(dia_id__dia_dia__gte=fecha_inicio_dt)
        except:
            pass
    if fecha_fin:
        try:
            fecha_fin_dt = dt.strptime(fecha_fin,"%Y-%m-%d").date()
            ppm_registros = ppm_registros.filter(dia_id__dia_dia__lte=fecha_fin_dt)
        except:
            pass
    if ppm_min:
        ppm_registros = ppm_registros.filter(dat_ppm__gte=int(ppm_min))
    if ppm_max:
        ppm_registros = ppm_registros.filter(dat_ppm__lte=int(ppm_max))
    if ph_min:
        ppm_registros = ppm_registros.filter(phe_ppm__gte=float(ph_min))
    if ph_max:
        ppm_registros = ppm_registros.filter(phe_ppm__lte=float(ph_max))

    
    # Valores únicos para los filtros
    turnos_unicos = PPM.objects.values_list('turnos_id__nom_tur', flat=True).distinct().order_by('turnos_id__nom_tur')
    lineas_unicos = PPM.objects.values_list('lineas_id__num_lin', flat=True).distinct().order_by('lineas_id__num_lin')
    trabajador_unicos = Trabajador.objects.all().order_by('nom_tra')



    
    ppm_formato = []
    for grupo in ppm_registros:
        ppm_formato.append({
            'id': grupo.id,
            'turno': grupo.turnos_id.nom_tur.upper(),
            'linea': grupo.lineas_id.num_lin,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'hora': grupo.hor_ppm,
            'ppm': grupo.dat_ppm,
            'ph': grupo.phe_ppm,                                   
            'fecha': grupo.dia_id.dia_dia.strftime('%d-%m-%Y'),
            'observacion': grupo.obs_ppm,
        })

    paginator = Paginator(ppm_formato, 15)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1)

    datos = {
        'listas': listas,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
        'turnos_unicos': turnos_unicos,
        'lineas_unicos': lineas_unicos,
        'trabajador_unicos': trabajador_unicos,
        'ppm_min': ppm_min,
        'ppm_max': ppm_max,
        'ph_min': ph_min,
        'ph_max': ph_max,
        'filtros_activos': {
            'turno': turno_filter,
            'linea': linea_filter,
            'trabajador': trabajador_filter,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'ppm_min': ppm_min,
            'ppm_max': ppm_max,
            'ph_min': ph_min,
            'ph_max': ph_max,
        }
    }

    return render(request, 'ppms/base/listappm.html', datos)