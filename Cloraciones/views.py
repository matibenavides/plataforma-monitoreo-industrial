from django.shortcuts import render
from .models import * 
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.

def mostrarCloracion(request):
    return render(request, "base/cloracion.html")

def registrarEstanque(request):
    if request.method == 'POST':

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        linea_id = Lineas.objects.get(id=1) # id= 1 es Linea 11
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        sector = Sector.objects.get(id=1) # id=1 Es el sector Estanque
        especie = Especies.objects.get(id=request.POST['especieop'])
        trabajador = Trabajador.objects.get(id=1) # id=1 el trabajador Matias

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

    return render(request, 'base/cloracion.html', datos)

def registrarCortaPedicelo(request):
    if request.method == 'POST':

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        linea_id = Lineas.objects.get(id=1) # id= 1 es Linea 11
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        sector = Sector.objects.get(id=2) # id=2 Es el sector Corta Pedicelo
        especie = Especies.objects.get(id=request.POST['especieop'])
        trabajador = Trabajador.objects.get(id=1) # id=1 el trabajador Matias

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

    return render(request, 'base/cloracion.html', datos)

def registrarRetorno(request):
    if request.method == 'POST':

        #Fecha actual
        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        lote_hipo = request.POST['lotehipo']
        lote_acido = request.POST['loteacid']
        linea_id = Lineas.objects.get(id=1) # id= 1 es Linea 11
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        sector = Sector.objects.get(id=3) # id=3 Es el sector Retorno
        especie = Especies.objects.get(id=request.POST['especieop'])
        trabajador = Trabajador.objects.get(id=1) # id=1 el trabajador Matias

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

    return render(request, 'base/cloracion.html', datos)


def mostrarlistaonce(request):
    busqueda = request.GET.get("buscar")
    bloquesLista = GrupoCloracion.objects.all().order_by('-id') # Muestra todos los datos ordenados de manera descendente (-id) 
    
    if busqueda:
        bloquesLista = bloquesLista.filter(
            Q(turnos_id__nom_tur__icontains = busqueda) |
            Q(trabajador_id__nom_tra__icontains = busqueda) |
            Q(sector_id__nom_sec__icontains = busqueda) |
            Q(especies_id__nom_esp__icontains = busqueda) |
            Q(dia_id__dia_dia__icontains = busqueda)
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
        })
        

    paginator = Paginator(bloques_modificados , 10)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1) 




    return render(request, "base/listaonce.html", {"listas": listas, "paginas": paginas, "pagina_actual": pagina_actual})


# def visualizarDatos(request, bloque_id):
#     bloque = get_object_or_404(Bloque, id=bloque_id)
#     registros_cloracion = Cloracion.objects.filter(bloque_id=bloque)

#     registros_data = []
#     for registro in registros_cloracion:
#         registros_data.append({
#             "hora": registro.hor_clo,
#             "ppm": registro.ppm_clo,
#             "ph": registro.phe_clo,
#             "hipoclorito": registro.hcl_clo,
#             "acido": registro.aci_clo,
#             "observacion": registro.obs_clo,
#         })

#     data = {
#         "bloque_id": bloque.id,
#         "registros_cloracion": registros_data
#     }
#     return JsonResponse(data)


