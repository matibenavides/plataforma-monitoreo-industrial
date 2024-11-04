from django.shortcuts import render
from .models import * 
from datetime import date
from django.core.paginator import Paginator



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

        bloque = Bloque.objects.create(
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
            ph = request.POST.get(f'ph_{i}') or None
            hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)
            acido = int(request.POST.get(f'acid_{i}', 0) or 0)
            observacion = request.POST.get(f'obs_{i}') 


            cloracion = Cloracion.objects.create(
                bloque_id = bloque,
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

        bloque = Bloque.objects.create(
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
            ph = request.POST.get(f'ph_{i}') or None
            hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)
            acido = int(request.POST.get(f'acid_{i}', 0) or 0)
            observacion = request.POST.get(f'obs_{i}') 


            cloracion = Cloracion.objects.create(
                bloque_id = bloque,
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


def mostrarlistaonce(request):
    bloquesLista = Bloque.objects.all().order_by('-id') # Muestra todos los datos ordenados de manera descendente (-id) 
    
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

