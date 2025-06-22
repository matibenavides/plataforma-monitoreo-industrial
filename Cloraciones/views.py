from django.shortcuts import render, get_object_or_404, redirect
from .models import * 
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#weasyprint / pdf
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML



# Create your views here.

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
    busqueda = request.GET.get("buscar")
    campo = request.GET.get("campo")
    
    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        lista = GrupoCloracion.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        lista = GrupoCloracion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

    if campo:
        if campo == "turno":
            try:
                turno_nom = busqueda
                if turno_nom not in ['A', 'B', 'a', 'b']:
                    messages.error(request, '¡El turno debe ser A, B!')
                    return redirect('archivos')
                lista = lista.filter(turnos_id__nom_tur__iexact=busqueda)
            except ValueError:
                messages.error(request, '¡El filtrado de Turnos, solo se acepta A o B!')
                return redirect('archivos')
        elif campo == "linea":
            try:
                linea_num = int(busqueda)
                if linea_num not in [11, 10, 5]:
                    messages.error(request, '¡Puedes buscar registros de las líneas 11, 10 o 5!')
                    return redirect('archivos')
                lista = lista.filter(lineas_id__num_lin__exact=busqueda)
            except ValueError:
                messages.error(request, '¡El valor de línea debe ser un número!')
                return redirect('archivos')
        elif campo == "trabajador":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                return redirect('archivos')
            lista = lista.filter(
                    Q(trabajador_id__nom_tra__icontains=busqueda) | 
                    Q(trabajador_id__app_tra__icontains=busqueda)
                ).distinct()
        elif campo == "sector":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡No se aceptan números en el tipo de sector')
                return redirect('archivos')
            lista = lista.filter(sector_id__nom_sec__icontains=busqueda)
        elif campo == "especie":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡No se aceptan números en la busqueda de especies')
                return redirect('archivos')
            lista = lista.filter(especies_id__nom_esp__icontains=busqueda)
        elif campo == "fecha":
            try:
                fecha = busqueda.split('-')
                if len(fecha) != 3:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                    return redirect('archivos')
                
                lista = lista.filter(dia_id__dia_dia__exact=busqueda)
            except:
                messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
        elif campo == "lote":
            try:
                lista = lista.filter(
                    Q(loh_gru__exact=busqueda) |
                    Q(loa_gru__exact=busqueda)
                    ).distinct()
                if not lista.exists():
                    messages.error(request, '¡No se encontró ningún registro con ese código de lote!')
                    return redirect('archivos')
            except:
                messages.error(request, '¡Error al buscar el código de lote!')
                return redirect('archivos')
        else:
            messages.error(request, '¡Campo de búsqueda inexistente!')
            return redirect('archivos')

    bloques_modificados = []
    for bloque in lista:
        bloques_modificados.append({
            'id': bloque.id,
            'turno': bloque.turnos_id.nom_tur.upper(),
            'linea': bloque.lineas_id.num_lin,
            'trabajador': f"{bloque.trabajador_id.nom_tra.capitalize()} {bloque.trabajador_id.app_tra.capitalize()}",
            'especie': bloque.especies_id.nom_esp.capitalize(),
            'sector':bloque.sector_id.nom_sec.capitalize(), 
            'fecha': bloque.dia_id.dia_dia.strftime('%Y-%m-%d'),
        })

    paginator = Paginator(bloques_modificados , 10)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1) 

    datos = {
        'listas': listas,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
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
    except:
        datos = {
            'msg' : '¡Error, el formulario no existe!',
            'sector' : 'Error'
        }

        return render(request, 'cloraciones/base/cloracion.html', datos)
    

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
        

        #---- Codigo de mostrarListaOnce ----#
        # El sentido de la reutilización del código es para enviar los datos filtrados a la vista,
        #  junto al mensaje de actualización de registros


        busqueda = request.GET.get("buscar")
        bloquesLista = GrupoCloracion.objects.all().order_by('-id') # Muestra todos los datos ordenados de manera descendente (-id) 
        
        if busqueda:
            bloquesLista = bloquesLista.filter(
                Q(turnos_id__nom_tur__icontains = busqueda) |
                Q(trabajador_id__nom_tra__icontains = busqueda) |
                Q(sector_id__nom_sec__icontains = busqueda) |
                Q(especies_id__nom_esp__icontains = busqueda) |
                Q(dia_id__dia_dia__icontains = busqueda) |
                Q(lineas_id__num_lin__icontains = busqueda)
            ).distinct()

        # Lista de diccionario con datos especificos, para formatear
        bloques_modificados = []
        for bloque in bloquesLista:
            bloques_modificados.append({
                "id": bloque.id,
                "turno": bloque.turnos_id.nom_tur.upper(),  
                "trabajador": f"{bloque.trabajador_id.nom_tra.capitalize()} {bloque.trabajador_id.app_tra.capitalize()}",
                "fecha": bloque.dia_id,
                "especie": bloque.especies_id.nom_esp.capitalize(),
                "sector": bloque.sector_id.nom_sec.capitalize(),
                "linea": bloque.lineas_id.num_lin, 
            })
            

        paginator = Paginator(bloques_modificados , 10)
        pagina = request.GET.get("page") or 1
        listas = paginator.get_page(pagina)
        pagina_actual = int(pagina)
        paginas = range(1, listas.paginator.num_pages + 1)

        #--- Diccionario de datos para enviar a la vista ---#
        datos = {
            'msg' : (f'¡Los registros de {grupo.sector_id.nom_sec} han sido actualizado!'),
            'sector' : (f'Formulario {grupo.id}'),
            'listas': listas,
            'paginas': paginas,
            'pagina_actual': pagina_actual
        }
        return render(request, 'cloraciones/base/listaonce.html', datos)

        

    except Exception as e:
        print(f"Error al actualizar: {e}")
        datos = {
            'msg' : '¡Error, el formulario no se pudo actualizar!',
            'sector' : 'Error'
        }

        return render(request, 'cloraciones/base/cloracion.html', datos)
    
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


        #---- Codigo de mostrarListaOnce ----#
        busqueda = request.GET.get("buscar")
        bloquesLista = GrupoCloracion.objects.all().order_by('-id') # Muestra todos los datos ordenados de manera descendente (-id) 
        
        if busqueda:
            bloquesLista = bloquesLista.filter(
                Q(turnos_id__nom_tur__icontains = busqueda) |
                Q(trabajador_id__nom_tra__icontains = busqueda) |
                Q(sector_id__nom_sec__icontains = busqueda) |
                Q(especies_id__nom_esp__icontains = busqueda) |
                Q(dia_id__dia_dia__icontains = busqueda) |
                Q(lineas_id__num_lin__icontains = busqueda)
            ).distinct()

        # Lista de diccionario con datos especificos, para formatear
        bloques_modificados = []
        for bloque in bloquesLista:
            bloques_modificados.append({
                "id": bloque.id,
                "turno": bloque.turnos_id.nom_tur.upper(),  
                "trabajador": f"{bloque.trabajador_id.nom_tra.capitalize()} {bloque.trabajador_id.app_tra.capitalize()}",
                "fecha": bloque.dia_id,
                "especie": bloque.especies_id.nom_esp.capitalize(),
                "sector": bloque.sector_id.nom_sec.capitalize(),
                "linea": bloque.lineas_id.num_lin, 
            })
            

        paginator = Paginator(bloques_modificados , 10)
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
        return render(request, 'cloraciones/base/listaonce.html', datos)

   except:
        #---- Codigo de mostrarListaOnce ----#
        busqueda = request.GET.get("buscar")
        bloquesLista = GrupoCloracion.objects.all().order_by('-id') # Muestra todos los datos ordenados de manera descendente (-id) 
        
        if busqueda:
            bloquesLista = bloquesLista.filter(
                Q(turnos_id__nom_tur__icontains = busqueda) |
                Q(trabajador_id__nom_tra__icontains = busqueda) |
                Q(sector_id__nom_sec__icontains = busqueda) |
                Q(especies_id__nom_esp__icontains = busqueda) |
                Q(dia_id__dia_dia__icontains = busqueda) |
                Q(lineas_id__num_lin__icontains = busqueda)
            ).distinct()

        # Lista de diccionario con datos especificos, para formatear
        bloques_modificados = []
        for bloque in bloquesLista:
            bloques_modificados.append({
                "id": bloque.id,
                "turno": bloque.turnos_id.nom_tur.upper(),  
                "trabajador": f"{bloque.trabajador_id.nom_tra.capitalize()} {bloque.trabajador_id.app_tra.capitalize()}",
                "fecha": bloque.dia_id,
                "especie": bloque.especies_id.nom_esp.capitalize(),
                "sector": bloque.sector_id.nom_sec.capitalize(), 
                "linea": bloque.lineas_id.num_lin, 
            })
            

        paginator = Paginator(bloques_modificados , 10)
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
        return render(request, 'cloraciones/base/listaonce.html', datos)

    
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
        
        # return render(request, 'cloraciones/form/descargarpdf.html', datos)
    except:
        datos = {
            'msg' : '¡Error, el PDF no existe!',
            'sector' : 'Error'
        }

        return render(request, 'cloraciones/base/cloracion.html', datos)