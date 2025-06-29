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
def mostrarFungicida(request, linea_id):
    try:
        linea = Lineas.objects.get(id=linea_id)
        if linea.id not in [2,4]:
            messages.error(request, 'El id debe ser referente a las líneas de trabajo')
            return redirect('menu')

        dosificacion = Dosificacion.objects.all().order_by('-id')

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            dosificacion = Dosificacion.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            dosificacion = Dosificacion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

        lista_formato = []
        for lista in dosificacion:
            lista_formato.append({
                'id': lista.id,
                'fecha': lista.dia_id.dia_dia.strftime('%Y-%m-%d'),
                'hora': lista.hor_dos,
                'producto': lista.fungicidas_id.nom_fun.title(),
                'peso_inicial': lista.pei_dos,
                'peso_final': lista.pef_dos,
                'cc_producto': lista.ccp_dos,
                'linea': lista.lineas_id.num_lin,
                'especie': lista.especies_id.nom_esp.capitalize(),
                'variedad': lista.variedad_id.nom_var.title(),
                'agua': lista.agu_dos,
                'cera': lista.cer_dos,
                'trabajador': f"{lista.trabajador_id.nom_tra.capitalize()} {lista.trabajador_id.app_tra.capitalize()}",
                'observacion': lista.obs_dos,
            })
        
        paginator = Paginator(lista_formato, 15)
        pagina = request.GET.get("page") or 1
        listas = paginator.get_page(pagina)
        pagina_actual = int(pagina)
        paginas = range(1, listas.paginator.num_pages + 1)

        datos = {
            'listas': listas,
            'paginas': paginas,
            'pagina_actual': pagina_actual,
            'linea': linea,
            'dosificacion': dosificacion,
        }
        return render(request, "fungicidas/base/fungicida.html", datos)

    except Lineas.DoesNotExist:
        messages.error(request, 'La línea especificada no existe')
        return redirect('menu')

    


@login_required(login_url='inicio')
def registrarFungicida(request, linea_id):

    linea = Lineas.objects.get(id=linea_id)
    if request.method == 'POST':

        
        especie = Especies.objects.get(id=request.POST['especie'])
        variedad = Variedad.objects.get(id=request.POST['variedad'])
        trabajador = request.user.trabajador

        hora = request.POST['hora']
        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)

        producto = Fungicidas.objects.get(id=request.POST['producto'])
        agua = int(request.POST['agua'] or 0)
        cera = int(request.POST['cera'] or 0)
        
        peso_inicial = request.POST['peso_inicial']
        peso_final = request.POST['peso_final']
        cc_producto = request.POST['cc_producto']

        observacion = request.POST['observacion']

        if agua > 0 and cera > 0:
            messages.error(request, '¡No se puede registrar agua y cera al mismo tiempo!')
            return redirect('fungicida', linea_id=linea.id)
        if agua == 0 and cera == 0:
            messages.error(request, 'Debes diluir al menos en agua o cera')
            return redirect('fungicida', linea_id=linea.id)



        dosificacion = Dosificacion.objects.create(
            lineas_id = linea,
            trabajador_id = trabajador,
            especies_id = especie,
            variedad_id = variedad,
            fungicidas_id = producto,
            dia_id = dia_obj,
            hor_dos = hora,
            pei_dos = peso_inicial,
            pef_dos = peso_final,
            ccp_dos = cc_producto,
            agu_dos = agua,
            cer_dos = cera,
            obs_dos = observacion,
        )
        dosificacion.save()

        #Registro en Historial
        nombre_corto = producto.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Fungicida - {nombre_corto} - L{linea.num_lin} - {especie.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'CREACIÓN',
            content_object = dosificacion,
            descripcion = descripcion_historial
        )
        

        messages.success(request, '¡Registro agregado correctamente!')

        return redirect('fungicida', linea_id=linea.id)
    
    else:

        datos = {
            'linea': linea,
        }
    return render(request, 'fungicidas/base/fungicida.html', datos)


