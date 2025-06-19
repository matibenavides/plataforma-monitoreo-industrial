from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Cloraciones.models import *

# from django.views.generic import TemplateView
import json
from django.db.models import Sum, Case, When, IntegerField, FloatField, F, Q, Value
from django.db.models.functions import Round, Coalesce
from datetime import datetime

from django.http.response import JsonResponse
from random import randrange

from .forms import formularioRegistro, TrabajadorForm

# Create your views here.


def iniciosesion(request):

    #verifica usuario
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contraseña']

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, (f"Bienvenido {username}"))
            return redirect('menu')
        else:
            messages.success(request, "Hubo un error al iniciar sesión")
            return redirect('inicio')
    else:
        messages.success(request, "Debes iniciar sesión para acceder a este sitio")
        return render(request, "logins/base/iniciosesion.html")
    




def muestramenu(request):
    if request.user.is_authenticated:
        return render(request, "logins/base/dashboard.html")
    else:
        messages.success(request, "Debes iniciar sesión para acceder a este sitio")
    return redirect('inicio')

def cerrarsesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión")
    return redirect('inicio')

@login_required(login_url='inicio')
def registroUsuario(request):
    if request.method == 'POST':
        form = formularioRegistro(request.POST)
        formTrabajador = TrabajadorForm(request.POST)

        if form.is_valid() and formTrabajador.is_valid():
            usuario = form.save()
            trabajador = formTrabajador.save(commit=False)
            trabajador.user = usuario #asigno el usuario con el trabajador (sus datos)
            trabajador.save()

            #autentico y logeo
            nomUsuario = form.cleaned_data['username']
            contraseña = form.cleaned_data['password1']
            usuario = authenticate(username=nomUsuario, password=contraseña)
            login(request, usuario)
            messages.success(request, "Te has registrado correctamente")
            return redirect('menu')
    else:
        form = formularioRegistro()
        formTrabajador = TrabajadorForm()
        return render(request, 'logins/base/registrousuario.html', {'form': form, 'formTrabajador': formTrabajador})


    return render(request, "logins/base/registrousuario.html", {'form': form})



# ----------------------------------------------------
# ----------- Graficos para Dashboard ----------------
# ----------------------------------------------------

def aniosDisponibles(request):
    # Función para filtrar registros de acuerdo al año
    # Obtiene datos únicos, de acuerdo al año
    years = Dia.objects.values_list('dia_dia__year', flat=True).distinct().order_by('dia_dia__year')
    return JsonResponse({'years': list(years)})



