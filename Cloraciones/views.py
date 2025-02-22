from django.shortcuts import render, get_object_or_404, redirect
from .models import * 
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

#weasyprint / pdf
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML



# Create your views here.

@login_required(login_url='inicio')
def mostrarCloracion(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)

    datos = {
        'linea': linea,
    } 
    return render(request, "cloraciones/base/cloracion.html", datos)

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

        datos = {
            'msg' : '¡Formulario agregado!',
            'sector' : 'Estanque'
        }

    return render(request, 'cloraciones/base/cloracion.html', datos)

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

        datos = {
            'msg' : '¡Formulario agregado!',
            'sector' : 'Corta Pedicelo'
        }

    return render(request, 'cloraciones/base/cloracion.html', datos)

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

        datos = {
            'msg' : '¡Formulario agregado!',
            'sector' : 'Retorno'
        }

    return render(request, 'cloraciones/base/cloracion.html', datos)

@login_required(login_url='inicio')
def mostrarListaonce(request):
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
        # !Importante mati: implementar autenticación de django
        # Para evitar que cualquiera ingrese al registro.
        grupo = get_object_or_404(GrupoCloracion, pk=grupo_id)
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