@login_required(login_url='inicio')
def visualizarFungicida(request, grupo_id):
    try:
        dosificacion = get_object_or_404(Dosificacion, id=grupo_id)
        fecha = dosificacion.dia_id.dia_dia.strftime('%Y-%m-%d')
        linea = Lineas.objects.get(id=dosificacion.lineas_id.id)

        especies = Especies.objects.all()
        variedades = Variedad.objects.all()
        productos = Fungicidas.objects.all()

        registros = Dosificacion.objects.all().order_by('-id')

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            registros = Dosificacion.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            registros = Dosificacion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

        lista_formato = []
        for lista in registros:
            lista_formato.append({
                'id': lista.id,
                'fecha': lista.dia_id.dia_dia.strftime('%Y-%m-%d'),
                'hora': lista.hor_dos,
                'producto': lista.fungicidas_id.nom_fun.title(),
                'peso_inicial': lista.pei_dos,
                'peso_final': lista.pef_dos,
                'cc_producto': lista.ccp_dos,
                'linea': lista.lineas_id.num_lin,
                'especie': lista.especies_id.nom_esp.capitalize(),
                'variedad': lista.variedad_id.nom_var.title(),
                'agua': lista.agu_dos,
                'cera': lista.cer_dos,
                'trabajador': f"{lista.trabajador_id.nom_tra.capitalize()} {lista.trabajador_id.app_tra.capitalize()}",
                'observacion': lista.obs_dos,
            })

        paginator = Paginator(lista_formato, 15)
        pagina = request.GET.get("page") or 1
        listas = paginator.get_page(pagina)
        pagina_actual = int(pagina)
        paginas = range(1, listas.paginator.num_pages + 1)

        datos = {
            'pagina_actual': pagina_actual,
            'paginas': paginas,
            'listas': listas,
            'dosificacion': dosificacion,
            'fecha': fecha,
            'linea': linea,
            'especies': especies,
            'variedades': variedades,
            'productos': productos,
        }
        return render(request, 'fungicidas/form/actualizarfungicida.html', datos)


    except Exception as e:

        linea = Lineas.objects.first()

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('fungicida', linea_id=linea.id)
    

@login_required(login_url='inicio')
def actualizarFungicida(request, grupo_id):
    try:
        dosificacion = Dosificacion.objects.get(id=grupo_id)

        linea = Lineas.objects.get(id=request.POST['lineaop'])

        especie = Especies.objects.get(id=request.POST['especie'])
        variedad = Variedad.objects.get(id=request.POST['variedad'])

        hora = request.POST['hora']
        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)

        producto = Fungicidas.objects.get(id=request.POST['producto'])
        agua = int(request.POST['agua'] or 0)
        cera = int(request.POST['cera'] or 0)
        
        peso_inicial = request.POST['peso_inicial']
        peso_final = request.POST['peso_final']
        cc_producto = request.POST['cc_producto']

        observacion = request.POST['observacion']

        if agua > 0 and cera > 0:
            messages.error(request, '¡No puedes actualizar en ambos campos!')
            return redirect('fungicida', linea_id=linea.id)
        if agua == 0 and cera == 0:
            messages.error(request, 'No puedes dejar ambos campos en cero')
            return redirect('fungicida', linea_id=linea.id)

        dosificacion.lineas_id = linea
        dosificacion.especies_id = especie
        dosificacion.variedad_id = variedad
        dosificacion.fungicidas_id = producto
        dosificacion.dia_id = dia_obj
        dosificacion.hor_dos = hora
        dosificacion.pei_dos = peso_inicial
        dosificacion.pef_dos = peso_final
        dosificacion.ccp_dos = cc_producto
        dosificacion.agu_dos = agua
        dosificacion.cer_dos = cera
        dosificacion.obs_dos = observacion
        dosificacion.save()

        #Registro en Historial
        nombre_corto = producto.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Fungicida - {nombre_corto} - L{linea.num_lin} - {especie.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'EDICIÓN',
            content_object = dosificacion,
            descripcion = descripcion_historial
        )



        messages.success(request, '¡Registro actualizado correctamente!')

        return redirect('fungicida', linea_id=linea.id)

    except:
        datos = {
            'linea': linea,
        }
    return render(request, 'fungicidas/base/fungicida.html', datos)


