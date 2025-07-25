from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime as dt
from Cloraciones.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from django.core.paginator import Paginator
from django.db.models import Q

from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML


@login_required(login_url='inicio')
def mostrarProducto(request, linea_id):
    try:
        linea = Lineas.objects.get(id=linea_id)
        if linea.id not in [2,4]:
            messages.error(request, 'El id debe ser referente a las líneas de trabajo')
            return redirect('menu')
        
        #loop para registros repetidos
        filas = 12
        datos = {
            'filas': range(1, filas + 1),
            'linea': linea,
        }
        return render(request, "productos/base/producto.html", datos)

    except Lineas.DoesNotExist:
        messages.error(request, 'La línea especificada no existe')
        return redirect('menu')

    

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

        #Registro en Historial
        nombre_corto = producto.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Producto - {nombre_corto} - L{linea.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = grupopro,
            descripcion = descripcion_historial
        )

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
        
        messages.success(request, '¡Registro agregado correctamente!')
        return redirect('producto', linea_id=linea.id)

    else:
        
        datos = {
            'linea': linea,
        }

    return render(request, 'productos/base/producto.html', datos)



@login_required(login_url='inicio')
def mostrarListaProducto(request):

    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        grupo_productos = GrupoProductos.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        grupo_productos = GrupoProductos.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')


    # Filtros
    turno_filter = request.GET.get('turno')
    linea_filter = request.GET.get('linea')
    trabajador_filter = request.GET.get('trabajador')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    #Aplicación de filtros
    if turno_filter:
        grupo_productos = grupo_productos.filter(turnos_id__nom_tur=turno_filter)
    if linea_filter:
        grupo_productos = grupo_productos.filter(lineas_id__num_lin=linea_filter)
    if trabajador_filter:
        grupo_productos = grupo_productos.filter(trabajador_id=trabajador_filter)
    if fecha_inicio:
        try:
            fecha_inicio_dt = dt.strptime(fecha_inicio, "%Y-%m-%d").date()
            grupo_productos = grupo_productos.filter(dia_id__dia_dia__gte=fecha_inicio_dt)
        except:
            pass
    if fecha_fin:
        try:
            fecha_fin_dt = dt.strptime(fecha_fin, "%Y-%m-%d").date()
            grupo_productos = grupo_productos.filter(dia_id__dia_dia__lte=fecha_fin_dt)
        except:
            pass

    # Valores únicos para los filtros
    turnos_unicos = GrupoProductos.objects.values_list('turnos_id__nom_tur', flat=True).distinct().order_by('turnos_id__nom_tur')
    lineas_unicos = GrupoProductos.objects.values_list('lineas_id__num_lin', flat=True).distinct().order_by('lineas_id__num_lin')
    trabajador_unicos = Trabajador.objects.all().order_by('nom_tra')
        
    grupo_modificado = []
    for grupo in grupo_productos:
        grupo_modificado.append({
            'id': grupo.id,
            'turno': grupo.turnos_id.nom_tur.upper(),
            'linea': grupo.lineas_id.num_lin,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'fecha': grupo.dia_id.dia_dia.strftime('%d-%m-%Y'),
        })

    paginator = Paginator(grupo_modificado, 10)
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
        'filtros_activos':{
            'turno': turno_filter,
            'linea': linea_filter,
            'trabajador': trabajador_filter,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        }
    }
    return render(request, "productos/base/listaproducto.html", datos)


@login_required(login_url='inicio')
def visualizarProducto(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoProductos, pk=grupo_id)
        registros_producto = Productos.objects.filter(grupopro_id = grupo).order_by('id')

        turnos = Turnos.objects.all()
        fecha = grupo.dia_id.dia_dia.strftime("%Y-%m-%d")
        observacion = grupo.obs_grp
        especie = Especies.objects.all()
        variedad = Variedad.objects.all()

        datos= {
            'grupo': grupo,
            'registros_producto': registros_producto,
            'turnos': turnos,
            'fecha': fecha,
            'observacion': observacion,
            'especie': especie,
            'variedad': variedad,
        }
        return render(request, 'productos/form/registroProducto.html', datos)


    except Exception as e:

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listaproducto')