def graficoCloroAcido(request):

    # parámetros de filtrados
    linea_id = request.GET.get('linea_id')
    turno_id = request.GET.get('turno_id')
    fecha_str = request.GET.get('dia_id')
    year = request.GET.get('year')

    


    # Base de la consulta con exclusiones
    registros = Cloracion.objects.exclude(
        Q(hcl_clo__isnull=True) | 
        Q(aci_clo__isnull=True)
    )



    # Filtros generales
    if linea_id:
        registros = registros.filter(grupoclo_id__lineas_id=linea_id)
    if turno_id:
        registros = registros.filter(grupoclo_id__turnos_id=turno_id)
    if year:
        registros = registros.filter(grupoclo_id__dia_id__dia_dia__year=year)
    if fecha_str:
        try:
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            registros = registros.filter(grupoclo_id__dia_id__dia_dia=fecha_dt)
        except ValueError:
            pass
    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        lista = Dosificacion.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        lista = Dosificacion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

    # Consulta directa a la base de datos
    # Agrupando por líneas y sumando directamente en la base de datos
    resultados = registros.values(
        'grupoclo_id__lineas_id__id',
        'grupoclo_id__lineas_id__num_lin'
    ).annotate(
        suma_hcl=Round(Sum('hcl_clo') / 1000.0),
        suma_aci=Round(Sum('aci_clo') / 1000.0)
    ).order_by('grupoclo_id__lineas_id__id')

    #
    sumas_hcl = {}
    sumas_aci = {}

    for resultado in resultados:
        linea_id = resultado['grupoclo_id__lineas_id__id']

        sumas_hcl[linea_id] = resultado['suma_hcl'] or 0
        sumas_aci[linea_id] = resultado['suma_aci'] or 0

    

    suma_hcl_linea11 = sumas_hcl.get(1, 0)
    suma_aci_linea11 = sumas_aci.get(1, 0)

    suma_hcl_linea10 = sumas_hcl.get(2, 0)
    suma_aci_linea10 = sumas_aci.get(2, 0)

    suma_hcl_linea5 = sumas_hcl.get(3, 0)
    suma_aci_linea5 = sumas_aci.get(3, 0)

    

    # Define color variables based on theme
    colors = {
        'primary':  '#8a47f5',  
        'secondary': '#ac86e9',  
        'accent':    '#e0d0f8',  

        # Tonos complementarios
        'contrast1': "#eddffe",   
        'contrast2': '#c3ace7',   
        'contrast3': '#fff6ff',   
    }

        
    chart = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        },
        'legend': {
            # 'right': '5%',
            'orient': 'horizontal',
            'data': [
            'Linea 11',
            'Linea 10', 
            'Linea 5',
            ]
        },
        'series': [
            {
            'name': 'Ácido (Lts)', 
            'type': 'pie',
            'selectedMode': 'single',
            'radius': [0, '30%'],
            'label': {
                'show': True,
                'position': 'inner',
                'formatter': '{b}'
            },
            'labelLine': {
                'show': False
            },
            'data': [
                { 'value': suma_aci_linea11, 'name': 'Linea 11', 'itemStyle': {'color': colors['contrast1']}},
                { 'value': suma_aci_linea10, 'name': 'Linea 10', 'itemStyle': {'color': colors['contrast2']}},
                { 'value': suma_aci_linea5, 'name': 'Linea 5', 'itemStyle': {'color': colors['contrast3']}},
            ]
            },
            {
            'name': 'Hipoclorito (Lts)',
            'type': 'pie',
            'radius': ['45%', '60%'],
            'label': {
                'show': False
            },
            'labelLine': {
                'show': False
            },
            'data': [
                { 'value': suma_hcl_linea11, 'name': 'Linea 11', 'itemStyle': {'color': colors['primary']}},
                { 'value': suma_hcl_linea10, 'name': 'Linea 10', 'itemStyle': {'color': colors['secondary']}},
                { 'value': suma_hcl_linea5, 'name': 'Linea 5', 'itemStyle': {'color': colors['accent']}},
            ]
            }
        ]
    }

    return JsonResponse(chart)

# ----------------------------------------------------
# ----------------------------------------------------