@login_required(login_url='inicio')
def eliminarFungicida(request, grupo_id):
    try:
        dosificacion = Dosificacion.objects.get(id=grupo_id)
        linea = dosificacion.lineas_id

        #Registro en Historial
        nombre_corto = dosificacion.fungicidas_id.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Fungicida - {nombre_corto} - L{dosificacion.lineas_id.num_lin} - {dosificacion.especies_id.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = dosificacion,
            descripcion = descripcion_historial
        )

        dosificacion.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('fungicida', linea_id=linea.id)
    except Exception as e:
        linea = Lineas.objects.first()
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('fungicida', linea_id=linea.id)
    
@login_required(login_url='inicio')
def eliminarlistaFungicida(request, grupo_id):
    try:
        dosificacion = Dosificacion.objects.get(id=grupo_id)

        #Registro en Historial
        nombre_corto = dosificacion.fungicidas_id.nom_fun.lower().replace("shield brite", "sb").strip().capitalize()
        descripcion_historial = (
            f"Fungicida - {nombre_corto} - L{dosificacion.lineas_id.num_lin} - {dosificacion.especies_id.nom_esp}"
        )
        Historial.objects.create(
            trabajador_id = request.user,
            accion = 'ELIMINACIÓN',
            content_object = dosificacion,
            descripcion = descripcion_historial
        )

        dosificacion.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('listafungicida')
    except Exception as e:
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listafungicida')
    

