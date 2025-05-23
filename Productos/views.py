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



@login_required(login_url='inicio')
def mostrarListaProducto(request):

    busqueda = request.GET.get("buscar")
    campo = request.GET.get("campo")
    lista = GrupoProductos.objects.all().order_by('-id')

    # Filtrado de busqueda por campo de listado
    if campo:
        if campo == "turno":
            try:
                turno_nom = busqueda
                if turno_nom not in ['A', 'B', 'a', 'b']:
                    messages.error(request, '¡El turno debe ser A, B!')
                    return redirect('listaproducto')
                lista = GrupoProductos.objects.filter(turnos_id__nom_tur__iexact=busqueda)
            except ValueError:
                messages.error(request, '¡En filtro de Turnos, solo se acepta A o B!')
                return redirect('listaproducto')
        elif campo == "linea":
            try:
                linea_num = int(busqueda)
                if linea_num not in [10, 1]:
                    messages.error(request, '¡La línea debe ser 10 o 1!')
                    return redirect('listaproducto')
                lista = GrupoProductos.objects.filter(lineas_id__num_lin__exact=busqueda)
            except ValueError:
                messages.error(request, '¡El valor de línea debe ser un número!')
                return redirect('listaproducto')
        elif campo == "trabajador":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                return redirect('listaproducto')
            lista = GrupoProductos.objects.filter(
                    Q(trabajador_id__nom_tra__icontains=busqueda) | 
                    Q(trabajador_id__app_tra__icontains=busqueda)
                ).distinct()
        elif campo == "fecha":
            try:
                fecha = busqueda.split('-')
                if len(fecha) != 3:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                    return redirect('listaproducto')
                
                lista = GrupoProductos.objects.filter(dia_id__dia_dia__exact=busqueda)
            except:
                messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
        elif campo == "observacion":
            lista = GrupoProductos.objects.filter(obs_grp__icontains=busqueda)
        else:
            lista = GrupoProductos.objects.all().order_by('-id')
            messages.error(request, '¡Campo de búsqueda inexistente!')
            return redirect('listaproducto')
        
    lista_formato = []
    for grupo in lista:
        lista_formato.append({
            'id': grupo.id,
            'turno': grupo.turnos_id.nom_tur.upper(),
            'linea': grupo.lineas_id.num_lin,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'fecha': grupo.dia_id.dia_dia.strftime('%Y-%m-%d'),
        })

    paginator = Paginator(lista_formato, 10)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1)

    datos = {
        'listas': listas,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
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
        grupo.delete()

        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('listaproducto')
    except Exception as e:
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listaproducto')

@login_required(login_url='inicio')
def PDFProducto(request, grupo_id):
    try:
        grupo = get_object_or_404(GrupoProductos, pk=grupo_id)
        registros_producto = Productos.objects.filter(grupopro_id=grupo)

        turnos = Turnos.objects.all()
        especie = Especies.objects.all()
        variedad = Variedad.objects.all()

        
        total_kilos = sum(registro.kil_pro for registro in registros_producto)
        total_bins = sum(registro.bin_pro for registro in registros_producto)

        # Reemplaza valores vacíos con '-' después de calcular los totales
        for registro in registros_producto:
            registro.hor_pro = '-' if registro.hor_pro is None else registro.hor_pro
            registro.gas_pro = '-' if registro.gas_pro == 0.0 else registro.gas_pro
            registro.kil_pro = '-' if registro.kil_pro == 0.0 else registro.kil_pro
            registro.bin_pro = '-' if registro.bin_pro == 0 else registro.bin_pro
            registro.ren_pro = '-' if registro.ren_pro == 0.0 else registro.ren_pro

        #PDF
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

        #Nombre archivo
        filename = f'Producto_L{grupo.lineas_id.num_lin}_{grupo.trabajador_id.nom_tra}_{grupo.dia_id.dia_dia}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response

    except Exception as e:
        messages.error(request, f'¡Error, el PDF no existe! {e}')
        return redirect('listaproducto')



