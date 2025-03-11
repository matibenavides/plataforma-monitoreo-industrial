from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from Cloraciones.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q

from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML


@login_required(login_url='inicio')
def mostrarProducto(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)

    #loop para registros repetidos
    filas = 12
    datos = {
        'filas': range(1, filas + 1),
        'linea': linea,
    }
    
    return render(request, "productos/base/producto.html", datos)

@login_required(login_url='inicio')
def registrarProducto(request, linea_id):

    
    if request.method == 'POST':

        #Datos para Grupo Productos
        obser = request.POST['observacion']

        dia_actual = date.today()
        dia_obj, created = Dia.objects.get_or_create(dia_dia=dia_actual)

        linea = Lineas.objects.get(id=linea_id)
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        trabajador = request.user.trabajador
        producto = Fungicidas.objects.get(id=request.POST['producto']) # input hidden (shield brite 230)

        #Grupo Producto
        grupopro = GrupoProductos.objects.create(
            obs_grp = obser,
            dia_id = dia_obj,
            lineas_id = linea,
            turnos_id = turno,
            trabajador_id = trabajador,
            fungicidas_id = producto,
        )
        grupopro.save()

        #Registros iterables 12 filas
        for i in range(1, 13):
            hora = request.POST.get(f'hora_{i}') or None
            codigo = request.POST.get(f'cod_{i}')
            especie = Especies.objects.get(id=request.POST.get(f'especie_{i}')) if request.POST.get(f'especie_{i}') else None
            variedad = Variedad.objects.get(id=request.POST.get(f'variedad_{i}')) if request.POST.get(f'variedad_{i}') else None
            ccproducto = request.POST.get(f'cc_{i}') or 0
            retard = request.POST.get(f'retard_{i}') or 0
            agua = request.POST.get(f'agua_{i}') or 0
            gasto = request.POST.get(f'gasto_{i}') or 0
            kilos = request.POST.get(f'kilos_{i}') or 0
            bins =  request.POST.get(f'bins_{i}') or 0
            rendimiento = request.POST.get(f'rendimiento_{i}') or 0

            productos = Productos.objects.create(
                grupopro_id = grupopro,
                especies_id = especie,
                variedad_id = variedad,
                hor_pro = hora,
                cod_pro = codigo,
                dof_pro = ccproducto,
                dor_pro = retard,
                doa_pro = agua,
                gas_pro = gasto,
                kil_pro = kilos,
                bin_pro = bins,
                ren_pro = rendimiento,
            )
            productos.save()
        
        messages.success(request, '¡Registro agregado correctamente!')
        return redirect('producto', linea_id=linea.id)

    else:
        
        datos = {
            'linea': linea,
        }

    return render(request, 'productos/base/producto.html', datos)




    pass

