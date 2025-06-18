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

# Create your views here.

@login_required(login_url='inicio')
def mostrarPPM(request, linea_id):
    try:

        #Envia id de linea para mostrar en template.
        #Proposito por diferentes ids enviados por navbar.
        linea = Lineas.objects.get(id=linea_id)

        if linea.id not in [1,3]:
            messages.error(request, 'El id debe ser referente a las líneas de trabajo')
            return redirect('menu')
        
        # Muestra listado de registros en el mismo template
        ppm = PPM.objects.all().order_by('-id')

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            ppm = PPM.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            ppm = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

        lista_formato = []
        for lista in ppm:
            lista_formato.append({
                'id': lista.id,
                'turno': lista.turnos_id.nom_tur.upper(),
                'linea': lista.lineas_id.num_lin,
                'trabajador': f"{lista.trabajador_id.nom_tra.capitalize()} {lista.trabajador_id.app_tra.capitalize()}",
                'hora': lista.hor_ppm,
                'ppm': lista.dat_ppm,
                'ph': lista.phe_ppm,
                'fecha': lista.dia_id.dia_dia.strftime('%Y-%m-%d'), # Formato (2025-02-25)
                'observacion': lista.obs_ppm,
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
        }
        
        return render(request, "ppms/base/ppm.html", datos)
    except Lineas.DoesNotExist:
        messages.error(request, '¡Error, línea inexistente!')
        return redirect('menu')

@login_required(login_url='inicio')
def registrarPPM(request,linea_id):

    linea = Lineas.objects.get(id=linea_id)
    if request.method == 'POST':

        

        # linea = Lineas.objects.get(id=request.POST['lineaop'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])
        trabajador = request.user.trabajador
        hora = request.POST['hora']

        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)
        #Solución, 'Cannot assign "'2025-02-23'": "PPM.dia_id" must be a "Dia" instance.'

        ppm = request.POST['ppm']
        phstr = request.POST['ph']

        ph = float(phstr) if phstr else None
        observacion = request.POST['observacion']

        ppm = PPM.objects.create(
            lineas_id=linea,
            trabajador_id=trabajador,
            turnos_id=turno,
            dia_id=dia_obj, 
            hor_ppm=hora,
            dat_ppm=ppm,
            phe_ppm=ph,
            obs_ppm=observacion,
        )


        messages.success(request, '¡Registro agregado correctamente!')
        

        return redirect('ppm', linea_id=linea.id)
    
    else:
       
        datos = {
            'linea': linea,
            
        }
    return render(request, 'ppms/base/ppm.html', datos)