def graficoTemperatura(request):

    # parámetros de filtrados
    linea_id = request.GET.get('linea_id')
    turno_id = request.GET.get('turno_id')
    fecha_str = request.GET.get('dia_id')
    year = request.GET.get('year')

    registros = Temperatura.objects.exclude(
        Q(hor_tem__isnull=True) |
        Q(pul_tem__isnull=True) |
        Q(agu_tem__isnull=True) |
        Q(amb_tem__isnull=True) |
        Q(est_tem__isnull=True)
    )

    if linea_id:
        registros = registros.filter(grupotem_id__lineas_id=linea_id)
    if turno_id:
        registros = registros.filter(grupotem_id__turnos_id=turno_id)
    if year:
        registros = registros.filter(grupotem_id__dia_id__dia_dia__year=year)
    if fecha_str:
        try:
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            registros = registros.filter(grupotem_id__dia_id__dia_dia=fecha_dt)
        except ValueError:
            pass
    

    registros = registros.order_by('hor_tem')

    # Array por tipo de temperatura, que guarda por hora y tipo de temperatura
    # [hora, temperatura]
    pulpa_data = [[registro.hor_tem.hour + registro.hor_tem.minute/60, registro.pul_tem] for registro in registros]
    agua_data = [[registro.hor_tem.hour + registro.hor_tem.minute/60, registro.agu_tem] for registro in registros]
    ambiente_data = [[registro.hor_tem.hour + registro.hor_tem.minute/60, registro.amb_tem] for registro in registros]
    fungicida_data = [[registro.hor_tem.hour + registro.hor_tem.minute/60, registro.est_tem] for registro in registros]

    chart = {
        # 'title': {
        #     'text': "Mediciones de Temperatura por Hora",
        #     'left': "center",
        # },
        'legend': {
            'orient': 'horizontal',
            # 'type': 'scroll',
            # 'top': '5%',
            # 'left': '8%',
            # 'itemGap': 20,
            # 'itemWidth': 14,
            # 'itemHeight': 14,
            'data': ["T° Pulpa", "T° Vaciado", "T° Camara", "T° Fungicida"],
            'selected': {
                "T° Pulpa": True,
                "T° Vaciado": True,
                "T° Camara": True,
                "T° Fungicida": True,
            },
            'textStyle': {'fontSize': 12},
            # 'pageButtonItemGap': 8,
            # 'pageButtonPosition': 'end'
        },
        'dataZoom': {
            'show': True,
            'type': 'slider',
        },
        'toolbox': {
            'show': True,
            'feature': {
                'saveAsImage': { 'show': True },
                'restore': { 'show': True },
                'dataZoom': {
                    'show': True,
                    'title': {
                        'zoom': "Zoom",
                        'back': "Restaurar",
                    }
                },
            },
            'bottom': '0%',
        },
        'dataZoom': [
            {
                'type': 'inside',
                'xAxisIndex': 0,
                'filterMode': 'none'
            },
        ],
        'xAxis': {
            'type': "value",
            # 'name': 'Hora',
            # 'nameLocation': 'middle',
            # 'nameGap': 35,
            # 'nameTextStyle': {'fontSize': 14, 'fontWeight': 'bold'},
            'min': 0,
            'max': 24,
            'interval':3,
            # 'data': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
            #     '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
            #     '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
            #     '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'],
            'axisLine': {'lineStyle': {'width': 1}},
            'axisLabel': {'fontSize': 12}
        },
        'yAxis': {
            'type': "value",
            'min': -5,
            'max': 20,
            'axisLabel': {
                'formatter': '{value} °C'
            },
            'axisLine': {'show': True, 'lineStyle': { 'width': 1}},
            'splitLine': {'show': True, 'lineStyle': {'type': 'dashed'}},
            'axisTick': {'show': True},
        },
        'tooltip': {
            'trigger': 'item',
        },
        'series': [
            {
                'name': "T° Pulpa",
                'type': "scatter",
                'symbol': "pin",
                'data': pulpa_data,
                'itemStyle': { 'color': '#499894' },
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            },
            {
                'name': "T° Vaciado",
                'type': "scatter",
                'symbol': "pin",
                'data': agua_data,
                'itemStyle': { 'color': '#4e79a7'},  
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            },
            {
                'name': "T° Camara",
                'type': "scatter",
                'symbol': "pin",
                'data': ambiente_data,
                'itemStyle': { 'color': '#59a14f'}, 
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            },
            {
                'name': "T° Fungicida",
                'type': "scatter",
                'symbol': "pin",
                'data': fungicida_data,
                'itemStyle': { 'color': '#364F6B'}, 
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            }
        ]
    }
    
    return JsonResponse(chart)

# ----------------------------------------------------
# ----------------------------------------------------

