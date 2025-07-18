from django.shortcuts import render, get_object_or_404, redirect
from .models import * 
from datetime import date, datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#weasyprint / pdf
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML




@login_required(login_url='inicio')
def mostrarCloracion(request, linea_id):
    try:
        linea = Lineas.objects.get(id=linea_id)
        if linea.id not in [1, 2, 3]:
            messages.error(request, 'El id debe ser referente a las líneas de trabajo')
            return redirect('menu')

        datos = {
            'linea': linea,
        } 
        return render(request, "cloraciones/base/cloracion.html", datos)
    except Lineas.DoesNotExist:
        messages.error(request, 'La línea especificada no existe')
        return redirect('menu')

@login_required(login_url='inicio')
def registrarEstanque(request):
    if request.method == 'POST':

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        linea_id = Lineas.objects.get(id=request.POST['linea_id'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        sector = Sector.objects.get(id=1) # id=1 Es el sector Estanque
        especie = Especies.objects.get(id=request.POST['especieop'])
        trabajador = request.user.trabajador # Toma el usuario logeado junto a los datos de la tabla Trabajador.

        bloque = GrupoCloracion.objects.create(
            loh_gru = lote_hipo,
            loa_gru = lote_acido,
            dia_id = dia_obj,
            lineas_id = linea_id,
            turnos_id = turno,
            sector_id = sector,
            especies_id = especie,
            trabajador_id = trabajador
            )
        bloque.save()

        #Registro en Historial
        descripcion_historial = (
            f"Cloración - {sector} - L{linea_id.num_lin} - {especie.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = bloque,
            descripcion = descripcion_historial
        )


        for i in range(1, 12):

            hora = request.POST.get(f'hora_{i}') or None
            ppm = request.POST.get(f'ppm_{i}') or None

            # Convierto ph a float para tomar el dato n.n, según función js para escribir digitos en un type="text" y automaticamente agregar punto 
            ph_str = request.POST.get(f'ph_{i}')
            ph = float(ph_str) if ph_str else None

            hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)
            acido = int(request.POST.get(f'acid_{i}', 0) or 0)
            observacion = request.POST.get(f'obs_{i}') 


            cloracion = Cloracion.objects.create(
                grupoclo_id = bloque,
                hor_clo = hora,
                ppm_clo = ppm,
                phe_clo = ph,
                hcl_clo = hipoclorito,
                aci_clo = acido,
                obs_clo = observacion
            )

        messages.success(request, '¡Formulario agregado!')
        return redirect('cloracion', linea_id=linea_id.id)

    return redirect('menu')

@login_required(login_url='inicio')
def registrarCortaPedicelo(request):
    if request.method == 'POST':

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        linea_id = Lineas.objects.get(id=request.POST['linea_id'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        sector = Sector.objects.get(id=2) # id=2 Es el sector Corta Pedicelo
        especie = Especies.objects.get(id=request.POST['especieop'])
        trabajador = request.user.trabajador

        bloque = GrupoCloracion.objects.create(
            loh_gru = lote_hipo,
            loa_gru = lote_acido,
            dia_id = dia_obj,
            lineas_id = linea_id,
            turnos_id = turno,
            sector_id = sector,
            especies_id = especie,
            trabajador_id = trabajador
            )
        bloque.save()

        #Registro en Historial
        descripcion_historial = (
            f"Cloración - {sector} - L{linea_id.num_lin} - {especie.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = bloque,
            descripcion = descripcion_historial
        )


        for i in range(1, 12):

            hora = request.POST.get(f'hora_{i}') or None
            ppm = request.POST.get(f'ppm_{i}') or None

            ph_str = request.POST.get(f'ph_{i}')
            ph = float(ph_str) if ph_str else None

            hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)
            acido = int(request.POST.get(f'acid_{i}', 0) or 0)
            observacion = request.POST.get(f'obs_{i}') 


            cloracion = Cloracion.objects.create(
                grupoclo_id = bloque,
                hor_clo = hora,
                ppm_clo = ppm,
                phe_clo = ph,
                hcl_clo = hipoclorito,
                aci_clo = acido,
                obs_clo = observacion
            )

        messages.success(request, '¡Formulario agregado!')
        return redirect('cloracion', linea_id=linea_id.id)

    return redirect('menu')

@login_required(login_url='inicio')
def registrarRetorno(request):
    if request.method == 'POST':

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        linea_id = Lineas.objects.get(id=request.POST['linea_id'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        sector = Sector.objects.get(id=3) # id=3 Es el sector Retorno
        especie = Especies.objects.get(id=request.POST['especieop'])
        trabajador = request.user.trabajador

        bloque = GrupoCloracion.objects.create(
            loh_gru = lote_hipo,
            loa_gru = lote_acido,
            dia_id = dia_obj,
            lineas_id = linea_id,
            turnos_id = turno,
            sector_id = sector,
            especies_id = especie,
            trabajador_id = trabajador
            )
        bloque.save()

        #Registro en Historial
        descripcion_historial = (
            f"Cloración - {sector} - L{linea_id.num_lin} - {especie.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = bloque,
            descripcion = descripcion_historial
        )


        for i in range(1, 12):

            hora = request.POST.get(f'hora_{i}') or None
            ppm = request.POST.get(f'ppm_{i}') or None

            ph_str = request.POST.get(f'ph_{i}')
            ph = float(ph_str) if ph_str else None

            hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)
            acido = int(request.POST.get(f'acid_{i}', 0) or 0)
            observacion = request.POST.get(f'obs_{i}') 


            cloracion = Cloracion.objects.create(
                grupoclo_id = bloque,
                hor_clo = hora,
                ppm_clo = ppm,
                phe_clo = ph,
                hcl_clo = hipoclorito,
                aci_clo = acido,
                obs_clo = observacion
            )

        messages.success(request, '¡Formulario agregado!')
        return redirect('cloracion', linea_id=linea_id.id)

    return redirect('menu')

@login_required(login_url='inicio')
def mostrarListaonce(request):
    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        grupo_cloracion = GrupoCloracion.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        grupo_cloracion = GrupoCloracion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')


    # Filtros específicos
    turno_filter = request.GET.get('turno')
    linea_filter = request.GET.get('linea')
    trabajador_filter = request.GET.get('trabajador')
    sector_filter = request.GET.get('sector')
    especie_filter = request.GET.get('especie')
    lote_hipo_filter = request.GET.get('lote_hipo')
    lote_acid_filter = request.GET.get('lote_acid')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Aplicar filtros
    if turno_filter:
        grupo_cloracion = grupo_cloracion.filter(turnos_id__nom_tur=turno_filter)
    if linea_filter:
        grupo_cloracion = grupo_cloracion.filter(lineas_id__num_lin=linea_filter)
    if trabajador_filter:
        grupo_cloracion = grupo_cloracion.filter(trabajador_id=trabajador_filter) #Ojo con este considerar usar el username
    if sector_filter:
        grupo_cloracion = grupo_cloracion.filter(sector_id__nom_sec=sector_filter)
    if especie_filter:
        grupo_cloracion = grupo_cloracion.filter(especies_id__nom_esp=especie_filter)
    if lote_hipo_filter:
        grupo_cloracion = grupo_cloracion.filter(loh_gru=lote_hipo_filter)
    if lote_acid_filter:
        grupo_cloracion = grupo_cloracion.filter(loa_gru=lote_acid_filter)
    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            grupo_cloracion = grupo_cloracion.filter(dia_id__dia_dia__gte=fecha_inicio_dt)
        except:
            pass
    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

            grupo_cloracion = grupo_cloracion.filter(dia_id__dia_dia__lte=fecha_fin_dt)
        except:
            pass
        
    # Valores únicos para los filtros
    turnos_unicos = GrupoCloracion.objects.values_list('turnos_id__nom_tur', flat=True).distinct().order_by('turnos_id__nom_tur')
    lineas_unicos = GrupoCloracion.objects.values_list('lineas_id__num_lin', flat=True).distinct().order_by('lineas_id__num_lin')
    trabajador_unicos = Trabajador.objects.all().order_by('nom_tra')
    sector_unicos = GrupoCloracion.objects.values_list('sector_id__nom_sec', flat=True).distinct().order_by('sector_id__nom_sec')
    especie_unicos = GrupoCloracion.objects.values_list('especies_id__nom_esp', flat=True).distinct().order_by('especies_id__nom_esp')


    grupo_modificado = []
    for grupo in grupo_cloracion:
        grupo_modificado.append({
            'id': grupo.id,
            'turno': grupo.turnos_id.nom_tur.upper(),
            'linea': grupo.lineas_id.num_lin,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'especie': grupo.especies_id.nom_esp.capitalize(),
            'sector':grupo.sector_id.nom_sec.capitalize(), 
            'fecha': grupo.dia_id.dia_dia.strftime('%d-%m-%Y'),
        })

    paginator = Paginator(grupo_modificado , 10)
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
        'sector_unicos': sector_unicos,
        'especie_unicos': especie_unicos,
        'filtros_activos': {
            'turno': turno_filter,
            'linea': linea_filter,
            'trabajador': trabajador_filter,
            'sector': sector_filter,
            'especie': especie_filter,
            'lote_hipo': lote_hipo_filter,
            'lote_acid': lote_acid_filter,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        }
    }

    return render(request, "cloraciones/base/listaonce.html", datos)


@login_required(login_url='inicio')
def visualizarDatos(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoCloracion, pk=grupo_id)
        registros_cloracion = Cloracion.objects.filter(grupoclo_id=grupo).order_by('id')

        turnos = Turnos.objects.all()
        especies = Especies.objects.all()
        fecha = grupo.dia_id.dia_dia.strftime("%Y-%m-%d")
        datos = {
            'grupo': grupo,
            'registros_cloracion': registros_cloracion,
            'turnos': turnos,
            'especies': especies,
            'fecha': fecha
        }
        return render(request, 'cloraciones/form/registrodatos.html', datos)
    except Exception as e:
        messages.error(request, f'¡Error, el formulario no existe! {e}')
        return redirect('archivos')
    

@login_required(login_url='inicio')
def actualizarRegistro(request, grupo_id):
    
    try:
        grupo = get_object_or_404(GrupoCloracion, pk=grupo_id)
        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        especie = Especies.objects.get(id=request.POST['especieop'])
        fecha = request.POST['fecha']

        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)
        
        grupoupdate = GrupoCloracion.objects.get(id=grupo_id)

        grupoupdate.loh_gru = lote_hipo
        grupoupdate.loa_gru = lote_acido
        grupoupdate.turnos_id = turno
        grupoupdate.especies_id = especie
        grupoupdate.dia_id = dia_obj
        grupoupdate.save()

        #Registro en Historial
        descripcion_historial = (
            f"Cloración - {grupoupdate.sector_id.nom_sec} - L{grupoupdate.lineas_id.num_lin} - {especie.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'EDICIÓN',
            content_object = grupoupdate,
            descripcion = descripcion_historial
        )

        for i in range(1, 12):

            registro_id = request.POST.get(f'cloracion_id_{i}') # Es el campo hidden para identificar el orden de ids
            
            if registro_id:
                registro = Cloracion.objects.get(id=registro_id)

                hora = request.POST.get(f'hora_{i}') or None
                ppm = request.POST.get(f'ppm_{i}') or None
                ph_str = request.POST.get(f'ph_{i}')
                ph = float(ph_str) if ph_str else None
                hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)
                acido = int(request.POST.get(f'acid_{i}', 0) or 0)
                observacion = request.POST.get(f'obs_{i}')

                
                registro.hor_clo = hora
                registro.ppm_clo = ppm
                registro.phe_clo = ph
                registro.hcl_clo = hipoclorito
                registro.aci_clo = acido
                registro.obs_clo = observacion
                registro.save()

        messages.success(request, '¡Registro actualizado correctamente!')
        return redirect('archivos')
    except Exception as e:
        messages.error(request, f'¡Error, el formulario no se pudo actualizar!')
        return redirect('archivos')
    