@login_required(login_url='inicio')
def mostrarListaFungicida(request):

    busqueda = request.GET.get("buscar")
    campo = request.GET.get("campo")
    lista = Dosificacion.objects.all().order_by('-id')

    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        lista = Dosificacion.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        lista = Dosificacion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')
    
    if campo:
        if campo == "fecha":
            try:
                fecha = busqueda.split('-')
                if len(fecha) != 3:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                    return redirect('listafungicida')
                
                lista = Dosificacion.objects.filter(dia_id__dia_dia__exact=busqueda)
            except:
                messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
        elif campo == "hora":
            try:
                hora = busqueda.split(':')
                if len(hora) !=2:
                    messages.error(request, '¡El formato de hora debe ser HH:MM!')
                    return redirect('listafungicida')
                
                lista = Dosificacion.objects.filter(hor_dos__exact=busqueda)
            except:
                messages.error(request, '¡El formato de hora debe ser HH:MM!')
        elif campo == "producto":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡La busqueda no puede iniciar con un número o signos')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(Q(fungicidas_id__nom_fun__icontains=busqueda)).distinct()
        elif campo == "peso_inicial":
            if not busqueda.isdigit():
                messages.error(request, '¡El valor de peso, debe ser un número entero!')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(pei_dos__exact=busqueda)
        elif campo == "cc_producto":
            if not busqueda.isdigit():
                messages.error(request, '!El valor de cc, debe ser un número entero!')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(ccp_dos__exact=busqueda)
        elif campo == "linea":
            try:
                linea_num = int(busqueda)
                if linea_num not in [1, 10]:
                    messages.error(request, '¡La línea debe ser 1 o 10')
                    return redirect('listafungicida')
                lista = Dosificacion.objects.filter(lineas_id__num_lin__exact=busqueda)
            except ValueError:
                messages.error(request, '¡El valor de línea debe ser un número!')
                return redirect('listafungicida')
        elif campo == "especie":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡La busqueda no puede iniciar con un número o signos')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(Q(especies_id__nom_esp__icontains=busqueda)).distinct()
        elif campo == "variedad":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡La busqueda no puede iniciar con un número o signos')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(Q(variedad_id__nom_var__icontains=busqueda)).distinct()
        elif campo == "agua":
            if not busqueda.isdigit():
                messages.error(request, '¡El valor de Dilución en Agua, debe ser un número entero!')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(agu_dos__exact=busqueda)
        elif campo == "cera":
            if not busqueda.isdigit():
                messages.error(request, '¡El valor de Dilución en Cera, debe ser un número entero!')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(cer_dos__exact=busqueda)
        elif campo == "trabajador":
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                return redirect('listafungicida')
            lista = Dosificacion.objects.filter(
                    Q(trabajador_id__nom_tra__icontains=busqueda) | 
                    Q(trabajador_id__app_tra__icontains=busqueda)
                ).distinct()
        elif campo == "observacion":
                lista = Dosificacion.objects.filter(obs_dos__icontains=busqueda)
        else:
            lista = Dosificacion.objects.all().order_by('-id')
            messages.error(request, '¡Campo de búsqueda inexistente!')
            return redirect('listafungicida')
    

    lista_formato = []
    for grupo in lista:
        lista_formato.append({
            'id': grupo.id,
            'fecha': grupo.dia_id.dia_dia.strftime('%Y-%m-%d'),
            'hora': grupo.hor_dos,
            'producto': grupo.fungicidas_id.nom_fun.title(),
            'peso_inicial': grupo.pei_dos,
            'peso_final': grupo.pef_dos,
            'cc_producto': grupo.ccp_dos,
            'linea': grupo.lineas_id.num_lin,
            'especie': grupo.especies_id.nom_esp.capitalize(),
            'variedad': grupo.variedad_id.nom_var.title(),
            'agua': grupo.agu_dos,
            'cera': grupo.cer_dos,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'observacion': grupo.obs_dos,
        })

    paginator = Paginator(lista_formato, 15)
    pagina = request.GET.get("page") or 1
    listas = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, listas.paginator.num_pages + 1)

    datos = {
        'listas': listas,
        'paginas': paginas,
        'pagina_actual': pagina_actual,
    }
    return render(request, 'fungicidas/base/listafungicida.html', datos)