def graficoPPM(request):

    linea_id = request.GET.get('linea_id')
    turno_id = request.GET.get('turno_id')
    fecha_str = request.GET.get('dia_id')
    year = request.GET.get('year')

    registros = Cloracion.objects.select_related(
        'grupoclo_id__dia_id',
        'grupoclo_id__sector_id'
    ).exclude(
        Q(hor_clo__isnull=True) |
        Q(ppm_clo__isnull=True) |
        Q(phe_clo__isnull=True) 
    )

    registrofungi = PPM.objects.select_related(
        'dia_id'
    ).exclude(
        Q(hor_ppm__isnull=True) |
        Q(dat_ppm__isnull=True) |
        Q(phe_ppm__isnull=True) 
    )


    
    if linea_id:
        registros = registros.filter(grupoclo_id__lineas_id=linea_id)
        registrofungi = registrofungi.filter(lineas_id=linea_id)
    if turno_id:
        registros = registros.filter(grupoclo_id__turnos_id=turno_id)
        registrofungi = registrofungi.filter(turnos_id=turno_id)
    if year:
        registros = registros.filter(grupoclo_id__dia_id__dia_dia__year=year)
        registrofungi = registrofungi.filter(dia_id__dia_dia__year=year)
    if fecha_str:
        try:
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            registros = registros.filter(grupoclo_id__dia_id__dia_dia=fecha_dt)
            registrofungi = registrofungi.filter(dia_id__dia_dia=fecha_dt)
        except ValueError:
            pass

    
    registrofungi = registrofungi.order_by('hor_ppm')

    registros_estanque = registros.filter(grupoclo_id__sector_id__id=1).order_by('hor_clo')
    registros_cortapedi = registros.filter(grupoclo_id__sector_id__id=2).order_by('hor_clo')
    registros_retorno = registros.filter(grupoclo_id__sector_id__id=3).order_by('hor_clo')
    
    estanque_ppm = [[r.hor_clo.hour + r.hor_clo.minute/60, r.ppm_clo] for r in registros_estanque]
    estanque_ph = [[r.hor_clo.hour + r.hor_clo.minute/60, r.phe_clo] for r in registros_estanque]

    cortapedi_ppm = [[r.hor_clo.hour + r.hor_clo.minute/60, r.ppm_clo] for r in registros_cortapedi]
    cortapedi_ph = [[r.hor_clo.hour + r.hor_clo.minute/60, r.phe_clo] for r in registros_cortapedi]

    retorno_ppm = [[r.hor_clo.hour + r.hor_clo.minute/60, r.ppm_clo] for r in registros_retorno]
    retorno_ph = [[r.hor_clo.hour + r.hor_clo.minute/60, r.phe_clo] for r in registros_retorno]
    
    fungi_ppm = [[r.hor_ppm.hour + r.hor_ppm.minute/60, r.dat_ppm] for r in registrofungi]
    fungi_ph = [[r.hor_ppm.hour + r.hor_ppm.minute/60, r.phe_ppm] for r in registrofungi]

    chart = {
        # 'title': {
        #     'text': "Mediciones de PPM y Ph",
        #     'left': "center",
        #     'textStyle': {'fontSize': 18, 'fontWeight': 'bold'}
        # },
        'legend': {
            # 'top': 30,
            # 'left': '5%',
            'data': ['Estanque', 'Corta Pedicelo', 'Retorno', 'Fungicida'],
            'selected': {  
                'Estanque': True,
                'Corta Pedicelo': True,
                'Retorno': True,
                'Fungicida': True,
            },
            'selectedMode': 'multiple',
            'textStyle': {'fontSize': 12},
        },
        'tooltip': {
            'trigger': 'item',
            
        },
        'grid': {
            # 'left': '8%',
            # 'right': '8%',
            # 'top': '20%',
            # 'bottom': '15%' # Added to make room for toolbox
        },
        'toolbox': {
            'show': True,
            'feature': {
                'saveAsImage': { 'show': True },
                'restore': { 'show': True },
                'dataZoom': {
                    'show': True,
                    'title': {
                        'zoom': "Zoom",
                        'back': "Restaurar",
                    }
                },
            },
            'bottom': '0%', # Changed from top to bottom
            # 'left': 'center' # Changed to center horizontally
        },
        'dataZoom': [
            {
                'type': 'inside',
                'xAxisIndex': 0,
                'filterMode': 'none'
            }
        ],
        'xAxis': {
            'type': 'value',
            # 'name': 'Hora',
            # 'nameLocation': 'middle',
            # 'nameGap': 35,
            # 'nameTextStyle': {'fontSize': 14, 'fontWeight': 'bold'},
            'min': 0,
            'max': 24,
            'interval': 3,
            'axisLine': {'lineStyle': {'width': 1}},
            'axisLabel': {'fontSize': 12}
        },
        'yAxis': [  
            {
                'type': 'value',
                'name': 'PPM',
                'min':0,
                'max':200,
                'position': 'left',
                'axisLine': {'show': True, 'lineStyle': { 'width': 1}},
                'splitLine': {'show': True, 'lineStyle': {'color':'#eee', 'type': 'solid'}},
                'axisTick': {'show': False},
                'axisLabel': {'fontSize': 11}
            },
            {
                'type': 'value',
                'name': 'pH',
                'min':0,
                'max':7,
                'position': 'right',
                'axisLine': {'show': True, 'lineStyle': { 'width': 1}},
                'axisLabel': {'formatter': '{value}.0', 'fontSize': 11},
                'splitLine': {'show': False},
                'axisTick': {'show': False},
            }
        ],
        'universalTransition': {'enabled': True},
        'series': [
            # Estanque (PPM y pH)
            {
                'id': 'estanque-ppm',
                'name': 'Estanque',
                'type': 'line',
                'yAxisIndex': 0,
                
                'itemStyle': {'color': '#499894'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},  
                'data': estanque_ppm
            },
            {
                'id': 'estanque-ph',
                'name': 'Estanque',
                'type': 'line',
                'yAxisIndex': 1,

                'itemStyle': {'color': '#499894'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},  
                'data': estanque_ph
            },

            # Corta Pedicelo (PPM y pH)
            {
                'id': 'corta-ppm',
                'name': 'Corta Pedicelo',
                'type': 'line',
                'yAxisIndex': 0,
                
                'itemStyle': {'color': '#4e79a7'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},
                'data': cortapedi_ppm
            },
            {
                'id': 'corta-ph',
                'name': 'Corta Pedicelo',
                'type': 'line',
                'yAxisIndex': 1,
                
                'itemStyle': {'color': '#4e79a7'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},
                'data': cortapedi_ph
            },

            # Retorno (PPM y pH)
            {
                'id': 'retorno-ppm',
                'name': 'Retorno',
                'type': 'line',
                'yAxisIndex': 0,

                'itemStyle': {'color': '#59a14f'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},
                'data': retorno_ppm
            },
            {
                'id': 'retorno-ph',
                'name': 'Retorno',
                'type': 'line',
                'yAxisIndex': 1,

                'itemStyle': {'color': '#59a14f'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},
                'data': retorno_ph
            },
            # Fungicida PPM y pH
            {
                'id': 'fungicida-ppm',
                'name': 'Fungicida',
                'type': 'line',
                'yAxisIndex': 0,

                'itemStyle': {'color': '#364F6B'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},
                'data': fungi_ppm
            },
            {
                'id': 'fungicida-ph',
                'name': 'Fungicida',
                'type': 'line',
                'yAxisIndex': 1,

                'itemStyle': {'color': '#364F6B'},
                'smooth': True,
                'emphasis': {'focus': 'series', 'scale': True},
                'blur': {'itemStyle': {'opacity': 0.1}},
                'data': fungi_ph
            },


        ],
        
    }

    return JsonResponse(chart)