@login_required(login_url='inicio')
def visualizarPPM(request, grupo_id):
    try:
        ppm = get_object_or_404(PPM, id=grupo_id)
        fecha = ppm.dia_id.dia_dia.strftime('%Y-%m-%d')
        turnos = Turnos.objects.all()
        linea = Lineas.objects.get(id=ppm.lineas_id.id)

        registros = PPM.objects.all().order_by('-id')

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            registros = PPM.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            registros = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

        

        lista_formato = []
        for lista in registros:
            lista_formato.append({
                'id': lista.id,
                'turno': lista.turnos_id.nom_tur.upper(),
                'linea': lista.lineas_id.num_lin,
                'trabajador': f"{lista.trabajador_id.nom_tra.capitalize()} {lista.trabajador_id.app_tra.capitalize()}",
                'hora': lista.hor_ppm,
                'ppm': lista.dat_ppm,
                'ph': lista.phe_ppm,
                'fecha': lista.dia_id.dia_dia.strftime('%Y-%m-%d'), # Formato (2025-02-25)
                'observacion': lista.obs_ppm,
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
            'ppm': ppm,
            'fecha': fecha,
            'turnos': turnos,
            'linea': linea,
        }
        return render(request, 'ppms/form/actualizarppm.html', datos)
    
    except Exception as e:
        
        linea = Lineas.objects.first()

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('ppm', linea_id=linea.id)
    

@login_required(login_url='inicio')
def actualizarPPM(request, grupo_id):
    try:
        ppm = PPM.objects.get(id=grupo_id)

        linea = Lineas.objects.get(id=request.POST['lineaop'])
        turno = Turnos.objects.get(id=request.POST['turnoop'])

        hora = request.POST['hora']
        fecha = request.POST['fecha']
        dia_obj, created = Dia.objects.get_or_create(dia_dia=fecha)

        registro_ppm = request.POST['ppm']
        str_ph = request.POST['ph']
        registro_ph = float(str_ph) if str_ph else None

        observacion = request.POST['observacion']

        ppm.lineas_id = linea
        ppm.turnos_id = turno
        ppm.hor_ppm = hora
        ppm.dia_id = dia_obj
        ppm.dat_ppm = registro_ppm
        ppm.phe_ppm = registro_ph
        ppm.obs_ppm = observacion
        ppm.save()

        messages.success(request, '¡Registro actualizado correctamente!')

        return redirect('ppm', linea_id=linea.id)

    except:
        datos = {
            'linea': linea,
            
        }
    return render(request, 'ppms/base/ppm.html', datos)




@login_required(login_url='inicio')
def eliminarPPM(request, grupo_id):
    try:
        ppm = PPM.objects.get(id=grupo_id)
        linea = ppm.lineas_id
        ppm.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('ppm', linea_id=linea.id)
    except Exception as e:
        
        linea = Lineas.objects.first()
        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('ppm', linea_id=linea.id)
    
def eliminarPPMLista(request, grupo_id):
    try:
        ppm = PPM.objects.get(id=grupo_id)
        
        ppm.delete()
        messages.success(request, '¡Registro eliminado correctamente!')
        return redirect('listappm')
    except Exception as e:

        messages.error(request, f'¡Error, registro inexistente! {e}')
        return redirect('listappm')

    
    


@login_required(login_url='inicio')
def DescargarPDFPPM(request):
    try:
        pagina = request.GET.get("page") or 1
        busqueda = request.GET.get("buscar")
        campo = request.GET.get("campo")
        
        # Consulta base ordenada
        ppm = PPM.objects.all().order_by('-id')

        # Chequea si el usuario es superuser (admin)
        if request.user.is_superuser:
            ppm = PPM.objects.all().order_by('-id')
        else:
            # Filtra registros para usuario normal
            ppm = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')
        
        # Aplicar filtros si se proporcionan "campo" y "buscar"
        if campo:
            if campo == "linea":
                try:
                    linea_num = int(busqueda)
                    if linea_num not in [5, 11]:
                        messages.error(request, '¡La línea debe ser 5 u 11!')
                        return redirect('listappm')
                    ppm = PPM.objects.filter(lineas_id__num_lin__exact=busqueda)
                except ValueError:
                    messages.error(request, '¡El valor de línea debe ser un número!')
                    return redirect('listappm')
            elif campo == "turno":
                try:
                    turno_nom = busqueda
                    if turno_nom not in ['A', 'B', 'a', 'b']:
                        messages.error(request, '¡El turno debe ser A, B!')
                        return redirect('listappm')
                    #  __iexact para comparar sin importar mayúsculas/minúsculas
                    ppm = PPM.objects.filter(turnos_id__nom_tur__iexact=busqueda)
                except ValueError:
                    messages.error(request, '¡En filtro de Turnos, solo se acepta A o B!')
                    return redirect('listappm')
            elif campo == "trabajador":
                # si es numerico, salta error
                if busqueda.replace('.','',1).isdigit():
                    messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                    return redirect('listappm')
                    
                # __icontains para buscar coincidencia parcial y ( | OR ) para ambos campos
                ppm = PPM.objects.filter(
                    Q(trabajador_id__nom_tra__icontains=busqueda) | 
                    Q(trabajador_id__app_tra__icontains=busqueda)
                ).distinct()
            elif campo == "ppm":
                if not busqueda.isdigit():
                    messages.error(request, '¡El valor de PPM debe ser un número entero!')
                    return redirect('listappm')
                    
                ppm = PPM.objects.filter(dat_ppm__exact=busqueda)
            elif campo == "ph":
                if busqueda.replace('.','',1).isdigit() == False:
                    messages.error(request, '¡El valor de PH debe ser un número!')
                    return redirect('listappm')
                
                # Validar que tenga punto decimal
                if '.' not in busqueda:
                    messages.error(request, '¡El valor de PH debe tener punto decimal! Ejemplo: 1.0')
                    return redirect('listappm')          
                ppm = PPM.objects.filter(phe_ppm__exact=busqueda)
            elif campo == "hora":
                try:
                    hora = busqueda.split(':')
                    if len(hora) != 2:
                        messages.error(request, '¡El formato de hora debe ser HH:MM!')
                        return redirect('listappm')
                    
                    ppm = PPM.objects.filter(hor_ppm__exact=busqueda)
                except:
                    messages.error(request, '¡El formato de hora debe ser HH:MM!')
            elif campo == "fecha":
                try:
                    fecha = busqueda.split('-')
                    if len(fecha) != 3:
                        messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                        return redirect('listappm')
                    
                    ppm = PPM.objects.filter(dia_id__dia_dia__exact=busqueda)
                except:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
            elif campo == "observacion":
                ppm = PPM.objects.filter(obs_ppm__icontains=busqueda)
            else:
                messages.error(request, '¡Campo de búsqueda inexistente!')
                return redirect('listappm')
        
        # Formatear los datos para el PDF
        lista_formato = []
        for item in ppm:
            lista_formato.append({
                'id': item.id,
                'turno': item.turnos_id.nom_tur.upper(),
                'linea': item.lineas_id.num_lin,
                'trabajador': f"{item.trabajador_id.nom_tra.capitalize()} {item.trabajador_id.app_tra.capitalize()}",
                'hora': item.hor_ppm,
                'ppm': item.dat_ppm,
                'ph': item.phe_ppm,
                'fecha': item.dia_id.dia_dia.strftime('%Y-%m-%d'),
                'observacion': item.obs_ppm,
            })
        
        # Paginar con 15 registros por página (aplicando el filtro)
        paginator = Paginator(lista_formato, 15)
        listas = paginator.get_page(pagina)
        
        fecha_hoy = date.today().strftime('%Y-%m-%d')
        
        # Renderizar la plantilla para el PDF
        template = get_template('ppms/form/descargarpdfPPM.html')
        html = template.render({
            'listas': listas,
            'fecha_hoy': fecha_hoy,
        })
        
        response = HttpResponse(content_type='application/pdf')
        filename = f'PPM_Registro_Pagina{pagina}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        html = HTML(string=html, base_url=request.build_absolute_uri())
        result = html.write_pdf(encoding='utf-8', presentational_hints=True)
        response.write(result)
        return response

    except Exception as e:
        linea = Lineas.objects.first()
        messages.error(request, f'Error al generar el PDF: {e}')
        return redirect('ppm', linea_id=linea.id)


@login_required(login_url='inicio')
def mostrarListaPPM(request):

    busqueda = request.GET.get("buscar")
    campo = request.GET.get("campo")
    lista = PPM.objects.all().order_by('-id')

    # Chequea si el usuario es superuser (admin)
    if request.user.is_superuser:
        lista = PPM.objects.all().order_by('-id')
    else:
        # Filtra registros para usuario normal
        lista = PPM.objects.filter(trabajador_id=request.user.trabajador).order_by('-id')

    if campo:
        if campo == "linea":
            try:
                linea_num = int(busqueda)
                if linea_num not in [5, 11]:
                    messages.error(request, '¡La línea debe ser 5 u 11!')
                    return redirect('listappm')
                lista = PPM.objects.filter(lineas_id__num_lin__exact=busqueda)
            except ValueError:
                messages.error(request, '¡El valor de línea debe ser un número!')
                return redirect('listappm')
        elif campo == "turno":
            try:
                turno_nom = busqueda
                if turno_nom not in ['A', 'B', 'a', 'b']:
                    messages.error(request, '¡El turno debe ser A, B!')
                    return redirect('listappm')
                #  __iexact para comparar sin importar mayúsculas/minúsculas
                lista = PPM.objects.filter(turnos_id__nom_tur__iexact=busqueda)
            except ValueError:
                messages.error(request, '¡En filtro de Turnos, solo se acepta A o B!')
                return redirect('listappm')
        elif campo == "trabajador":
            # si es numerico, salta error
            if busqueda.replace('.','',1).isdigit():
                messages.error(request, '¡El nombre de trabajador no puede ser un número!')
                return redirect('listappm')
                
            # __icontains para buscar coincidencia parcial y ( | OR ) para ambos campos
            lista = PPM.objects.filter(
                Q(trabajador_id__nom_tra__icontains=busqueda) | 
                Q(trabajador_id__app_tra__icontains=busqueda)
            ).distinct()      
        elif campo == "ppm":
                if not busqueda.isdigit():
                    messages.error(request, '¡El valor de PPM debe ser un número entero!')
                    return redirect('listappm')
                    
                lista = PPM.objects.filter(dat_ppm__exact=busqueda)
        elif campo == "ph":
            if busqueda.replace('.','',1).isdigit() == False:
                messages.error(request, '¡El valor de PH debe ser un número!')
                return redirect('listappm')
            
            # Validar que tenga punto decimal
            if '.' not in busqueda:
                messages.error(request, '¡El valor de PH debe tener punto decimal! Ejemplo: 1.0')
                return redirect('listappm')          
            lista = PPM.objects.filter(phe_ppm__exact=busqueda)
        elif campo == "hora":
            try:
                hora = busqueda.split(':')
                if len(hora) != 2:
                    messages.error(request, '¡El formato de hora debe ser HH:MM!')
                    return redirect('listappm')
                
                lista = PPM.objects.filter(hor_ppm__exact=busqueda)
            except:
                messages.error(request, '¡El formato de hora debe ser HH:MM!')

        elif campo == "fecha":
            try:
                fecha = busqueda.split('-')
                if len(fecha) != 3:
                    messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
                    return redirect('listappm')
                
                lista = PPM.objects.filter(dia_id__dia_dia__exact=busqueda)
            except:
                messages.error(request, '¡El formato de fecha debe ser YYYY-MM-DD!')
            
        elif campo == "observacion":
            lista = PPM.objects.filter(obs_ppm__icontains=busqueda)
        else:
            lista = PPM.objects.all().order_by('-id')
            messages.error(request, '¡Campo de búsqueda inexistente!')

    lista_formato = []
    for grupo in lista:
        lista_formato.append({
            'id': grupo.id,
            'turno': grupo.turnos_id.nom_tur.upper(),
            'linea': grupo.lineas_id.num_lin,
            'trabajador': f"{grupo.trabajador_id.nom_tra.capitalize()} {grupo.trabajador_id.app_tra.capitalize()}",
            'hora': grupo.hor_ppm,
            'ppm': grupo.dat_ppm,
            'ph': grupo.phe_ppm,                                   
            'fecha': grupo.dia_id.dia_dia.strftime('%Y-%m-%d'), # Formato (2025-02-25)
            'observacion': grupo.obs_ppm,
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

    return render(request, 'ppms/base/listappm.html', datos)