@login_required(login_url='inicio')
def DescargarPDFFungicida(request):
    try:
        pagina = request.GET.get("page") or 1
        busqueda = request.GET.get("buscar")
        campo = request.GET.get("campo")

        dosificacion = Dosificacion.objects.all().order_by('-id')

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            dosificacion = Dosificacion.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            dosificacion = Dosificacion.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

        if campo:
            if campo == "fecha":
                try:
                    fecha = busqueda.split('-')
                    if len(fecha) != 3:
                        messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                        return redirect('listafingicida')
                    
                    dosificacion = Dosificacion.objects.filter(dia_id__dia_dia__exact=busqueda)
                except:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
            elif campo == "hora":
                try:
                    hora = busqueda.split(':')
                    if len(hora) !=2:
                        messages.error(request, '¡El formato de hora debe ser HH:MM!')
                        return redirect('listafungicida')
                    
                    dosificacion = Dosificacion.objects.filter(hor_dos__exact=busqueda)
                except:
                    messages.error(request, '¡El formato de hora debe ser HH:MM!')
            elif campo == "producto":
                if busqueda.replace('.','',1).isdigit():
                    messages.error(request, '¡La busqueda no puede iniciar con un número o signos')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(Q(fungicidas_id__nom_fun__icontains=busqueda)).distinct()
            elif campo == "peso_inicial":
                if not busqueda.isdigit():
                    messages.error(request, '¡El valor de peso, debe ser un número entero!')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(pei_dos__exact=busqueda)
            elif campo == "cc_producto":
                if not busqueda.isdigit():
                    messages.error(request, '!El valor de cc, debe ser un número entero!')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(ccp_dos__exact=busqueda)
            elif campo == "linea":
                try:
                    linea_num = int(busqueda)
                    if linea_num not in [1, 10]:
                        messages.error(request, '¡La línea debe ser 1 o 10')
                        return redirect('listafungicida')
                    dosificacion = Dosificacion.objects.filter(lineas_id__num_lin__exact=busqueda)
                except ValueError:
                    messages.error(request, '¡El valor de línea debe ser un número!')
                    return redirect('listafungicida')
            elif campo == "especie":
                if busqueda.replace('.','',1).isdigit():
                    messages.error(request, '¡La busqueda no puede iniciar con un número o signos')
                    return redirect('listafungicida')
                lista = Dosificacion.objects.filter(Q(especies_id__nom_esp__icontains=busqueda)).distinct()
            elif campo == "variedad":
                if busqueda.replace('.','',1).isdigit():
                    messages.error(request, '¡La busqueda no puede iniciar con un número o signos')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(Q(variedad_id__nom_var__icontains=busqueda)).distinct()
            elif campo == "agua":
                if not busqueda.isdigit():
                    messages.error(request, '¡El valor de Dilución en Agua, debe ser un número entero!')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(agu_dos__exact=busqueda)
            elif campo == "cera":
                if not busqueda.isdigit():
                    messages.error(request, '¡El valor de Dilución en Cera, debe ser un número entero!')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(cer_dos__exact=busqueda)
            elif campo == "trabajador":
                if busqueda.replace('.','',1).isdigit():
                    messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                    return redirect('listafungicida')
                dosificacion = Dosificacion.objects.filter(
                        Q(trabajador_id__nom_tra__icontains=busqueda) | 
                        Q(trabajador_id__app_tra__icontains=busqueda)
                    ).distinct()
            elif campo == "observacion":
                    dosificacion = Dosificacion.objects.filter(obs_dos__icontains=busqueda)
            else:
                dosificacion = Dosificacion.objects.all().order_by('-id')
                messages.error(request, '¡Campo de búsqueda inexistente!')
                return redirect('listafungicida')
        
        
        lista_formato = []
        for grupo in dosificacion:
            lista_formato.append({
                'id': grupo.id,
                'fecha': grupo.dia_id.dia_dia.strftime('%Y-%m-%d'),
                'hora': grupo.hor_dos,
                'producto': grupo.fungicidas_id.nom_fun.title(),
                'peso_inicial': grupo.pei_dos,
                'peso_final': grupo.pef_dos,
                'cc_producto': grupo.ccp_dos,
                'linea': grupo.lineas_id.num_lin,
                'especie': grupo.especies_id.nom_esp.capitalize(),
                'variedad': grupo.variedad_id.nom_var.title(),
                'agua': grupo.agu_dos,
                'cera': grupo.cer_dos,
                'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
                'observacion': grupo.obs_dos,
            })

        paginator = Paginator(lista_formato, 15)
        listas = paginator.get_page(pagina)

        fecha_hoy = date.today().strftime('%Y-%m-%d')

        total_agua = sum([registro['agua'] for registro in lista_formato])
        total_cera = sum([registro['cera'] for registro in lista_formato]) 
        total_cc = sum([registro['cc_producto'] for registro in lista_formato])

        template = get_template('fungicidas/form/descargarpdfFungicida.html')
        html = template.render({
            'listas': listas,
            'fecha_hoy': fecha_hoy,
            'total_agua': total_agua,
            'total_cera': total_cera,
            'total_cc': total_cc,
        })

        response = HttpResponse(content_type='application/pdf')
        filename = f'Fungicida_Registro_Pagina{pagina}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response

    except Exception as e:
        linea = Lineas.objects.first()
        messages.error(request, f'Error al generar el PDF: {e}')
        return redirect('fungicida', linea_id=linea.id)