# ----------------------------------------------------
# ----------------------------------------------------

def graficoKilogramos(request):
    # Define color variables based on theme
    colors = {
        'primary': '#0c0689',    # --primary
        'secondary': '#ac86e9',  # --secondary
        'accent': '#8a47f5',     # --accent
        'tertiary': '#e0d0f8'    # --tertiary
    }

    # Filtros
    linea_id = request.GET.get('linea_id')
    turno_id = request.GET.get('turno_id')
    year = request.GET.get('year')



    # Registros de Productos
    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        registros = Productos.objects.exclude(
            Q(especies_id__isnull=True) |
            Q(kil_pro__isnull=True)
        )
    else:
        # Filtra registros para usuario normal 
        registros = Productos.objects.exclude(
            Q(especies_id__isnull=True) |
            Q(kil_pro__isnull=True)
        ).filter(grupopro_id__trabajador_id=request.user.trabajador)

    # Filtros para resultados
    if linea_id:
        registros = registros.filter(grupopro_id__lineas_id=linea_id)
    if turno_id:
        registros = registros.filter(grupopro_id__turnos_id=turno_id)
    if year:
        registros = registros.filter(grupopro_id__dia_id__dia_dia__year=year)

    registros = registros.order_by('grupopro_id__dia_id__dia_dia')

    # Agrupo por especie y mes
    resultados = registros.values(
        'especies_id__id',
        'especies_id__nom_esp', 
        'grupopro_id__dia_id__dia_dia__month'
    ).annotate(
        suma_kg = Coalesce(Round(Sum('kil_pro'), 2), Value(0), output_field=FloatField()),
    ).order_by('especies_id__id', 'grupopro_id__dia_id__dia_dia__month')

    # Inicializar arrays para cada especie
    ciruela_data = [0] * 12
    pera_data = [0] * 12
    cereza_data = [0] * 12
    nectarine_data = [0] * 12
    
    # Especies IDs
    CIRUELA_ID = 1
    PERA_ID = 2
    CEREZA_ID = 3
    NECTARINE_ID = 4
    
    # Poblar los arrays con los datos reales
    for r in resultados:
        mes_idx = r['grupopro_id__dia_id__dia_dia__month'] - 1
        if r['especies_id__id'] == CIRUELA_ID:
            ciruela_data[mes_idx] = r['suma_kg']
        elif r['especies_id__id'] == PERA_ID:
            pera_data[mes_idx] = r['suma_kg']
        elif r['especies_id__id'] == CEREZA_ID:
            cereza_data[mes_idx] = r['suma_kg']
        elif r['especies_id__id'] == NECTARINE_ID:
            nectarine_data[mes_idx] = r['suma_kg']

    chart = {
        'legend': {
            'data': ['Ciruela', 'Pera', 'Cereza', 'Nectarine'],
            'textStyle': {'color': colors['primary']}
        },
        'toolbox': {
            'feature': {
                'magicType': {
                    'type': ['stack', 'line', 'bar']
                },
                'dataView': {'readOnly': False},
                'saveAsImage': {'show': True}
            },
            'top': 5,
            'iconStyle': {'borderColor': colors['primary']}
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            },
            'backgroundColor': colors['tertiary'],
            'borderColor': colors['secondary'],
            'textStyle': {'color': colors['primary']}
        },
        'xAxis': {
            'data': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            'name': 'Mes',
            'nameLocation': 'middle',
            'nameGap': 30,
            'axisLine': {'lineStyle': {'color': colors['primary']}},
            'axisLabel': {'color': colors['primary']}
        },
        'yAxis': {
            'type': 'value',
            'name': 'Kilogramos',
            'axisLine': {'lineStyle': {'color': colors['primary']}},
            'axisLabel': {'color': colors['primary']}
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '10%',
            'containLabel': True
        },
        'series': [
            {
                'name': 'Ciruela',
                'type': 'bar',
                'stack': 'total',
                'itemStyle': {'color': colors['primary']},
                'emphasis': {
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': colors['accent']
                    }
                },
                'data': ciruela_data
            },
            {
                'name': 'Pera',
                'type': 'bar',
                'stack': 'total',
                'itemStyle': {'color': colors['secondary']},
                'emphasis': {
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': colors['accent']
                    }
                },
                'data': pera_data
            },
            {
                'name': 'Cereza',
                'type': 'bar',
                'stack': 'total',
                'itemStyle': {'color': colors['accent']},
                'emphasis': {
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': colors['accent']
                    }
                },
                'data': cereza_data
            },
            {
                'name': 'Nectarine',
                'type': 'bar',
                'stack': 'total', 
                'itemStyle': {'color': colors['tertiary']},
                'emphasis': {
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': colors['accent']
                    }
                },
                'data': nectarine_data
            }
        ]
    }
    return JsonResponse(chart)

