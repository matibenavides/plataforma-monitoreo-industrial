from django.shortcuts import render
from django.http import HttpResponse
from .models import Cloracion, Lineas, Turnos, Trabajador, Sector, Especies, Dia
from datetime import date
import datetime


# Create your views here.

def iniciosesion(request):
    return render(request, "iniciosesion.html")


def muestramenu(request):
    return render(request, "menu.html")


def cloracion(request):
    return render(request, "cloracion.html")

def slide(request):   # Este es una vista para mostrar el slide.html y probar su funcionamiento ante un nuevo cambio de slide.
    return render(request, "slide.html")



def guardarEstanque(request):
    
    return render(request, "slide.html")



def registrarEstanque(request):
    total_hipo = 0
    total_acido = 0

    turno_id = request.POST['turnoop']
    especie_id = request.POST['especieop']
    lote_hipoclorito = request.POST['lotehipo']
    lote_acido = request.POST['loteacid']
    
    #Fecha actúal
    dia_actual = date.today()
    dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)


    turno_obj, created = Turnos.objects.get_or_create(id=int(turno_id))  # Obtener el objeto y el estado de creación
    especie_obj, created = Especies.objects.get_or_create(id=int(especie_id))  # Obtener el objeto y el estado de creación


    for i in range(1, 12): # 11 Filas de inputs
        hora = request.POST.get(f'hora_{i}') or None # Mención al name con formato hora_1 / 2 etc.
        ppm = request.POST.get(f'ppm_{i}') or None
        ph = request.POST.get(f'ph_{i}') or None
        hipoclorito = int(request.POST.get(f'hipo_{i}', 0) or 0)  # 0 en caso de no poseer valores
        acido = int(request.POST.get(f'acid_{i}', 0) or 0) 
        observacion = request.POST.get(f'obs_{i}')

        total_hipo += hipoclorito
        total_acido += acido
        # Sacar este campo, parece sobrar. además de sumar esto con javaScript en el mismo formulario. pensar en los campos de total de ambas para futuro   
        
        # Recorre
        cloracion = Cloracion( 
            lineas_id= Lineas.objects.get(id=1), # id=1 es de linea 11
            turnos_id= turno_obj,
            trabajador_id= Trabajador.objects.get(id=1), # id=1 es el de mati, este campo variará
            sector_id = Sector.objects.get(id=1), # id=1 Es el sector Estanque
            especies_id = especie_obj, 
            dia_id = dia_obj,
            hor_clo = hora,
            ppm_clo = ppm,
            phe_clo = ph,
            hcl_clo = hipoclorito,
            aci_clo = acido,
            loh_clo = lote_hipoclorito,
            loa_clo = lote_acido,
            obs_clo = observacion
        )
        cloracion.save()


    return render(request, "slide.html")