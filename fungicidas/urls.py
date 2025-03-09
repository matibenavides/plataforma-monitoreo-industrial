from django.urls import path
from . import views


urlpatterns = [
    path('fungicida/<int:linea_id>', views.mostrarFungicida, name="fungicida"),

    path('registrar_fungicida/<int:linea_id>', views.registrarFungicida, name="registrarfungicida"),
    path('visualizar_fungicida/<int:grupo_id>/', views.visualizarFungicida, name="visualizarfungicida"),
    path('actualizar_fungicida/<int:grupo_id>/', views.actualizarFungicida, name="actualizarfungicida"),
    path('eliminar_fungicida/<int:grupo_id>/', views.eliminarFungicida, name="eliminarfungicida"),
    path('eliminarlista_fungicida/<int:grupo_id>/', views.eliminarlistaFungicida, name="eliminarlistafungicida"),
    path('archivos_fungicida/', views.mostrarListaFungicida, name="listafungicida"),
    path('pdf_fungicida/', views.DescargarPDFFungicida, name="pdffungicida"),
    


    

]