# ----------------------------------------------------
# ----------------------------------------------------


# ----------------------------------------------------
# ----------- KPIS para el Dashboard ----------------
# ----------------------------------------------------

def kpigeneral(request):
    linea_id = request.GET.get('linea_id')
    turno_id = request.GET.get('turno_id')
    fecha_str = request.GET.get('dia_id')
    year = request.GET.get('year')


    # template fungicida usa shield brite 230 y demáses
    # Tabla Dosificacion
    # Debo clasificar el ccp_dos que es cc de producto, según la clasificación de fungicidas_id

    #Hago exclude para escoger los campos que deseo utilizar
    registros_dosificacion = Dosificacion.objects.exclude(
        Q(ccp_dos__isnull = True) |
        Q(agu_dos__isnull = True) |
        Q(cer_dos__isnull = True) 
    )

    registros_productos = Productos.objects.exclude(
        Q(dor_pro__isnull = True) | # Dosis de retards
        Q(kil_pro__isnull = True) | # Kilos de producción
        Q(bin_pro__isnull = True)   # Cantidad de bins
    )

    #Realizo filtros según parametros
    if linea_id:
        registros_dosificacion = registros_dosificacion.filter(lineas_id=linea_id)
        registros_productos = registros_productos.filter(grupopro_id__lineas_id=linea_id)
    if year:
        registros_dosificacion = registros_dosificacion.filter(dia_id__dia_dia__year=year)
        registros_productos = registros_productos.filter(grupopro_id__dia_id__dia_dia__year=year)
    if fecha_str:
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        registros_dosificacion = registros_dosificacion.filter(dia_id__dia_dia=fecha_dt)
        registros_productos = registros_productos.filter(grupopro_id__dia_id__dia_dia=fecha_dt)
    if turno_id:
        registros_productos = registros_productos.filter(grupopro_id__turnos_id=turno_id)

    

     
    #Realizo la suma de los shield brites según su ID en consulta hacia la BD

    #Coalesce maneja valores nulos en la suma

    kpi_resultados_dosificacion = registros_dosificacion.aggregate(
        # shield son datos en cc, se pasan a litros
        # Agua y cera son Litros
        shbr230_total = Coalesce(Round(Sum('ccp_dos', filter=Q(fungicidas_id=1)) / 1000.0, 2), Value(0), output_field=FloatField()),
        shbr430_total = Coalesce(Round(Sum('ccp_dos', filter=Q(fungicidas_id=2)) / 1000.0, 2), Value(0), output_field=FloatField()),
        shbrpyr_total = Coalesce(Round(Sum('ccp_dos', filter=Q(fungicidas_id=3)) / 1000.0, 2), Value(0), output_field=FloatField()),
        total_agua = Coalesce(Round(Sum('agu_dos')), Value(0), output_field=FloatField()),
        total_cera = Coalesce(Round(Sum('cer_dos')), Value(0), output_field=FloatField()),
    )

    kpi_resultados_productos = registros_productos.aggregate(
        total_retards = Coalesce(Round(Sum('dor_pro')), Value(0), output_field=IntegerField()),
        total_kilos = Coalesce(Round(Sum('kil_pro'), 2), Value(0), output_field=FloatField()),
        total_bins = Coalesce(Round(Sum('bin_pro')), Value(0), output_field=IntegerField()),
    )

    # | une dos diccionarios ( Dictionary union operator )

    kpi_resultados = kpi_resultados_dosificacion | kpi_resultados_productos
    
    return JsonResponse(kpi_resultados)