@login_required(login_url='inicio')
def actualizarProducto(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoProductos, pk=grupo_id)

        
        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)
        
        # Actualizar grupo
        grupo.dia_id = dia_obj
        grupo.turnos_id = Turnos.objects.get(id=request.POST['turnoop'])
        grupo.obs_grp = request.POST['observacion']
        grupo.save()

        #Registro en Historial
        nombre_corto = grupo.fungicidas_id.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Producto - {nombre_corto} - L{grupo.lineas_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'EDICIÓN',
            content_object = grupo,
            descripcion = descripcion_historial
        )

        for i in range(1,13):

            #elemento hidden
            producto_id = request.POST.get(f'producto_id_{i}')

            if producto_id:
                registro = Productos.objects.get(id=producto_id)

                hora = request.POST.get(f'hora_{i}') or None
                codigo = request.POST.get(f'cod_{i}')
                especie = Especies.objects.get(id=request.POST.get(f'especie_{i}')) if request.POST.get(f'especie_{i}') else None
                variedad = Variedad.objects.get(id=request.POST.get(f'variedad_{i}')) if request.POST.get(f'variedad_{i}') else None
                ccproducto = float(request.POST.get(f'cc_{i}', '0').replace(',', '.'))
                retard = float(request.POST.get(f'retard_{i}', '0').replace(',', '.'))
                agua = float(request.POST.get(f'agua_{i}', '0').replace(',', '.'))
                gasto = float(request.POST.get(f'gasto_{i}', '0').replace(',', '.'))
                kilos = float(request.POST.get(f'kilos_{i}', '0').replace(',', '.'))
                bins = int(float(request.POST.get(f'bins_{i}', '0').replace(',', '.'))) # En caso de ingresar 1,2 o 1.2. Se guardara como entero
                rendimiento = float(request.POST.get(f'rendimiento_{i}', '0').replace(',', '.'))

                registro.hor_pro = hora
                registro.cod_pro = codigo
                registro.especies_id = especie
                registro.variedad_id = variedad
                registro.dof_pro = ccproducto
                registro.dor_pro = retard
                registro.doa_pro = agua
                registro.gas_pro = gasto
                registro.kil_pro = kilos
                registro.bin_pro = bins
                registro.ren_pro = rendimiento
                registro.save()

        messages.success(request, '¡Registro actualizado correctamente!')
        
        return redirect('listaproducto')

    except Exception as e:

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listaproducto')


@login_required(login_url='inicio')
def eliminarProducto(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoProductos, pk=grupo_id)

        #Registro en Historial
        nombre_corto = grupo.fungicidas_id.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Producto - {nombre_corto} - L{grupo.lineas_id.num_lin}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = grupo,
            descripcion = descripcion_historial
        )

        grupo.delete()

        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('listaproducto')
    except Exception as e:
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listaproducto')



@login_required(login_url='inicio')
def PDFProducto(request, grupo_id):
    try:
        grupo = get_object_or_404(
            GrupoProductos.objects.select_related(
                'lineas_id', 'trabajador_id', 'dia_id'
            ),
            pk=grupo_id
        )
        # Trae solo los campos y relaciones necesarios
        registros_producto = (
            Productos.objects
            .filter(grupopro_id=grupo)
            .select_related('especies_id', 'variedad_id')
            .only(
                'hor_pro', 'gas_pro', 'kil_pro', 'bin_pro', 'ren_pro',
                'especies_id', 'variedad_id', 'cod_pro', 'dof_pro', 'dor_pro', 'doa_pro'
            )
        )

        # Calcula los totales directamente en la base de datos
        agregados = registros_producto.aggregate(
            total_kilos=Sum('kil_pro'),
            total_bins=Sum('bin_pro')
        )
        total_kilos = agregados['total_kilos'] or 0
        total_bins = agregados['total_bins'] or 0

        turnos = Turnos.objects.all()
        especie = Especies.objects.all()
        variedad = Variedad.objects.all()

        # Renderiza el template, maneja los valores nulos/cero en el template
        template = get_template('productos/form/descargarpdfPro.html')
        html = template.render({
            'grupo': grupo,
            'registros_producto': registros_producto,
            'turnos': turnos,
            'especie': especie,
            'variedad': variedad,
            'total_bins': total_bins,
            'total_kilos': total_kilos,
        })
        response = HttpResponse(content_type='application/pdf')
        filename = f'Producto_L{grupo.lineas_id.num_lin}_{grupo.trabajador_id.nom_tra}_{grupo.dia_id.dia_dia}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response

    except Exception as e:
        messages.error(request, f'¡Error, el PDF no existe! {e}')
        return redirect('listaproducto')



