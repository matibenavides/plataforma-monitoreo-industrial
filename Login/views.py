from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Cloraciones.models import *

# from django.views.generic import TemplateView
import json
from django.db.models import Sum, Case, When, IntegerField, FloatField, F, Q, Value
from django.db.models.functions import Round
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
    

# Este metodo de @login_required funciona y al intentar viajar a /menu manualmente, me redirijirá al path con el nombre 'inicio'.
# El punto, es que no me enviará un mensaje como lo hace la función de abajo en caso de querer intentar ir hacia ese lugar,
# por lo tanto es eficaz en casos especificos por si deseo implementar un mensaje de error o no.

# @login_required(login_url='inicio')
# def muestramenu(request):
#     return render(request, "menu.html")


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

    


        
    chart = {
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        },
        'title': {
                    'text': "Cantidad de Hipoclorito y Ácido",
                    'right': "5%",
                    'textStyle': {'fontSize': 18, 'fontWeight': 'bold'}
                },
        'legend': {
            'top':30,
            'right': '5%',
            'orient': 'vertical',
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
                'position': 'inner',
                'fontSize': 14
            },
            'labelLine': {
                'show': False
            },
            'data': [
                { 'value': suma_aci_linea11, 'name': 'Linea 11', 'selected': True },
                { 'value': suma_aci_linea10, 'name': 'Linea 10' },
                { 'value': suma_aci_linea5, 'name': 'Linea 5' },
            ]
            },
            {
            'name': 'Hipoclorito (Lts)',
            'type': 'pie',
            'radius': ['45%', '60%'],
            'labelLine': {
                'length': 30
            },
            'label': {
                'formatter': '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                'backgroundColor': '#F6F8FC',
                'borderColor': '#8C8D8E',
                'borderWidth': 1,
                'borderRadius': 4,
                'rich': {
                'a': {
                    'color': '#6E7079',
                    'lineHeight': 22,
                    'align': 'center'
                },
                'hr': {
                    'borderColor': '#8C8D8E',
                    'width': '100%',
                    'borderWidth': 1,
                    'height': 0
                },
                'b': {
                    'color': '#4C5058',
                    'fontSize': 14,
                    'fontWeight': 'bold',
                    'lineHeight': 33
                },
                'per': {
                    'color': '#fff',
                    'backgroundColor': '#4C5058',
                    'padding': [3, 4],
                    'borderRadius': 4
                }
                }
            },
            'data': [
                { 'value': suma_hcl_linea11, 'name': 'Linea 11'},
                { 'value': suma_hcl_linea10, 'name': 'Linea 10'},
                { 'value': suma_hcl_linea5, 'name': 'Linea 5' },
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
        'title': {
            'text': "Mediciones de Temperatura por Hora",
            'left': "center",
        },
        'legend': {
            'top': 30,
            'data': ["T° Pulpa Entrada", "T° Agua Vaciado", "T° Ambiente Camara", "T° Estanque Fungicida"],
            'selected': {
                "T° Pulpa Entrada": True,
                "T° Agua Vaciado": True,
                "T° Ambiente Camara": True,
                "T° Estanque Fungicida": True,
            }
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
        },
        'dataZoom': [
            {
                'type': 'inside',
                'xAxisIndex': 0,
                'filterMode': 'none'
            },
            {
                'type': 'slider',
                'xAxisIndex': 0,
                'filterMode': 'none',
                'height': 20,
                
                'handleIcon': 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                'handleSize': '120%'
            }
        ],
        'xAxis': {
            'type': "category",
            'name': 'Hora',
            'nameLocation': 'middle',
            'nameGap': 35,
            'nameTextStyle': {'fontSize': 14, 'fontWeight': 'bold'},
            'data': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
                '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
                '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'],
            
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
                'name': "T° Pulpa Entrada",
                'type': "scatter",
                'symbol': "pin",
                'data': pulpa_data,
                'itemStyle': { 'color': '#FF6B6B' },
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            },
            {
                'name': "T° Agua Vaciado",
                'type': "scatter",
                'symbol': "pin",
                'data': agua_data,
                'itemStyle': { 'color': '#4D96FF'},
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            },
            {
                'name': "T° Ambiente Camara",
                'type': "scatter",
                'symbol': "pin",
                'data': ambiente_data,
                'itemStyle': { 'color': '#FFC300'},
                'symbolSize': 12,
                'emphasis': {'focus': 'series'},
            },
            {
                'name': "T° Estanque Fungicida",
                'type': "scatter",
                'symbol': "pin",
                'data': fungicida_data,
                'itemStyle': { 'color': '#6A4C93'},
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

    registros = Cloracion.objects.exclude(
        Q(hor_clo__isnull=True) |
        Q(ppm_clo__isnull=True) |
        Q(phe_clo__isnull=True) 
    )

    registrofungi = PPM.objects.exclude(
        Q(hor_ppm__isnull=True) |
        Q(dat_ppm__isnull=True) |
        Q(phe_ppm__isnull=True) 
    )

    # Filtros para resultados
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


    # Filtro por sector
    registros_estanque = registros.filter(grupoclo_id__sector_id__id=1).order_by('hor_clo')
    registros_cortapedi = registros.filter(grupoclo_id__sector_id__id=2).order_by('hor_clo')
    registros_retorno = registros.filter(grupoclo_id__sector_id__id=3).order_by('hor_clo')
    
    
    # Lista formateada por sector
    estanque_ppm = [[r.hor_clo.hour + r.hor_clo.minute/60, r.ppm_clo] for r in registros_estanque]
    estanque_ph = [[r.hor_clo.hour + r.hor_clo.minute/60, r.phe_clo] for r in registros_estanque]

    cortapedi_ppm = [[r.hor_clo.hour + r.hor_clo.minute/60, r.ppm_clo] for r in registros_cortapedi]
    cortapedi_ph = [[r.hor_clo.hour + r.hor_clo.minute/60, r.phe_clo] for r in registros_cortapedi]

    retorno_ppm = [[r.hor_clo.hour + r.hor_clo.minute/60, r.ppm_clo] for r in registros_retorno]
    retorno_ph = [[r.hor_clo.hour + r.hor_clo.minute/60, r.phe_clo] for r in registros_retorno]
    
    fungi_ppm = [[r.hor_ppm.hour + r.hor_ppm.minute/60, r.dat_ppm] for r in registrofungi]
    fungi_ph = [[r.hor_ppm.hour + r.hor_ppm.minute/60, r.phe_ppm] for r in registrofungi]


    chart = {
        'title': {
            'text': "Mediciones de PPM y Ph",
            'left': "center",
            'textStyle': {'fontSize': 18, 'fontWeight': 'bold'}
        },
        'legend': {
            'top': 30,  # Ajustado
            'data': ['Estanque', 'Corta Pedicelo', 'Retorno', 'Fungicida'],
            'selected': {  
                'Estanque': True,
                'Corta Pedicelo': True,
                'Retorno': True,
                'Fungicida': True,
            },
            'selectedMode': 'multiple',
            'textStyle': {'fontSize': 14},
        },
        'tooltip': {
            'trigger': 'item',
            
        },
        'grid': {
            'left': '8%',
            'right': '8%',
            'top': '20%',   
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
                'right': '5%',
                'top': '5%',
            },
        },
        'dataZoom': [  # Se mantiene igual
            {
                'type': 'inside',
                'xAxisIndex': 0,
                'filterMode': 'none'
            },
            {
                'type': 'slider',
                'xAxisIndex': 0,
                'filterMode': 'none',
                'height': 20,
                
                'handleIcon': 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                'handleSize': '120%'
            }
        ],
        'xAxis': {
            'type': 'category',
            'name': 'Hora',
            'nameLocation': 'middle',
            'nameGap': 35,
            'nameTextStyle': {'fontSize': 14, 'fontWeight': 'bold'},
            'data': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
                '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
                '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'],
            'axisLine': {'lineStyle': {'width': 1}},
            'axisLabel': {'fontSize': 12}
        },
        'yAxis': [  # Ejes Y duales (se mantienen)
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
                
                'itemStyle': {'color': '#0d47a1'},
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

                'itemStyle': {'color': '#1976d2'},
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
                
                'itemStyle': {'color': '#1b5e20'},
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
                
                'itemStyle': {'color': '#388e3c'},
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

                'itemStyle': {'color': '#b71c1c'},
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

                'itemStyle': {'color': '#d84315'},
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

                'itemStyle': {'color': '#311b92'},
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

                'itemStyle': {'color': '#5e35b1'},
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

    # Filtros

    linea_id = request.GET.get('linea_id')
    turno_id = request.GET.get('turno_id')
    year = request.GET.get('year')

    # Registros de Productos
    registros = Productos.objects.exclude(
        Q(especies_id__isnull=True) |
        Q(kil_pro__isnull=True) 
    )

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
        suma_kg=(Sum('kil_pro'))
    ).order_by('especies_id__id', 'grupopro_id__dia_id__dia_dia__month')


    # Inicializar arrays para cada especie con ceros para todos los meses (1-12)
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
        # Obtener índice de mes (0-11) para acceder al array
        mes_idx = r['grupopro_id__dia_id__dia_dia__month'] - 1
        
        # Asignar valor al array correspondiente según la especie
        if r['especies_id__id'] == CIRUELA_ID:
            ciruela_data[mes_idx] = r['suma_kg']
        elif r['especies_id__id'] == PERA_ID:
            pera_data[mes_idx] = r['suma_kg']
        elif r['especies_id__id'] == CEREZA_ID:
            cereza_data[mes_idx] = r['suma_kg']
        elif r['especies_id__id'] == NECTARINE_ID:
            nectarine_data[mes_idx] = r['suma_kg']

    
    chart = {
        'title': {
            'text': "Kilogramos totales por especie",
            'left': "center",
            'textStyle': { 'fontSize': 18, 'fontWeight': 'bold' }
        },
        'legend': {
            'top': 30, # Separado del título
            'data': ['Ciruela', 'Pera', 'Cereza', 'Nectarine'],
        },
        'toolbox': {
            # Opcional: añadir 'saveAsImage' si quieres esa función
            'feature': {
                'magicType': {
                    'type': ['stack', 'line', 'bar'] # Permitir cambiar a apilado, línea o barra normal
                },
                'dataView': { 'readOnly': False }, # Permitir ver y editar datos
                'saveAsImage': { 'show': True }    # Botón para guardar imagen
            },
            'top': 5 # Posicionar la caja de herramientas un poco más abajo
        },
        'tooltip': {
            'trigger': 'axis', # <-- CAMBIO CLAVE: Activar por eje (mes)
            'axisPointer': { # Mejora la indicación visual del eje
                'type': 'shadow' # Muestra una sombra en la columna del eje
            }
            # No necesitamos un formatter personalizado por ahora,
            # el tooltip por defecto para 'axis' muestra todas las series.
        },
        'xAxis': {
            'data': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            'name': 'Mes', # Nombre del eje X más descriptivo
            'nameLocation': 'middle', # Centrar el nombre
            'nameGap': 30, # Espacio entre etiquetas y nombre del eje
            'axisLine': { 'onZero': True },
            'splitLine': { 'show': False },
            'splitArea': { 'show': False }
        },
        'yAxis': {
            'type': 'value', # Asegurar que el eje Y es numérico
            'name': 'Kilogramos' # Añadir nombre al eje Y
        },
        'grid': {
            'left': '3%', # Ajustar márgenes si es necesario
            'right': '4%',
            'bottom': '10%', # Dejar espacio para la leyenda del zoom si se añade
            'containLabel': True # Asegura que las etiquetas de los ejes no se corten
        },
        'series': [
            {
                'name': 'Ciruela',
                'type': 'bar',
                'stack': 'total', # <-- Apilar todas juntas
                'emphasis': {      # <-- Énfasis estándar
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0,0,0,0.3)'
                    }
                },
                'data': ciruela_data
            },
            {
                'name': 'Pera',
                'type': 'bar',
                'stack': 'total', # <-- Apilar todas juntas
                'emphasis': {      # <-- Énfasis estándar
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0,0,0,0.3)'
                    }
                },
                # Datos ficticios para Pera (ej: patrón creciente)
                'data': pera_data
            },
            {
                'name': 'Cereza',
                'type': 'bar',
                'stack': 'total', # <-- Apilar todas juntas
                'emphasis': {      # <-- Énfasis estándar
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0,0,0,0.3)'
                    }
                },
                # Datos ficticios para Cereza (ej: patrón estacional corto)
                'data': cereza_data
            },
            {
                'name': 'Nectarine',
                'type': 'bar',
                'stack': 'total', # <-- Apilar todas juntas
                'emphasis': {      # <-- Énfasis estándar
                    'focus': 'series',
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0,0,0,0.3)'
                    }
                },
                # Datos ficticios para Nectarine (ej: patrón variable)
                'data': nectarine_data
            }
        ]
    };
    return JsonResponse(chart)

# ----------------------------------------------------
# ----------------------------------------------------