@login_required(login_url='inicio')
def eliminarRegistro(request, grupo_id):
   try:
        
        grupo = get_object_or_404(GrupoCloracion, pk=grupo_id)

        #Registro en Historial
        descripcion_historial = (
            f"Cloración - {grupo.sector_id.nom_sec} - L{grupo.lineas_id.num_lin} - {grupo.especies_id.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = grupo,
            descripcion = descripcion_historial
        )

        grupo.delete()

        messages.success(request, '¡Formulario eliminado!')
        return redirect('archivos')

   except Exception as e:
        messages.error(request, f'¡Error, el formulario no existe')
        return redirect('archivos')


    
@login_required(login_url='inicio')
def DescargarPDF(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoCloracion, pk=grupo_id)
        registros_cloracion = Cloracion.objects.filter(grupoclo_id=grupo).order_by('id')

        turnos = Turnos.objects.all()
        especies = Especies.objects.all()

        for registro in registros_cloracion:
            if registro.ppm_clo is None:
                registro.ppm_clo = '-'
            if registro.phe_clo is None:
                registro.phe_clo = '-'
            if registro.hor_clo is None:
                registro.hor_clo = '-'
        
        #Suma de todos los hipocloritos y acidos
        total_hipo = sum([registro.hcl_clo for registro in registros_cloracion])
        total_acido = sum([registro.aci_clo for registro in registros_cloracion])

        #Para generar el PDF
        template = get_template('cloraciones/form/descargarpdf.html')
        # renderiza el template con los datos
        html = template.render({
            'grupo': grupo,
            'registros_cloracion': registros_cloracion,
            'turnos': turnos,
            'especies': especies,
            'total_hipo': total_hipo,
            'total_acido': total_acido
        })
        # genero un response que sea de tipo pdf
        response = HttpResponse(content_type='application/pdf')

        #Construimos el nombre del archivo
        filename = f'Cloracion_L{grupo.lineas_id.num_lin}_{grupo.trabajador_id.nom_tra}_{grupo.dia_id.dia_dia}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response
        
    except Exception as e:
        messages.error(request, f'¡Error, el PDF no existe {e}')
        return redirect('archivos')